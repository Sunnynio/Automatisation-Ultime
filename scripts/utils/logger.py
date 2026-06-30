import logging
import os

_level = logging.DEBUG if os.getenv("DEBUG") else logging.INFO

logging.basicConfig(
    level=_level,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)

logger = logging.getLogger("automatisation_ultime")
