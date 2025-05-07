from time import sleep
from interfaces.logger import ILogger
from interfaces.repository import IDataAccessRepository
from interfaces.web_scrapper import IWebScrapper
from accessdata.jsonl_repository import JsonlRepository
from accessdata.sql_repository import SqlRepository
from accessdata.xlsx_repository import ExcelRepository
from business_logic.app_settings import AppSettings
from business_logic.ikea_scrapper import IkeaScrapper
from services.log_service import ConsolLoger, FileLogger


def main():
    scrapper: IWebScrapper
    logger: ILogger
    repository: IDataAccessRepository

    settings = AppSettings("config.json")

    if settings.log_level == "DEBUG":
        logger = ConsolLoger(settings.log_level)
    else:
        logger = FileLogger(settings.logs_dir, settings.log_level)

    ext = settings.db_path.split(".")[-1].lower()
    if ext == "jsonl":
        repository = JsonlRepository(settings.db_path, logger)
    elif ext == "xlsx":
        repository = ExcelRepository(settings.db_path)
    elif ext == "db":
        repository = SqlRepository(settings.db_path)
    else:
        msg = f"Unsupported database file: .{ext}"
        logger.log_error(msg)
        raise ValueError(msg)

    scrapper = IkeaScrapper(settings.scrape_url, logger)
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
