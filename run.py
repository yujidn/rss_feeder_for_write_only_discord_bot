import json
import os

import requests
import yaml

import rss_feeder

os.chdir(os.path.dirname(os.path.abspath(__file__)))
# with open("feed_list.yaml") as f:
#     feed_list = yaml.safe_load(f)

# secret gist のraw urlから取得している
res = requests.get(url=os.environ.get("RSS_LIST"))
feed_list = yaml.safe_load(res.text)


def socket_communication(chid: int, data: dict, prefix: str):
    import socket

    # ホストとポートを指定
    HOST = "localhost"
    PORT = 12345

    # ソケットを作成
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    client_socket.sendall(bytes(json.dumps({"id": chid, "data": data, "prefix": prefix}), "utf-8"))
    client_socket.close()


for feed in feed_list:
    ch_id = feed["ch_id"]
    urls = feed["urls"]
    for url in urls:
        url = url["url"]
        new_entries = rss_feeder.check_feed(url)
        new_entries.reverse()
        for entry in new_entries:
            socket_communication(ch_id, entry)
