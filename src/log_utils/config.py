"""
Config file for my logger. Supresses many 3rd party logs.
"""

import logging

def setup_logging(debug: bool = False):
    """Setup logging in the main/root module."""
    level = logging.DEBUG if debug else logging.INFO

    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("stanza").setLevel(logging.ERROR)
    logging.getLogger("stanza").handlers.clear()
    logging.getLogger("stanza").propagate = False
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("piper").setLevel(logging.WARNING)
    logging.getLogger("argostranslate.utils").setLevel(logging.WARNING)
    logging.getLogger("faster_whisper").setLevel(logging.WARNING)
