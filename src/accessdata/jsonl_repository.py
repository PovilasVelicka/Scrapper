import json
from typing import Optional
from src.services.log_service import ILogger
from src.interfaces import repository as repo
import os

class JsonlRepository(repo.IDataAccessRepository):
    def __init__(self, db_path: str, logger: ILogger):
        directory = os.path.dirname(db_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        self.__db_path = db_path
        self.__logger = logger


    def insert(self,  item: dict) -> dict:
        with open(self.__db_path, 'a', encoding='utf-8') as f:
            new_line = json.dumps(item, ensure_ascii=False) + '\n'
            f.write(new_line)
        return item


    def get_first_or_default(self, id_keys: dict[str, str | int]) -> Optional[dict]:
        if not os.path.exists(self.__db_path):
            return None

        with open(self.__db_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue

                try:
                    item = json.loads(line)
                except json.JSONDecodeError:
                    self.__logger.log_error(
                        f"Invalid JSON in file {self.__db_path}: {line}"
                    )
                    continue

                if self._is_equals(item, id_keys):
                    return item
        return None


    def update(self, new_item: dict, id_keys: dict[str, str | int]) -> dict:
        # Prepare a path for the temporary file
        temp_file = self.__db_path + ".tmp"

        # Open the original database file for reading, and a temporary file for writing
        with open(self.__db_path, 'r', encoding='utf-8') as r, open(temp_file, 'w', encoding='utf-8') as w:
            while line := r.readline():
                obj = json.loads(line)

                # If the current line does not match the ID keys, write it as is
                if not self._is_equals(obj, id_keys):
                    w.write(line)
                    continue

                # If a match is found, write the new item instead of the original
                new_line = json.dumps(new_item, ensure_ascii=False) + '\n'
                w.write(new_line)

                # After updating the matching line, copy the rest of the file as is
                for line in r:
                    w.write(line)
                break

        # Replace the old file with the new updated file atomically
        os.replace(temp_file, self.__db_path)

        # Return the updated item for verification
        updated_item = self.get_first_or_default(id_keys)
        if not updated_item:
            raise ValueError('Unable to update item.')
        return updated_item


    @staticmethod
    def _is_equals(item: dict, id_keys: dict[str: str | int]) -> bool:
        return all([item[k] == v for k, v in id_keys.items()])