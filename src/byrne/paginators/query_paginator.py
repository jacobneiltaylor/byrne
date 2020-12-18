from .paginator import Paginator

class QueryPaginator(Paginator):
    def on_page(self):
        return self._table.query(**self.next_call_args)
