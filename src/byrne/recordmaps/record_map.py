from abc import ABC, abstractmethod


class RecordMap(ABC):
    @abstractmethod
    def map_record(self, record: dict):
        raise NotImplementedError

    @abstractmethod
    def unmap_object(self, obj) -> dict:
        raise NotImplementedError
