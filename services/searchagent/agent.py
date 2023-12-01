import rabbitmqConnection as rmqc
import redis
import requests

searches = []
rmq = rmqc.RabbitMQConnection()


def redisConnection(db):
    dbdict = {"searches": 0, "results": 1}

    r = redis.Redis(host='redis', port=6379, db=dbdict[db])
    return r


def registerSearch(search):
    print(search)
    headers = {'Content-Type': 'application/json'}
    response = requests.post("http://localhost:5110/hash",
                             json=search)
    search["parameter-hash"] = response.json()["hash"]
    # register search in db
    db = redisConnection("searches")
    db.rpush(search["user-id"], search)
    db.expire(search["parameter-hash"], 5*60)

    # listen for results
    # todo

    # push search to rabbitmq
    rmq.publish_search(search)
    print("published search")


def getSearchResults(search):
    # check if user is already/ still registereds
    # check if there are all resluts for one the one userid
    # return results

    pass


def callbackSearchfound(ch, method, properties, body):
    # get every intresting user ids
    # add to interessting user ids
    pass
