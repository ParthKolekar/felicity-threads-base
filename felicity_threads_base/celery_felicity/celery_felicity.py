from __future__ import absolute_import
from celery import Celery


app = Celery('felicity_threads_base.base.tasks')
app.config_from_object('felicity_threads_base.felicity_threads_base.celeryconfig')

if __name__ == '__main__':
        app.start()

