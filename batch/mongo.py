import pymongo


MONGO_URI = "mongodb+srv://sample-user1:sample-user@cluster0.n12zp.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
client = pymongo.MongoClient(MONGO_URI).myslack


def find_latest_history_ts(channel_id):
    return client.history.find_one({"channel_id": channel_id}, sort=[('ts', -1)])


def update_history_ts(channel_id, latest_ts):
    return client.history.update_one({'channel_id': channel_id}, {'$set': {'ts': latest_ts}}, upsert=True)


def find_latest_history_ts(channel_id, thread_ts):
    return client.reply.find_one({"channel_id": channel_id, 'thread_ts': thread_ts}, sort=[('ts', -1)])


def update_reply_ts(channel_id, thread_ts, latest_ts):
    return client.reply.update_one({'channel_id': channel_id, 'thread_ts': thread_ts}, {'$set': {'ts': latest_ts}}, upsert=True)
