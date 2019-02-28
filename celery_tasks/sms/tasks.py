"""

"""
from celery_tasks.main import celery
from libs.yuntongxun.sms import CCP


@celery.task
def send_sms_code(mobile, sms_code):
    result = 0
    a=1
    # result = CCP().send_template_sms(mobile, [sms_code, 6], 1)
    return result
