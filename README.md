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
# 初回起動の場合
# $ python manage.py migrate
$ python manage.py runserver
```

### Boxアプリの情報を登録

* ホストで実行

```shell
$ docker-compose exec db bash 
```

* ゲスト（Docker）で実行

```shell
$ psql --username admin --dbname poc
```

```sql
insert into box_config (app_environment, app_client_id, app_secret, create_dt, update_dt) values
('develop', 'YOUR_CLIENT_ID', 'YOUR_CLIENT_SECRET', now(), now());
commit;
-- box_configテーブルのapp_environmentには環境ごとに下記の値を指定する
-- develop: 開発環境
-- st: システムテストなどの環境
-- production: 本番環境
-- →現在の環境の制御は、my_box_project/settings.pyのAPP_ENVIRONMENTで設定(現在はdevelopが設定されている)
```



### 以下のURLにアクセス

```http://localhost:8000/box_api```
