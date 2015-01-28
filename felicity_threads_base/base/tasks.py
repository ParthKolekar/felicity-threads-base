from __future__ import absolute_import

from celery import shared_task

@shared_task
def test(param):
    return 'The test task executed with argument "%s" ' % param

@shared_task
def checker_queue(submission_id):
    return str(submission_id) + " to Worker Queue Added."
