import rabbitmqConnection as rmqc
import redis
import requests
import json

searches = []
rmq = rmqc.RabbitMQConnection()


def redisConnection(db):
    dbdict = {"uid_searches": 0, "hash_uid": 1,
              "uidxhash_sources": 2, "raw_flights": 3, "uidxhash_priced_results": 4}

    r = redis.Redis(host='localhost', port=6379, db=dbdict[db])
    return r


def registerSearch(search):
    response = requests.post("http://localhost:5110/hash",
                             json=search)
    search["parameter-hash"] = response.json()["hash"]
    # register search in db
    db = redisConnection("uid_searches")
    db.rpush(search["user-id"], json.dumps(search))
    db.expire(search["user-id"], 5*60)

    db2 = redisConnection("hash_uid")
    db2.rpush(search["parameter-hash"], search["user-id"])
    db2.expire(search["parameter-hash"], 5*60)
    # listen for results
    # todo

    # push search to rabbitmq
    rmq.publish_search(search)
    print("published search")


def isSearchResultInDB(search):
    response = requests.post("http://localhost:5110/hash",
                             json=search)
    parameter_hash = response.json()["hash"]
    uid = search["user-id"]
    db = redisConnection("uidxhash_priced_results")
    key = str(uid) + ":" + str(parameter_hash)
    result = db.get(key)
    if result is None:
        return False
    else:
        return True


def getSearchResults(search):
    response = requests.post("http://localhost:5110/hash",
                             json=search)
    parameter_hash = response.json()["hash"]
    uid = search["user-id"]
    db = redisConnection("uidxhash_priced_results")
    key = str(uid) + ":" + str(parameter_hash)
    result = db.get(key)
    return result
