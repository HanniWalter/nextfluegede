import rabbitmqConnection as rmqc
import redis

searches = []
conn = rmqc.RabbitMQConnection()

def registerSearch(search):
    #register search in db
    #listen for results
    #push search to rabbitmq

    pass

def getSearchResults(search):
    #check if user is already/ still registereds
    #check if there are all resluts for one the one userid
    #return results

    pass

def callback_Searchfound(ch, method, properties, body):
    #get every intresting user ids
    #add to interessting user ids
    pass