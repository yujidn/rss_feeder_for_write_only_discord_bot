import hashlib
import json
import os

import feedparser

cache_dir = "cache"


def load_last_entry(url: str) -> dict:
    entry = {}
    filename = get_filepath(url)
    if os.path.exists(filename):
        with open(filename, "r") as f:
            entry = json.load(f)
    return entry


def store_last_entry(url: str, entry: dict) -> None:
    if os.path.exists(cache_dir) is False:
        os.mkdir(cache_dir)

    filename = get_filepath(url)
    with open(filename, "w") as f:
        json.dump(entry, f)


def get_filepath(url: str) -> str:
    hashed_url = hashlib.md5(url.encode()).hexdigest()
    return f"{os.path.join(cache_dir, hashed_url)}.json"


def get_feed(url: str) -> dict:
    try:
        feed = feedparser.parse(url)
        new_entry = {
            "title": getattr(feed.entries[0], "title", ""),
            "link": getattr(feed.entries[0], "link", ""),
            "tags": [tag.term for tag in getattr(feed.entries[0], "tags", [])],
        }
    except Exception as e:
        print(f"An error occurred while fetching the feed: {e}")
        return {}

    return new_entry


def check_feed(url: str) -> dict:
    new_entry = get_feed(url)
    if new_entry == {}:
        return {}

    last_entry = load_last_entry(url)
    if new_entry != last_entry:
        store_last_entry(url, new_entry)

        return new_entry

    return {}
