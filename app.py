import os
from sys import exit
from time import sleep
from dotenv import load_dotenv
from typing import Optional
from src.interfaces.logger import ILogger
from src.interfaces.repository import IDataAccessRepository
from src.interfaces.web_scrapper import IWebScrapper
from src.interfaces.mail_service import IMailService
from src.accessdata.jsonl_repository import JsonlRepository
from src.accessdata.sql_repository import SqlRepository
from src.accessdata.xlsx_repository import ExcelRepository
from src.business_logic.app_settings import AppSettings
from src.business_logic.ikea_scrapper import IkeaScrapper
from src.services.log_service import Logger
from src.services.mail_service import GmailService


def main():
    settings = AppSettings("config.json")
    scrapper: IWebScrapper
    logger: ILogger = Logger("main_app", settings.log_level)
    repository: IDataAccessRepository
    mail_service: Optional[IMailService] = None
    ext = settings.db_path.split(".")[-1].lower()

    # select repository object by database file extension
    if ext == "jsonl":
        repository = JsonlRepository(settings.db_path, Logger("JsonlRepository", settings.log_level))
    elif ext == "xlsx":
        repository = ExcelRepository(settings.db_path, Logger("ExcelRepository", settings.log_level))
    elif ext == "db":
        repository = SqlRepository(settings.db_path, Logger("SqlRepository", settings.log_level))
    else:
        msg = f"Unsupported database file: .{ext}"
        logger.log_error(msg)
        raise ValueError(msg)

    # create mail service object, get credentials from .env file
    load_dotenv()
    gmail_user = os.getenv("GMAIL_USERNAME")
    gmail_password = os.getenv("GMAIL_APP_PASSWORD")
    if gmail_user and gmail_password:
        mail_service = GmailService(gmail_user, gmail_password, Logger("GmailService", settings.log_level))

    # create scrapper object
    scrapper = IkeaScrapper(settings.scrape_url, Logger("IkeaScrapper", settings.log_level))

    # process page until all items will scrap
    while not scrapper.is_completed:
        try:
            for i in scrapper.page_items():
                if repository.get_first_or_default(i):
                    repository.update(i, {"id": i["id"]})
                else:
                    repository.insert(i)
            success_message = f"The page {settings.scrape_url} successfully scrapped into {settings.db_path}"
            logger.log_info(success_message)
            scrapper.clear_state()
            if mail_service:
                mail_service.send_email(settings.email_recipient, "Scrapper", success_message)
        except KeyboardInterrupt:
            interrupt_message = f"Interrupted by user!"
            logger.log_error(interrupt_message)
            if mail_service:
                mail_service.send_email(settings.email_recipient, "Scrapper", interrupt_message)
            exit()
        except Exception as e:
            logger.log_error(f"Unexpected error: {e}")
            logger.log_info(f"Waiting 10 seconds")
            sleep(10)


if __name__ == "__main__":
    main()
