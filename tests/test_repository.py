import os
import json
from typing import Self, assert_type

import pytest
from src.accessdata.jsonl_repository import JsonlRepository
from src.interfaces.repository import IDataAccessRepository
from src.services.log_service import ILogger


class MockLogger(ILogger):
    def log_debug(self, message: str):
        print(f"DEBUG: {message}")


    def log_info(self, message: str) -> Self:
        print(f"INFO: {message}")


    def log_warning(self, message: str) -> Self:
        print(f"WARNING: {message}")


    def log_error(self, message: str) -> Self:
        print(f"ERROR: {message}")


    def log_critical(self, message: str) -> Self:
        print(f"CRITICAL: {message}")


@pytest.fixture
def temp_db_path(tmpdir):
    return os.path.join(tmpdir, "test_db.jsonl")


@pytest.fixture
def repository(temp_db_path) -> IDataAccessRepository:
    return JsonlRepository(temp_db_path, MockLogger())


def test_insert(repository, temp_db_path):
    # given
    item = {"id": 1, "name": "Test Item"}

    # when
    inserted_item = repository.insert(item)

    # then
    assert inserted_item == item

    # check if item append in file
    with open(temp_db_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    assert len(lines) == 1
    assert json.loads(lines[0]) == item


def test_get_first_when_item_exists(repository, temp_db_path):
    # given
    item = {"id": 1, "name": "Test Item"}
    repository.insert(item)

    # when
    first_item = repository.get_first_or_default({"id": 1 })

    # then
    assert first_item is not None
    assert first_item == item


def test_update_exists_item(repository, temp_db_path):
    item = {"id": 1, "name": "Test Item"}
    repository.insert(item)

    # given
    item_to_update = {"id": 1, "name": "Test Item Updated"}

    # when
    updated_item = repository.update(item_to_update, {"id": 1})

    # then
    assert item_to_update == updated_item