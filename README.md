# 10,000 Words

This is a project for building vocabulary in foreign languages.
The user supplies their own texts, and the application helps them build word
lists and sentence lists, which they can then practice in the app.

**NOTE:** This app was initially developed with English, Dutch, and German in
mind. For this reason, the grammatical models probably aren't as diverse as
they need to be to accommodate other language families.

For example, Japanese has more than two politeness levels, but this app
currently only handles 'casual' and 'formal'. I sincerely encourage people
interested in studying other languages to fork this and improve on the word
models.


## Requirements

* Python >= 3.12
* Docker >= 27.5.1 (optional, for postgres)


## Development

There are two ways to run this project,
either with a full Postgres database or with a local sqlite database.

### Quickstart with Sqlite

Install dependencies:

```sh
pip install -r requirements.txt
pip install -r requirements_dev.txt
```

Then set up the sqlite database:

```sh
cd backend
python manage.py migrate
```

If desired, create an admin user for the Django admin UI.

```sh
python manage.py createsuperuser
```

**NOTE:** This will not create a user capable of running
the 10,000 Words app.

Finally, start the app in the console:

```sh
cd ..
textual run --dev cli.app:TenThousandWordsApp
```

You can run tests that don't require postgres by doing:

```sh
pytest
```

And you can access the django admin at [localhost:8000](http://localhost:8000)
by running:

```sh
cd backend
python manage.py runserver
```


### Quickstart with Postgres

**NOTE:** Requires Docker.

Build and start the docker containers:

```sh
docker compose up -d --build
```

This will create an `admin` user with the password `dev`,
for use with the Django admin if desired.

You can visit the textual app at [localhost:8080](http://localhost:8080).

If you want to use the django admin,
you can visit [localhost:8000/admin](http://localhost:8000/admin).

To run the tests that require postgres:

```sh
docker compose exec web bash
pytest -c pytest.requires_postgres.ini
```

