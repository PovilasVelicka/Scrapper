from time import sleep
from src.interfaces.logger import ILogger
from src.interfaces.repository import IDataAccessRepository
from src.interfaces.web_scrapper import IWebScrapper
from src.accessdata.jsonl_repository import JsonlRepository
from src.accessdata.sql_repository import SqlRepository
from src.accessdata.xlsx_repository import ExcelRepository
from src.business_logic.app_settings import AppSettings
from src.business_logic.ikea_scrapper import IkeaScrapper
from src.services.log_service import Logger


def main():
    settings = AppSettings("config.json")
    scrapper: IWebScrapper
    logger: ILogger = Logger("main_app", settings.log_level)
    repository: IDataAccessRepository
    ext = settings.db_path.split(".")[-1].lower()
    if ext == "jsonl":
        repository = JsonlRepository(settings.db_path, Logger("JsonlRepository",settings.log_level))
    elif ext == "xlsx":
        repository = ExcelRepository(settings.db_path)
    elif ext == "db":
        repository = SqlRepository(settings.db_path)
    else:
        msg = f"Unsupported database file: .{ext}"
        logger.log_error(msg)
        raise ValueError(msg)

    scrapper = IkeaScrapper(settings.scrape_url, Logger("IkeaScrapper", settings.log_level))
    complete = False
    while not complete:
        try:
            for i in scrapper.page_items():
                if repository.get_first_or_default(i):
                    repository.update(i, {"id": i["id"]})
                else:
                    repository.insert(i)
            logger.log_info(f"The page {settings.scrape_url} successfully scrapped into {settings.db_path}")
            scrapper.clear_state()
            complete = True
        except KeyboardInterrupt:
            logger.log_error(f"Interrupted by user!")
            complete = True
        except Exception as e:
            logger.log_error(f"Unexpected error: {e}")
            logger.log_info(f"Waiting 10 seconds")
            sleep(10)


if __name__ == "__main__":
    main()
