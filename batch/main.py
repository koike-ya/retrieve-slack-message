import slack
import mongo as mongo_client
import bigquery as bq_client


if __name__ == '__main__':
    channels = slack.retrieve_all_channels()
    slack.join_all_channels(channels)
    slack.retrieve_conversation_history(bq_client, mongo_client, channels)
    slack.retrieve_conversation_reply(bq_client, mongo_client, channels)
