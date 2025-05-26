from abc import ABC, abstractmethod
from typing import Optional

class IDataAccessRepository(ABC):
    @abstractmethod
    def insert(self, item: dict) -> dict:
        """
        Inserts a new item into the data store.

        :param item: A dictionary representing the item to insert.
        :return: The inserted item, potentially with added fields (e.g., generated ID).
        """
        pass

    @abstractmethod
    def get_first_or_default(self, id_keys: dict[str, str | int]) -> Optional[dict]:
        """
        Retrieves the first matching item from the data store based on the given key(s).

        :param id_keys: A dictionary of identifying keys used to find the item (e.g., {"id": "123"}).
        :return: The matching item as a dictionary, or None if not found.
        """
        pass

    @abstractmethod
    def update(self, new_item: dict, id_keys: dict[str, str | int]) -> dict:
        """
        Updates an existing item in the data store based on the given key(s).

        :param new_item: A dictionary with updated item data.
        :param id_keys: A dictionary of keys to identify which item to update.
        :return: The updated item as a dictionary.
        """
        pass