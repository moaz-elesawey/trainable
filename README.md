
# Traintable

Traintable is a System written in Python and shipped with a standalone API.


Develpment
===

Reset PostgreSQL Database
```sh
$ docker stop pg-trainable
$ docker rm pg-trainable
$ docker volume rm pg-trainable-data
```

Start PostgreSQL Database instance in docker with the following command.
```sh
$ docker run --name pg-trainable \
    -it -d -p 54322:5432 \
    -e POSTGRES_USER='postgres' \
    -e POSTGRES_PASSWORD='P@ssw0rd' \
    -e POSTGRES_DB='trainable' \
    -v pg-trainable-data:/var/lib/postgresql \
    postgres:16
```

Exec into the PostgreSQL Database instance
```sh
$ docker exec -it pg-trainable bash
```

View the logs of the db instance
```sh
$ docker logs pg-trainable -f -n 10

```
