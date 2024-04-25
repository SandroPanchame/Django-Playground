from time import sleep
from celery import shared_task
from storefront.celery import celery
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@shared_task
def notify_customers(message):
    logger.info('Sending 10k emails...')
    # print('Sending 10k emails...')
    logger.info(message)
    sleep(10)
    logger.info('emails were sent!')
    # print(message)
    # sleep(10)
    # print('Emails were successfuly sent!')