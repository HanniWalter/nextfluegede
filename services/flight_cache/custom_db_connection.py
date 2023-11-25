import redis
import json

def get_redis_client(db):
    redis_host = 'localhost'
    redis_port = 6379
    redis_db = 0
    return redis.StrictRedis(host=redis_host, port=redis_port, db=db)

parent_db = get_redis_client(0)
child_db = get_redis_client(1)

def cleanup(key):
    pass

def add_data(data):
    print(data.keys())
    return
    data_expiration = 0
    if parent_db.exists(data["parameter-hash"]):
        for i in range( len(data["results"])):
            child_db.sadd(data["parameter-hash"], data["results"][i])
        parent_db.set(data["parameter-hash"], data["results"])
        parent_db.expireat(data["parameter-hash"], data["expiration-date"])
    else:
        for i,result in enumerate (range(len(data["results"]))):
            pass


def get_data(parameter_hash):
    pass

def delete_specific_result(parameter_hash, result):
    pass



if __name__ == "__main__":
    #read testdata
    with open("testdata/test.json") as f:
        results = json.load(f)

    
    pass