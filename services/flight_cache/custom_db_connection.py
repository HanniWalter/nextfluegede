import redis
import json
import datetime
import random
from redis.commands.json.path import Path


def get_redis_client(db):
    redis_host = 'localhost'
    redis_port = 6379
    redis_db = 0
    return redis.StrictRedis(host=redis_host, port=redis_port, db=db, password=None)


results_parent_db = get_redis_client(0)
results_child_db = get_redis_client(1)


def cleanup(key):
    now = datetime.datetime.now().timestamp()

    # get all results
    dead_results = results_parent_db.zrangebyscore(key, 0, now)
    results_parent_db.zpopmin(key, len(dead_results))


def set_parent_db_expiration(parameter_hash):
    last_entry = results_parent_db.zrevrange(
        parameter_hash, -1, -1, withscores=True)
    if last_entry == []:
        return
    last_entry = last_entry[0][1]
    partentexpire = datetime.datetime.fromtimestamp(last_entry)
    results_parent_db.expireat(parameter_hash, partentexpire)


def add_data(data):
    parameter_hash = data["parameter-hash"]
    cleanup(parameter_hash)

    key_existed = True
    if not results_parent_db.exists(parameter_hash):
        # create empty ordered set
        key_existed = False

    for result in data["results"]:
        data_expiration = datetime.datetime.strptime(result["expiration-time"],
                                                     "%Y-%m-%dT%H:%M:%S.%f")
        # get free key in child db
        result_key = result["id"]
        # add result to child db
        results_child_db.set(result_key, json.dumps(result))
        results_child_db.expireat(result_key, data_expiration)
        # add result to parent db

        sec = data_expiration.timestamp()
        results_parent_db.zadd(parameter_hash, {result_key: sec})
        # set expiration date
        if not key_existed:
            results_parent_db.expireat(parameter_hash, data_expiration)
            key_existed = True
    set_parent_db_expiration(parameter_hash)


def get_data(parameter_hash):
    now = datetime.datetime.now().timestamp()

    # get all results
    results = []
    raw_results = results_parent_db.zrangebyscore(
        parameter_hash, now, float("inf"))
    for result in raw_results:
        result = results_child_db.get(result)
        if result is not None:
            results.append(json.loads(result))

    cleanup(parameter_hash)
    return results


def delete_specific_result(parameter_hash, result):
    id = result["id"]
    results_parent_db.zrem(parameter_hash, id)
    results_child_db.delete(id)


if __name__ == "__main__":
    # read testdata
    with open("services/flight_cache/testdata/test.json") as f:
        results = json.load(f)
    results["expiration-time"] = datetime.datetime.now() + \
        datetime.timedelta(minutes=2)
    results["expiration-time"] = results["expiration-time"].strftime(
        "%Y-%m-%dT%H:%M:%S.%f")
    add_data(results)
    print(get_data(results["parameter-hash"]))
