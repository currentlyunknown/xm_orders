# XM Orders

This is a containerized REST API for making orders to convert money from one currency to another.

## How it works

Celery is used to run background tasks asynchronously (in this case, to convert a currency).

Once an Order is made, a task is queued for Celery to process.

Then, FE can use the `/api/orders/get-order-status/{order_id}` to review the `order_status` until it shows up as `executed`.

There's 5 statuses available for the order:
- pending
- started
- failed (if any error occurs)
- executed
- canceled

## What's included

- All the endpoints required for Orders
- Register new users
- Login
- Logout
- Email confirmation
- Temporary email validator (to make sure the email used for registering is not a temp email)

## Tech stack

- DjangoRestFramework
- PostgreSQL
- Celery (for background tasks, in this case for converting currencies)
- Redis (for brokering Celery tasks)
- Flower (for browsing Celery tasks)
- Pytest
- Poetry
- Docker

## Installation

1. Open your Docker Daemon (i.e. Docker Desktop).
2. In terminal, go to the app directory (`xm_orders`)
3. `make docker_build` to build the container images.
4. `make docker_up` to start the containers.

## Tearing down

1. `make docker_down` to stop the containers.
2. `make docker_nuke` to remove the containers and their images (warning - you'll need to run `make docker_build` again after this to access the app again)

## .env file

You'll need to create an `.env.dev` file in `xm_orders/app`

Its structure should look like this:

```
DEBUG=1
SECRET_KEY=foo
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=orders_dev
SQL_USER=orders
SQL_PASSWORD=orders
SQL_HOST=orders-db
SQL_PORT=5432
DATABASE=postgres
CELERY_BROKER=redis://redis:6379/0
CELERY_BACKEND=redis://redis:6379/0
```

## Run tests

`make docker_bash` to start app container's bash.

Once there, run `python -m pytest` to run all automatic tests.

## API Swagger

To see all the endpoints, go to `localhost:8007/swagger/`

Routes available for Order making:

`/api/orders/create-order/`

`/api/orders/delete-order/{order_id}`

`/api/orders/get-order/{order_id}`

`/api/orders/cancel-order/{order_id}`

`/api/orders/get-order-status/{order_id}`

## Admin dashboard

You can access Admin dashboard on `localhost:8007/admin/`

By default, a superuser is created with the following credentials:

Login: `admin@admin.com`

Pass: `adminpass`
