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
* Docker >= 27.5.1


## Development

Run the docker container:

```sh
docker compose up -d --build
```

Then SSH into the docker container to set up Django:

```sh
docker compose exec web bash
cd backend
python manage.py migrate
```

Optionally you can create a superuser to access the Django admin:

```sh
python manage.py createsuperuser
```
