import os
from enum import Enum
import requests
from tqdm import tqdm


TOKEN = os.environ['SLACK_MESSAGE_SLACK_TOKEN']


class RequestType(Enum):
    CHANNELS = 1
    HISTORY = 2
    JOIN = 3


def _request_slack_api(request_type: RequestType,
                       payload: dict = {},
                       ):
    if request_type == RequestType.CHANNELS:
        url = "https://slack.com/api/conversations.list"
        payload["limit"] = "1000"
    elif request_type == RequestType.HISTORY:
        url = "https://slack.com/api/conversations.history"
    elif request_type == RequestType.JOIN:
        url = "https://slack.com/api/conversations.join"

    header = {
        "Authorization": "Bearer {}".format(TOKEN)
    }

    res = requests.get(url, headers=header, params=payload)
    return res.json()


def _retrieve_slack_api(request_type: RequestType,
                        payload: dict = {},
                        ):
    res = []
    res.append(_request_slack_api(request_type, payload))
    if not res[-1]['ok']:
        print(res)
        return []

    while res[-1].get('has_more'):
        payload['cursor'] = res[-1]['response_metadata']['next_cursor']
        res.append(_request_slack_api(request_type, payload))

    return res


def retrieve_channel_history(channel_id, latest_ts=0):
    messages = []
    payload = {
        "channel": channel_id,
        "limit": 200,
        "oldest": latest_ts
    }

    res_list = _retrieve_slack_api(RequestType.HISTORY, payload)
    [messages.extend(res['messages']) for res in res_list if res]
    return messages


def retrieve_all_channels():
    res_list = _retrieve_slack_api(RequestType.CHANNELS)
    channels = []
    [channels.extend(res['channels']) for res in res_list]
    return channels


def join_all_channels(channels):
    for channel in tqdm(channels):
        channel_id = channel['id']
        payload = {
            'channel': channel_id
        }
        _request_slack_api(RequestType.JOIN, payload)


def retrieve_conversation_history(retrieval_history_client, data_client, channels):
    for channel in tqdm(channels):
        channel_id = channel['id']
        latest_ts_channel = retrieval_history_client.find_latest_history_ts(
            channel_id)
        latest_ts = latest_ts_channel.get('ts', 0) if latest_ts_channel else 0
        messages = retrieve_channel_history(channel_id, latest_ts)

        if messages:
            for message in messages:
                message['channel_id'] = channel_id
            data_client.insert(messages, 'history')
            messages.sort(key=lambda message: message['ts'])
            latest_ts = messages[-1]['ts']
            retrieval_history_client.update_history_ts(channel_id, latest_ts)


def _retrieve_replies(channel_id, thread_ts, latest_reply_ts=0):
    messages = []
    payload = {
        "channel": channel_id,
        "ts": thread_ts,
        "oldest": latest_reply_ts,
        "limit": 200,
    }

    res_list = _retrieve_slack_api(RequestType.HISTORY, payload)
    [messages.extend(res['messages']) for res in res_list if res]
    return messages


def retrieve_conversation_reply(retrieval_history_client, data_client, channels):
    for channel in tqdm(channels):
        channel_id = channel['id']
        messages = retrieve_channel_history(channel_id)

        for message in messages:
            thread_ts = message['ts']
            latest_ts_history = retrieval_history_client.find_latest_reply_ts(
                channel_id, thread_ts)
            latest_reply_ts = latest_ts_history.get(
                'ts', 0) if latest_ts_history else 0

            thread_messsages = _retrieve_replies(
                channel_id, thread_ts, latest_reply_ts)
            if thread_messsages:
                for thread_messsage in thread_messsages:
                    thread_messsage['channel_id'] = channel_id
                data_client.insert(thread_messsages, 'reply')
                thread_messsages.sort(key=lambda m: m['ts'])
                latest_ts = thread_messsages[-1]['ts']
                retrieval_history_client.update_reply_ts(
                    channel_id, thread_ts, latest_ts)
