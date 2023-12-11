web: gunicorn gingembre.asgi --worker-class=uvicorn.workers.UvicornWorker
postdeploy: python manage.py migrate