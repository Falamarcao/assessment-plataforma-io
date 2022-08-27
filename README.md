<br>
<br>
<img src="images/logo-plataforma.png" alt="drawing" width="400"/>

# Pre assessment: Plataforma.io | Backend Python

![DRF Web UI](images/screenshot.jpg)

### This is my solution for the assessment presented [**HERE!**](Pre%20assessment%20-%20Plataforma.io%20-%20Backend%20Python.md)
### I hope you get fascinated or at least delighted.

# Getting Started

## Dependencies

* Docker
* Nginx (prod)
* Gunicorn (prod)
* PostgreSQL or possibly others SQL Databases
* Python
* Packages:
  * **Django**
  + **Django Rest Framework**
  + More Details on [requirements.txt](small_business/requirements.txt)


## Installing

> Do you have [Docker Installed](https://www.docker.com/)?


## NOTES About Both Enviroments - PROD & DEV
When web container start, on the first time, the follow commands are executed automatically:
```
    python manage.py flush --no-input
    python manage.py makemigrations
    python manage.py migrate --noinput
    python manage.py loaddata users.json posts.json reposts.json quote-postings.json
```
Getting ready the database and loading some example data, so NO NEED TO EXECUTE the commands ABOVE.\
They are included on entrypoints scripts: [entrypoint.sh](small_business/entrypoint.sh) and [entrypoint.prod.sh](small_business/entrypoint.prod.sh).

But if wanted on your own risk it's possible to execute using:
```
docker-compose -f docker-compose.prod.yml exec web python manage.py flush --noinput
docker-compose -f docker-compose.prod.yml exec web python manage.py makemigrations
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate --noinput
docker-compose -f docker-compose.prod.yml exec web python manage.py loaddata customers.json staff.json rooms.json events.json
```

**INFO: we are not putting migrations on version control because this is a fresh start project.\
Usually we put migrations on version control when we have a older project or a project where we expect to grow.**

## Building and Running Development environment (DEV)
* ### BUILD
  > docker-compose build --no-cache

* ### RUN
  > docker-compose up -d

* ### STOP
  > docker-compose down -v

* ### OPEN http://localhost:8000/

* ### SUPER USER & DJANGO ADMIN
  ```
  username: superuser
  password: password
  
  admin url: http://localhost:8000/admin
  ```

## Building and Running production-ready environment (PROD)
* ### If you have DEV running first take it down.
  > docker-compose down -v
* ### And then BUILD & RUN
  > docker-compose -f docker-compose.prod.yml up -d --build
* ### FINALLY OPEN http://localhost:1337/
* ### STOP
  > docker-compose -f docker-compose.prod.yml down -v

* ### USERS & DJANGO ADMIN
  ```
  username: superuser
  password: password
  
  username: staff
  password: password
  
  admin url: http://localhost:8000/admin
  ```

## Automated Tests

On DEV Environment tests are executed on every container start see [entrypoint.sh](small_business/entrypoint.sh) and a [test.log](small_business/test.log) file is generated,\
to run on demand see the commands bellow:

* ### DEV
  ````commandline
  docker-compose exec web python manage.py test small_business.rooms small_business.events
  ````

* ### PROD
  ````commandline
  docker-compose -f docker-compose.prod.yml exec web python manage.py test small_business.rooms small_business.events
  ````

## Help: If you have any problem please e-mail me or contact me on LinkedIn.


### Common issue:
```
Use notepad++, go to edit -> EOL conversion -> change from CRLF to LF.

update: For VScode users: you can change CRLF to LF by clicking on CRLF present on lower right side in the status bar

https://stackoverflow.com/questions/51508150/standard-init-linux-go190-exec-user-process-caused-no-such-file-or-directory
```

## Author: Marco Maschio
### [Linkedin](https://linkedin.com/in/marcoantonioms) | [Resume](https://falamarcao.github.io/resume/)
E-mail: marcoantoniom.siqueira@gmail.com

Thank you for your time, and I hope we can talk in near future.