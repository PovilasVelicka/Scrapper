import os
import pytest
from typing import Self
from src.accessdata.jsonl_repository import JsonlRepository
from src.accessdata.xlsx_repository import ExcelRepository
from src.accessdata.sql_repository import SqlRepository
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
def temp_item():
    return {"name": "MAXIMERA", "description": "aukštas stalčius, balta, 60x60 cm", "price": "55", "details": [{"Plotis": "56,4 cm"}, {"Rėmas, plotis": "60,0 cm"}, {"Gylis": "54,2 cm"}, {"Aukštis": "21,2 cm"}, {"Rėmas, gylis": "60,0 cm"}, {"Didž. apkrova": "25 kg"}], "id": "902.046.39"}


@pytest.fixture
def temp_db_path(request, tmpdir):
    file_type = request.param
    return os.path.join(tmpdir, f"test_db.{file_type}")


@pytest.fixture
def repository(request, temp_db_path):
    repo_class = request.param  # get repository class
    return repo_class(temp_db_path, MockLogger())


@pytest.mark.parametrize(("repository", "temp_db_path"), [
    (JsonlRepository, "jsonl"),
    (ExcelRepository, "xlsx"),
    (SqlRepository, "db")
], indirect=True)
def test_insert(repository, temp_item):
    # given
    item = temp_item

    # when
    inserted_item = repository.insert(item)

    # then
    assert inserted_item == item


@pytest.mark.parametrize(("repository", "temp_db_path"), [
    (JsonlRepository, "jsonl"),
    (ExcelRepository, "xlsx"),
    (SqlRepository, "db")
], indirect=True)
def test_get_first_when_item_exists(repository, temp_item):
    # given
    item = temp_item
    repository.insert(item)

    # when
    first_item = repository.get_first_or_default({"id": item["id"] })

    # then
    assert first_item is not None
    assert first_item == item


@pytest.mark.parametrize(("repository", "temp_db_path"), [
    (JsonlRepository, "jsonl"),
    (ExcelRepository, "xlsx"),
    (SqlRepository, "db")
], indirect=True)
def test_update_exists_item(repository, temp_item):
    item = temp_item
    repository.insert(item)

    # given
    item_to_update = item.copy()
    item_to_update["name"] = "new name"

    # when
    updated_item = repository.update(item_to_update, {"id": item["id"]})
    print(f"before update: {item}")
    print(f"after update: {updated_item}")
    # then
    assert not item['name'] == updated_item['name']