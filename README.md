# retrieve-slack-message
slackのWeb APIからメッセージを取得する

## python実行環境の構築
Anaconda環境がインストールされているとする。
1. pythonの実行環境を構築
```
conda create -n myslack python=3.7
conda activate myslack
```

## ローカルでslackメッセージの取得、BQへのアップロードの実行
environments.jsonを小池から取得後、以下を実行
```
python batch/main.py path/to/credential.json
```

## word cloud 環境構築

2. slackのエクスポートデータを加工
slackのデータをエクスポートする。
そして以下のnotebookを実行する
```
convert_exported_slack_messages.ipynb
```

3. フォントをダウンロード
```
https://github.com/adobe-fonts/source-han-sans/raw/release/Variable/TTF/SourceHanSans-VF.ttf
```

4. 
以下のnotebookを実行
```
word_cloud.ipynb
```
