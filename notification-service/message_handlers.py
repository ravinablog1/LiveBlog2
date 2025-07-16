import pika
import json
from celery import shared_task

# RabbitMQ connection
def get_rabbitmq_connection():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('rabbitmq')
    )
    return connection

@shared_task
def process_notification(notification_data):
    """Process notifications from message queue"""
    notification_type = notification_data.get('type')
    
    if notification_type == 'comment':
        handle_comment_notification(notification_data)
    elif notification_type == 'post_update':
        handle_post_update_notification(notification_data)
    elif notification_type == 'follow':
        handle_follow_notification(notification_data)

def publish_notification(exchange, routing_key, message):
    """Publish notification to RabbitMQ"""
    connection = get_rabbitmq_connection()
    channel = connection.channel()
    
    channel.exchange_declare(exchange=exchange, exchange_type='topic')
    channel.basic_publish(
        exchange=exchange,
        routing_key=routing_key,
        body=json.dumps(message)
    )
    connection.close()