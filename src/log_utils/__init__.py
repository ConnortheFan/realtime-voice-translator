"""
Setup log_utils as a package.
"""

import logging as _logging
from .config import setup_logging
from .decorator import log_calls

# Re-export main tools for users to use:
# from log_utils import setup_logging, log_calls
__all__ = ["setup_logging", "log_calls", "get_logger"]

def get_logger(name: str | None = None):
    """
    Returns a configured logger.

    If name is None, uses root logger.
    """
    return _logging.getLogger(name)
