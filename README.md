# kindle wallpaper 日本語化

## TL;DR

* 古いkindle(paper white, 第5世代)を天気予報とGoogleカレンダーのイベントを表示する壁紙に  
  ![kindle wallpaper](https://ichusrlocalbin.github.io/images/posts/kindle-wallpaper/kindle-wallpaper.jpg)
* 充電は1ヵ月に1度くらい(にならないかなー、と願望。これから測定します)  
  [がんばった記録](https://github.com/ichusrlocalbin/kindle-wallpaper-jp/tree/master/docs#バッテリーとの戦い)

## 動機

* 天気予報を録画から見るの面倒。iPhoneもwithingsの体重計も天気予報の精度が悪い。
* kindleだとバッテリーをほぼ食わないから壁紙に最適
* 家族も喜ぶ
* 新しいkindleも買える!

## アーキテクチャ

* raspberry-pi: 天気予報、カレンダー取得、壁紙作成
* kindle papwer white(5th generation): raspberry-piから壁紙取得して表示

## 元のkindle-wallpaperと違う所

* 元のkinlde-wallpaper: [pjimenezmateo/kindle-wallpaper](https://github.com/pjimenezmateo/kindle-wallpaper) Thank you so much!
* 天気予報は、livedoorのAPIを使用。元となるデータは、日本気象協会っぽい。
  * 元々あった画像が少なく、無理に天気を当てはめているので、一つの画像に複数の天気が割り当てられている。
  * 詳しくは[メモ](docs/README.md)を参照
* メッセージの日本語化: 曜日とか
* 本日の予定と全日の予定との区別の廃止(予定を表示する幅が狭かったので)
* 更新時刻が朝の6時だったけど、次の日の天気予報も見たいんじゃないかと思い、日本時間の15時(UTCで6時)に変更(cronの更新時刻のコードはそのまま、天気予報は次の日のものを表示するようにした)
* google-apiを使うようになったりと細かな変更

## raspberry-piの設定

### 準備: APIの有効化

* 基本的には、[Google Calendar API Python Quickstart](https://developers.google.com/google-apps/calendar/quickstart/python) の手順に従う
* `APIを呼び出す場所` では、 `[その他のUI(Windows、CLIツールなど)]` を選択  
  (`[その他の非UI(cronジョブ、デーモンなど)]` を選択すると、ログイン操作が必要とのエラーが出る)  
* `アクセスするデータの種類` では、 `ユーザデータ` を選択
* ダウンロードした `client_id.json` は `wallpaper-server`へ移動。
* 開発環境で `create_events_image.py` を実行し、作成された `~/.credentials` ディレクトリをDockerを構築する端末のDockerfileがあるディレクトリにコピーしておく(webブラウザで認証が必要なので)

### 環境構築

個人の環境に合わせ、設定を修正

* `kindle/display_wallpaper.sh` の `WALLPAPER_SERVER`
* `wallpaper-server/programs/create_events_image.py` の `CALENDAR_ID`  
   `primary` 以外を設定する場合は、同スクリプト中の `show my carender_id list` の二つを外して、どの `CALENDAR_ID` を設定すべきか検討をつける
* `wallpaper-server/programs/create_weather_image.py` の `yql_query = 'select * from weather.forecast where woeid = 26236758 and u="c"'` の `woeid` を自分の表示したい場所に設定する。現状は、東京。woeidは、 [https://www.yahoo.com/news/weather/](https://www.yahoo.com/news/weather/) の `Change location` に郵便番号を入れて表示されるURLの末尾から取得できる。


```
$ docker build -t kindle-wallpaper .
```

### 起動

```
docker run -p 8080:80 --name kw -d kindle-wallpaper
```

### 動作確認

インストール当日、実行して、次の日の状態の画像が取得できることを確認

```
docker exec -it kw bash
./display_wallpaper.sh
exit
curl http://localhost:8080/done.png > done.png
```

次の日の15時5分以降に実行して、その次の日の状態の画像が取得できることを確認

```
curl http://localhost:8080/done.png > done.png
```

### boot時に自動起動

* 参考: https://docs.docker.com/engine/admin/host_integration/

`/etc/systemd/system/docker-kindle-wallpaper.service` を追加

```
[Unit]
Description=Kindle wallpaper container
Requires=docker.service
After=docker.service

[Service]
Restart=always
ExecStart=/usr/bin/docker run -p 8080:80 --name kindle-wallpaper kindle-wallpaper
ExecStop=/usr/bin/docker stop -t 2 kindle-wallpaper
ExecStopPost=/usr/bin/docker rm -f kindle-wallpaper

[Install]
WantedBy=default.target
```

変更時の起動

```
sudo systemctl daemon-reload
sudo systemctl start docker-kindle-wallpaper.service
```

boot時に有効化

```
sudo systemctl enable docker-kindle-wallpaper.service
```

## kindle側の設定

```
ssh root@192.168.15.244 'mkdir /mnt/us/wallpaper'
scp kindle/display_wallpaper.sh root@192.168.15.244:/mnt/us/wallpaper/
scp kindle/keep_ready_to_suspend.sh root@192.168.15.244:/mnt/us/wallpaper/
scp kindle/keep_ready_to_suspend.conf root@192.168.15.244:/etc/init/
ssh root@192.168.15.244
chmod 755 /mnt/us/wallpaper/*.sh
mntroot rw
echo '5 6 * * * /mnt/us/wallpaper/display_wallpaper.sh  >> /var/log/display_wallpaper.log' >> /etc/crontab/root
```

## 参考: kindle paper white(第5世代)のjailbreak

1. Firmwareを5.4.5にdown grade
2. jailbreak
3. bridgeをインストール
4. Firmwareを5.6.1.1にup grade
5. KUAL, Helper, MR Package installのインストール
6. USB Networkのインストール  
   sshのパスワードが設定されてないようだったので、公開鍵を入れる。
   ```
cp ~/.ssh/id_rsa.pub /Volumes/Kindle/usbnet/etc/authorized_keys
```
7. ssh 
   ```
ssh root@192.168.15.244
```
8. 書き込みが必要なとき
   ```
mntroot rw
```

### kindle jailbreak関連 参考サイト

* jailbreakの方法:  [Kindle: PW1（2012、第5世代）、5.6.1.1へ強制アップデート勧告](http://soranoji.air-nifty.com/blog/2016/03/kindle-pw120125.html) 
* 各種ツールのインストール: [Kindle：jailbreak方法（5.7.x - 5.8.1）その3 jailbreak後のツールのインストール](http://soranoji.air-nifty.com/blog/2016/07/kindlejailbre-2.html)
* jailbreak用ツールなどのダウンロード先: [http://www.mobileread.com/forums/showthread.php?t=225030](Snapshots of NiLuJe's hacks)
* paper white(第5世代)用のUSB Network (`kindle-usbnet-0.21.N.zip`) のダウンロード先 [Kindle Touch/PW1/PW2 5.0.x - 5.4.4.2 JailBreak. Plus FW 5.x USBNetwork.](http://www.mobileread.com/forums/showthread.php?t=186645)

## Licence

本家に合わせて、 [CC BY](https://creativecommons.org/licenses/by/4.0/deed.ja) で
