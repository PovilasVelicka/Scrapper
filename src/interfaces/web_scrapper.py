from abc import ABC, abstractmethod
from typing import Generator

class IWebScrapper(ABC):
    @abstractmethod
    def page_items(self) -> Generator[dict, None, None]:
        """
        Yields all items found by iterating through paginated product pages.
        :return: A generator that yields dictionaries, each representing a scraped product item.
        """
        pass

    @abstractmethod
    def clear_state(self):
        """
        Clears any internal saved state used for tracking progress.

        This method is typically used to reset pagination or previously stored
        position markers so that the process can start fresh the next time it's run.
        Implementations may delete a file, reset a database record, or clear in-memory data.
        """
        pass

    @abstractmethod
    def is_completed(self) -> bool:
        """
        Checks if the scraping process has completed.

        Implementations may track whether all pages have been processed,
        all items have been retrieved, or whether a stopping condition has been met.

        :return: True if the scraping process is finished, False otherwise.
        """
        pass
