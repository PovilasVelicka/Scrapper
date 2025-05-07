from abc import ABC, abstractmethod
from typing import Self


class ILogger(ABC):
    """
    Interface for logging messages at various severity levels.

    This abstract base class defines a standardized logging contract for use
    throughout the application. Implementations should handle how and where
    log messages are recorded (e.g., console, file, remote service).

    Each method logs a message at a specific level and returns the logger
    instance itself to support method chaining.
    """

    @abstractmethod
    def log_debug(self, message: str) -> Self:
        """Logs a debug-level message (typically used for development and diagnostics)."""
        pass

    @abstractmethod
    def log_info(self, message: str) -> Self:
        """Logs an informational message (general operational messages)."""
        pass

    @abstractmethod
    def log_warning(self, message: str) -> Self:
        """Logs a warning (something unexpected, but not necessarily an error)."""
        pass

    @abstractmethod
    def log_error(self, message: str) -> Self:
        """Logs an error message (something went wrong but the application can continue)."""
        pass

    @abstractmethod
    def log_critical(self, message: str) -> Self:
        """Logs a critical error (a serious failure, possibly requiring immediate attention)."""
        pass
