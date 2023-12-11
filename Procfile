web: gunicorn gingembre.asgi --worker-class=uvicorn.workers.UvicornWorker --log-file -
postdeploy: python manage.py migrate