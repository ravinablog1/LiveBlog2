import pika
import json
import redis
from django.conf import settings
from celery import shared_task

# RabbitMQ Configuration
def get_rabbitmq_connection():
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=settings.RABBITMQ_HOST,
                port=settings.RABBITMQ_PORT,
                virtual_host='/',
                credentials=pika.PlainCredentials('guest', 'guest')
            )
        )
        return connection
    except Exception as e:
        print(f"RabbitMQ connection failed: {e}")
        return None

# Redis Configuration
redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=0,
    decode_responses=True
)

class MessageBroker:
    @staticmethod
    def publish_to_rabbitmq(exchange, routing_key, message):
        """Publish message to RabbitMQ"""
        connection = get_rabbitmq_connection()
        if not connection:
            return False
            
        try:
            channel = connection.channel()
            channel.exchange_declare(exchange=exchange, exchange_type='topic')
            channel.basic_publish(
                exchange=exchange,
                routing_key=routing_key,
                body=json.dumps(message),
                properties=pika.BasicProperties(delivery_mode=2)  # Persistent
            )
            connection.close()
            return True
        except Exception as e:
            print(f"Failed to publish message: {e}")
            return False
    
    @staticmethod
    def publish_to_redis(channel, message):
        """Publish message to Redis pub/sub"""
        try:
            redis_client.publish(channel, json.dumps(message))
            return True
        except Exception as e:
            print(f"Failed to publish to Redis: {e}")
            return False

# Background Tasks
@shared_task
def process_notification_queue():
    """Process notification queue from RabbitMQ"""
    connection = get_rabbitmq_connection()
    if not connection:
        return
        
    channel = connection.channel()
    channel.queue_declare(queue='notifications', durable=True)
    
    def callback(ch, method, properties, body):
        try:
            message = json.loads(body)
            # Process notification
            from realtime.tasks import send_notification
            send_notification.delay(message)
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            print(f"Error processing notification: {e}")
    
    channel.basic_consume(queue='notifications', on_message_callback=callback)
    channel.start_consuming()

@shared_task
def process_image_queue():
    """Process image processing queue"""
    # Image processing logic
    pass

@shared_task
def generate_reports():
    """Generate analytics reports"""
    # Report generation logic
    pass