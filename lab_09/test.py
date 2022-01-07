import json
import os
import time
from pprint import pprint
from typing import Callable

import requests
import matplotlib.pyplot as plt

cached_x = []
x = []

HOST = 'http://localhost:8080'
STATS = f'stats.rests'
ORDERS = f'orders'

# STATS_CACHED = f'{STATS}?cached=true'
#
#
# CURL = 'curl -w "@curl-format.txt" -o /dev/null'
# CONTENT_TYPE_HEADER = """-H 'Content-Type: application/json'"""
# CURL_GET = f'{CURL} -X GET'
# CURL_POST = f'{CURL} -X POST {CONTENT_TYPE_HEADER}'
# CURL_PATCH = f'{CURL} -X PATCH {CONTENT_TYPE_HEADER}'
# CURL_DELETE = f'{CURL} -X DELETE'

#
# def bench_request(req: str) -> float:
#     start = time.time()
#     os.system(req)
#     return time.time() - start


def bench_req_func(func: Callable) -> float:
    start = time.time()
    func()
    return time.time() - start


def stats_request_wrapper(cached: bool):
    url = f'{HOST}/{STATS}'
    return requests.get(url, params={'cached': cached})


def stats_request_handle():
    x.append(bench_req_func(lambda: stats_request_wrapper(False)))
    # x.append(bench_request(f"{CURL_GET} '{HOST}/{STATS}'"))


def stats_request_cached_handle():
    cached_x.append(bench_req_func(lambda: stats_request_wrapper(True)))
    # cached_x.append(bench_request(f"{CURL_GET} '{HOST}/{STATS_CACHED}'"))


def ins_query():
    url = f'{HOST}/{ORDERS}'

    data = {
        "customer_id": 1,
        "employee_id": 1,
        "restaurant_id": 1,
        "dst_address": 1,
        "src_address": 1,
        "products": [{"product_id": 1, "amount": 3}, {"product_id": 2, "amount": 2}]
    }

    # cached_x.append(bench_request(f"""{CURL_POST} -d '{json.dumps(data)}' '{HOST}/{ORDERS}'"""))
    requests.post(url, json=data)


def upd_query(order_id: int):
    url = f'{HOST}/{ORDERS}'

    data = {
        "id": order_id,
        "dst_address": 2
    }

    requests.patch(url, json=data)

    # cached_x.append(bench_request(f"{CURL_PATCH} -d '{data}' '{HOST}/{ORDERS}'"))


def del_query(order_id: int):
    url = f'{HOST}/{ORDERS}'

    requests.delete(url, params={'id': order_id})
    # cached_x.append(bench_request(f"{CURL_DELETE} '{HOST}/{ORDERS}?id={order_id}'"))


def process():
    global cached_x, x
    cached_x = []
    x = []
    for i in range(120):
        print(f'{round(i/120*100, 2)}%')
        if i % 5 == 0:
            stats_request_cached_handle()
            stats_request_handle()
            time.sleep(1)

    plt.plot(range(len(x)), x, label='Requests')
    plt.plot(range(len(cached_x)), cached_x, label='Cached requests')
    plt.legend()
    plt.savefig('graph_reg.png')

    plt.clf()


def process_ins():
    global cached_x, x
    cached_x = []
    x = []
    for i in range(120):
        print(f'{round(i/120*100, 2)}%')
        if i % 5 == 0:
            stats_request_cached_handle()
            stats_request_handle()
            time.sleep(1)

        if i % 10 == 0:
            ins_query()

    plt.plot(range(len(x)), x, label='Requests')
    plt.plot(range(len(cached_x)), cached_x, label='Cached requests')
    plt.legend()
    plt.savefig('graph_ins.png')

    plt.clf()


def process_update(val):
    global cached_x, x
    cached_x = []
    x = []
    for i in range(120):
        print(f'{round(i/120*100, 2)}%')
        if i % 5 == 0:
            stats_request_cached_handle()
            stats_request_handle()
            time.sleep(1)

        if i % 10 == 0:
            upd_query(val)
            val += 1

    plt.plot(range(len(x)), x, label='Requests')
    plt.plot(range(len(cached_x)), cached_x, label='Cached requests')
    plt.legend()
    plt.savefig('graph_upd.png')

    plt.clf()


def process_delete(val):
    global cached_x, x
    cached_x = []
    x = []
    for i in range(120):
        print(f'{round(i/120*100, 2)}%')
        if i % 5 == 0:
            stats_request_cached_handle()
            stats_request_handle()
            time.sleep(1)

        if i % 10 == 0:
            del_query(val)
            val += 1

    plt.plot(range(len(x)), x, label='Requests')
    plt.plot(range(len(cached_x)), cached_x, label='Cached requests')
    plt.legend()
    plt.savefig('graph_del.png')

    plt.clf()


if __name__ == "__main__":
    VAL = 100038

    process()
    process_ins()
    process_update(VAL)
    process_delete(VAL)
