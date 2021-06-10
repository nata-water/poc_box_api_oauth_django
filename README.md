### モジュールのインストール

```shell
$ pip install pipenv
$ pipenv install
```

### 各サーバー起動

* DBサーバ

```shell
$ docker-compose up -d
# or
# docker compose up -d
```

* Django APサーバ

```shell
$ pipenv shell
# 初回起動の場合
# $ python manage.py migrate
$ python manage.py runserver
```

### Boxアプリの情報を登録

```sql
insert into box_config (app_environment, app_client_id, app_secret, create_dt, update_dt) values
('develop', 'YOUR_CLIENT_ID', 'YOUR_CLIENT_SECRET', now(), now())
-- box_configテーブルのapp_environmentには環境ごとに下記の値を指定する
-- develop: 開発環境
-- st: システムテストなどの環境
-- production: 本番環境
-- →現在の環境の制御は、my_box_project/settings.pyのAPP_ENVIRONMENTで設定(現在はdevelopが設定されている)
```



### 以下のURLにアクセス

```http://localhost:8000/box_api```


### 備忘録

#### Box Python SDKのドキュメント
    * https://box-python-sdk.readthedocs.io/en/latest/index.html

#### リフレッシュトークンの利用について（確証はまだない）

* おそらく、コンテキストプロセッサーで、各リクエスト処理にアクセストークンの検証処理を差し込むイメージ。
  *  リクエスト時にアクセストークンの有効期限(1時間)が切れていなかった場合
      * -> セッションのアクセストークンで各ページからBox APIを呼ぶ
  * リクエスト時にアクセストークンの有効期限(1時間)が切れていた場合
    * リクエスト失敗をハンドリング
    * リフレッシュトークンの期限を検証し、発行日(?)から60日以内であれば、リフレッシュトークンを元にアクセストークンを再度取得する
