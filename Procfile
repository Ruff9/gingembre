web: gunicorn gingembre.asgi --worker-class=uvicorn.workers.UvicornWorker --capture-output --log-level='debug'
postdeploy: python manage.py migrate