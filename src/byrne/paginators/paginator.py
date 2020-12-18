from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor
from typing import Callable

from boto3_type_annotations import dynamodb

from ..table import Table
from ..constants import DEFAULT_PAGE

PAGE_FUNC = Callable[[dynamodb.Client, str], dict]  # def page_func(client, last_evaluated_key=None) -> {'Items':{...}}
COND_FUNC = Callable[[int], bool]  # def condition_func(current_item_length) -> true/false


class Paginator(ABC):
    def __init__(self, table: Table, base_args: dict, page_length: int = DEFAULT_PAGE, preload=True):
        self._table = table
        self._items = []
        self._eof = False
        self._executor = ThreadPoolExecutor()
        self._last_page = None
        self._last_key = None
        self._base_args = base_args
        self._page_length = page_length
        if preload:
            self.trigger_page()
            self.ingest_page()

    @property
    def should_page(self):
        return len(self._items) <= self._page_length

    @property
    def can_page(self):
        return self._last_page is None

    @property
    def next_call_args(self):
        if self._last_key is None:
            return self._base_args
        args = {"start": self._last_key}
        args.update(self._base_args)
        return args

    @abstractmethod
    def on_page(self):
        raise NotImplementedError

    def trigger_page(self):
        self._page = self._executor.submit(lambda: self.on_page())

    def ingest_page(self):
        result = self._page.result()
        self._page = None

        if "LastEvaluatedKey" in result:
            self._last_key = result["LastEvaluatedKey"]
        else:
            self._last_key = None
            self._eof = True

        new_items = result["Items"]
        new_items.reverse()

        self._items = new_items + self._items

    def __iter__(self):
        if self._eof:
            raise RuntimeError("Paginator called after EOF")

        while not self._eof and len(self._items) > 0:
            if not self._eof and self.should_page and self.can_page:
                self.trigger_page()
            
            if self._page.done or len(self._items) == 0:
                self.ingest_page()

            yield self._items.pop()