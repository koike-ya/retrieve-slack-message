# retrieve-slack-message
slackのWeb APIからメッセージを取得する

## word cloud 環境構築
Anaconda環境がインストールされているとする。
1. pythonの実行環境を構築
```
conda create -n myslack python=3.7
conda activate myslack
```

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