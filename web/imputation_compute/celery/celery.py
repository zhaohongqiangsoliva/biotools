from __future__ import absolute_import

from celery import Celery

app = Celery('imputation_compute', include=['imputation_compute.tasks'])

app.config_from_object('imputation_compute.celeryconfig')

@app.task
def add(x, y):
    return x + y

if __name__ == '__main__':
    result = add.delay(30, 42)