import os

from ..logging import LOGGER


def dirr():
    for file in os.listdir():
        if file.endswith(".jpg"):
            os.remove(file)
        elif file.endswith(".jpeg"):
            os.remove(file)
        elif file.endswith(".png"):
            os.remove(file)

BASE_DIR = os.getcwd()
DOWNLOAD_DIR = os.path.join(BASE_DIR, "downloads")
CACHE_DIR = os.path.join(BASE_DIR, "cache")

# All of these must start at the very beginning of the line (no spaces)
os.makedirs(DOWNLOAD_DIR, exist_ok=True)
os.makedirs(CACHE_DIR, exist_ok=True)

if "downloads" not in os.listdir():
    os.mkdir("downloads")
if "cache" not in os.listdir():
    os.mkdir("cache")

LOGGER(__name__).info("Directories Updated.")