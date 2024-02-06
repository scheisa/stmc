from copy import deepcopy
from  re import sub
from dataclasses import dataclass
from miniflux import Client, ClientError
from requests import get
from requests.exceptions import MissingSchema, HTTPError
from markdownify import markdownify
from time import sleep

from utils import parse_config, die
from ui import ui_init

@dataclass
class Entry:
    title: str
    content: str
    url: str
    created: str
    id_: int

@dataclass
class Category:
    title: str
    c_id: int
    unread: int
    entries: list[Entry]

def get_entries(categories_list: list[Category], categories: list, client: Client) -> int:
    total_unread: int = 0

    for category in categories:
        entries_info: list[Entry] = []

        entries = client.get_entries(category_id=category['id'], status=['unread'])

        if entries == ClientError:
            die("error", "client error", 0)

        if entries['total'] > 0:
            for entry in entries['entries']:
                entry_info = Entry(
                        title = entry['title'],
                        content = entry['content'],
                        url = entry['url'],
                        created = entry['published_at'],
                        id_ = int(entry['id']))
                entries_info.append(entry_info)

            category_info = Category(
                        title = category['title'],
                        c_id = category['id'],
                        unread = entries['total'],
                        entries = deepcopy(entries_info))

            categories_list.append(category_info)

            total_unread += entries['total']

    categories_list.sort(key=lambda x: x.unread, reverse=True)

    return total_unread

def main():
    categories: list = []
    total_unread: int = 0
    categories_list: list[Category] = []

    # parsing config file
    config = parse_config()
    # parsing options
    url = config.get("instance", "url")
    api = config.get("instance", "api")

    try:
        miniflux_client = Client(url, api_key=api)
        categories = miniflux_client.get_categories();
    except (MissingSchema, ClientError) as e:
        die("error", f"unable to connect to the Miniflux instance: invalid api key or url", 0)

    total_unread = get_entries(categories_list, categories, miniflux_client)
    if total_unread == 0:
        die("info", "no items to read", 0)
 
    for category in categories_list:
        print(category.title, category.unread)

    ui_init(categories_list, total_unread)

main()
