from .paginator import Paginator

class ScanPaginator(Paginator):
    def on_page(self):
        return self._table.scan(**self.next_call_args)
