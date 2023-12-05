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
    db.rpush(search["user-id"], search)
    db.expire(search["user-id"], 5*60)

    # listen for results
    # todo

    # push search to rabbitmq
    rmq.publish_search(search)
    print("published search")


# list of providers
providers = ["travelfusion", "amadeus", "bing"]


def registerPricedResult(body):
    key = body["user-id"] + ":" + body["parameter-hash"]
    db = redisConnection("uidxhash_priced_results")
    db.set(key, json.dumps(body))


def registerResult(body):
    hash = body["parameter-hash"]
    db0 = redisConnection("uid_searches")
    db = redisConnection("hash_uid")
    db2 = redisConnection("uidxhash_sources")
    db3 = redisConnection("raw_flights")
    # get intersting user ids
    user_ids = db.lrange(hash, 0, -1)

    if body["results-origin"] == "cache":
        for provider in body["results-provider-name"]:
            for user_id in user_ids:
                user_idxhash = str(user_id)+":"+str(hash)

                db2.sadd(user_idxhash, provider)
                db2.expire(user_idxhash, 5*60)
    elif body["results-origin"] == "provider":
        provider = body["results-provider-name"][0]
        for user_id in user_ids:
            user_idxhash = str(user_id)+":"+str(hash)
            db2.sadd(user_idxhash, provider)
            db2.expire(user_idxhash, 5*60)

    # add data to db
    if body["results"]["result"] != []:
        for user_id in user_ids:
            results = [json.dumps(result)
                       for result in body["results"]["result"]]
            db3.rpush(str(user_id)+":"+str(hash), *results)
            db3.expire(str(user_id)+":"+str(hash), 5*60)

    # check if every provider is in user ids
    for user_id in user_ids:
        user_idxhash = str(user_id)+":"+str(hash)
        if len(db2.smembers(user_idxhash)) == len(providers):
            print("all providers are in")
            # get all results
            results = db3.lrange(user_idxhash, 0, -1)
            results = [json.loads(result) for result in results]
            # get search:
            searches = db0.lrange(user_id, 0, -1)
            for search in searches:
                search = json.loads(search)
                if search["parameter-hash"] == hash:
                    rmq.publish_results_for_pricer(
                        search=search, results=results)
                    break
            db2.sadd(user_idxhash, "locked")
