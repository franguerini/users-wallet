### User Wallet Python Exercise

##### Requirements
- virtualenv 
- python 3.X
- mysql

##### Instalation
- Set up virtual env
```
virtualenv venv
source venv/bin/activate
```
- Install dependencies 
`pip3 install -r requirements.txt`

- Set up database variables
```
export 'DB_NAME' = <database table name>
export 'DB_USER' = <database table user>
export 'DB_PASSWORD' = <database table password>
export 'DB_HOST' = <database table host (optional - default localhost)>
export 'DB_PORT' = <database table name (optional - default 3306)>
```

- Optional - Load fixture data
`./manage.py loaddata fixture UserWalletsApp/fixtures/fixture.json `

- Start server
`python manage.py runserver`

- Test
`python manage.py test`




