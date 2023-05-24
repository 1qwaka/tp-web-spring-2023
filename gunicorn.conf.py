import multiprocessing

bind = "127.0.0.1:8000"
wsgi_app = "asksus.wsgi:application"
workers = 2
worker_class = 'sync'
timeout = 15
daemon = False
raw_env = [
    'DJANGO_SECRET_KEY=django-insecure-v8jxe9nmzx^=sthxh6#31(dk$yulja+yg0q5jc7igxd&7hzat+'
]
backlog = 2048
errorlog = "errors.log"
loglevel = "info"
accesslog = "access.log"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
