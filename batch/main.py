import sys
import os
import json


if __name__ == '__main__':
    # 標準入力をそのまま環境変数に入れるの、セキュリティ的にリスクありそう
    os_env_path = sys.argv[1]
    with open(os_env_path, 'r') as f:
        os_env_dict = json.load(f)
    # slackやmongoのファイルで使う環境変数を先に入れておく必要がある
    os.environ.update(os_env_dict)

    import slack
    import mongo as mongo_client
    import bigquery as bq_client
    from json_file import JsonlineClient

    channels = slack.retrieve_all_channels()
    # jsonl_client = JsonlineClient(dir_path=Path(__file__).resolve().parent)
    slack.join_all_channels(channels)
    slack.retrieve_conversation_history(mongo_client, bq_client, channels)
    slack.retrieve_conversation_reply(mongo_client, bq_client, channels)
