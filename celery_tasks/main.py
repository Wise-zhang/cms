"""

"""
import os

from celery import Celery

# 设置setting文件
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cms.settings")

# 创建celery对象
celery = Celery(main="cms", broker="redis://127.0.0.1:6379/14")

# 指定从哪进行扫描任务
celery.autodiscover_tasks(['celery_tasks.sms'])


