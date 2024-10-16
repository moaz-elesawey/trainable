
# Traintable

Your Training Platform


To start the application in dev mode use:
```sh
$ docker compose -p trainble watch
```

this command watches for any changes in application files and reload the app.


To connect to the database you can go to [adminer](0.0.0.0:8080) which redirect to adminer which is a simple interface to manage databases.

You can connect to the database using the credientials specified in the `.env` file.

Or if you prefer cli tool like me you can use the greatest `pgcli` using the following command

```sh
$ pgcli -h 127.0.0.1 -p 5432 -Upostgres -d trainable -W
```


To view the logs of the `webapp` use

```sh
$ docker compose -p trainable logs webapp -f
```

Development
---
Refer to [Development](./development.md)


Deployment
---
Refer to [Deployment](./deployment.md)

Credit
---
This work of `docker` and `docker compose` is based on [full-stack-fastapi-template](https://github.com/fastapi/full-stack-fastapi-template.git) by tiagolog and fastapi.