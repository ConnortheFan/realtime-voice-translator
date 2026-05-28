import time
import logging
from functools import wraps

def log_calls(func):
    logger = logging.getLogger(func.__module__)

    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.debug("ENTER %s", func.__qualname__)

        start = time.perf_counter()

        try:
            result = func(*args, **kwargs)
            return result
        
        except Exception:
            logger.debug("ERROR in %s", func.__qualname__)
            raise

        finally:
            elapsed = time.perf_counter() - start
            logger.debug("EXIT %s (%.3fs)", func.__qualname__, elapsed)


    return wrapper