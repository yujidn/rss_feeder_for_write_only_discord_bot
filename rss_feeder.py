import hashlib
import json
import os
import typing

import feedparser

cache_dir = "cache"


def load_old_entries(url: str) -> typing.List[dict]:
    entries = []
    filename = get_filepath(url)
    if os.path.exists(filename):
        with open(filename, "r") as f:
            entries = json.load(f)
    return entries


def store_old_entries(url: str, entries: typing.List[dict]) -> None:
    if os.path.exists(cache_dir) is False:
        os.mkdir(cache_dir)

    filename = get_filepath(url)
    with open(filename, "w") as f:
        json.dump(entries, f)


def get_filepath(url: str) -> str:
    hashed_url = hashlib.md5(url.encode()).hexdigest()
    return f"{os.path.join(cache_dir, hashed_url)}.json"


def get_feed(url: str) -> typing.List[dict]:
    try:
        feed = feedparser.parse(url)

        entries = []
        # 10件まで取得
        for entry in feed.entries[:10]:
            entries.append(
                {
                    "title": getattr(entry, "title", ""),
                    "link": getattr(entry, "link", ""),
                    "tags": [tag.term for tag in getattr(entry, "tags", [])]
                    if hasattr(entry, "tags")
                    else [],
                }
            )

    except Exception as e:
        print(f"An error occurred while fetching the feed: {e}")
        return entries

    return entries


def check_feed(url: str) -> typing.List[dict]:
    entries = get_feed(url)
    if len(entries) == 0:
        return []

    old_entries = load_old_entries(url)

    new_entries = []
    for entry in entries:
        flg = True
        for ol in old_entries:
            if entry == ol:
                flg = False
                break
        if flg:
            new_entries.append(entry)
        else:
            break
    if len(new_entries) > 0:
        store_old_entries(url, old_entries + new_entries)

    return new_entries
