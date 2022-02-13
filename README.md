
Set up virtual venv

pip3 install -r requirements.txt

Set up database variables
export 'DB_NAME' = <database table name>
export 'DB_USER' = <database table user>
export 'DB_PASSWORD' = <database table password>
export 'DB_HOST' = <database table host (default localhost)>
export 'DB_PORT' = <database table name (default 3306)>


python manage.py runserver

python manage.py test

./manage.py loaddata fixture UserWalletsApp/fixtures/fixture.json
