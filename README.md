# Pulp Science
A Website where people can publish and read articles (or follow projects) about scientifical topics.


## Contributing
If you want to contribute please make sure to not commit directly to the master or development branch.
Instead, create a new branch from development and create a pull request with the development branch.

### Basic setup

To clone and contribute to this project please follow these steps:
- Make sure git and git LFS is installed on your machine to clone this repository
- Install tox
  - When installing tox please ensure that its path doesn't contain any spaces. This likely leads to weird errors.
  - For this, you can e.g. create a virtual python environment at `C:\` (on windows) and installing tox there.
- Set up your tox development environment by running
    ```bash
    tox -e dev
    ./.tox/dev/Scripts/activate
    ```
- If you are using PyCharm: Configure python interpreter of your IDE to `.tox/dev/Scripts/python.exe`

And that's it!

### Tips for frontend development

If you want to code on the stylesheets you will need to [install a sass compiler](https://sass-lang.com/install).
E.g. on Windows you can use `choco install sass`.

Hint: In PyCharm it is very comfortable to configure file watchers and scopes for the different scss main files.
For example, I configured two file watchers with its own scopes to compile `main_base.scss` and `main_index.scss`.

Below you can see an example of how you can configure such a file watcher:
![Screenshot of file watcher](readme_screenshot_file_watcher.jpg "Configuration to automatically compile `main_base.scss`.")

You can define a custom scope, since you only need to recompile when code is changed affecting the `main_base.scss`:
![Screenshot of file watcher scope](readme_screenshot_scope.jpg "Add only files to the scope imported by `main_base.scss`.")

## Server setups
There are two different setups. The easy-to-use test server of django
and a docker image emulating the production use-case.

### Django test setup
To use the django test server simply run:
```bash
python manage.py runserver
```
The backend will use the sqlite file as database. If you change something
in your code you should see the changes live in your browser - you don't have
to restart the server.

The server is addressable at `localhost:8000`.

Note: If you want to use djangos admin panel you may have to create the
superuser first:
```bash
python manage.py createsuperuser
```
But if you didn't rebuilt the sqlite database there should already be a superuser.
(user: admin, password: sekret1)

### Docker production setup
To use the docker setup - including backend and Postgres database server - run:
```bash
docker-compose up -d
```
If you changed something in the code you may have to rebuild the image:
```bash
docker-compose up -d --build
```
If you added a database migration or rebuilt the database volume you have
to migrate these changes. You have two options to do so:
1. Go to Docker Desktop and open a terminal for the backend container. It
should be named something like `pulpscience_web_1`. Type:
```bash
python manage.py migrate
```
2. Connect a terminal of your choice to the docker container and run migrations:
```bash
docker exec -it pulpscience_web_1 /bin/bash
python manage.py migrate
```

Alternatively, you can run this single command in the container directly with:
```bash
docker exec pulpscience_web_1 python manage.py migrate
```

To stop the docker container you can use:
```bash
docker-compose down
```
The server is addressable at `localhost:8020`. Both setups can run parallel.

Note: For the testing `.env` the admin account should be the same. (user: admin, password: sekret1)
