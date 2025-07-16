from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/liveblog/(?P<liveblog_id>\d+)/$', consumers.LiveBlogConsumer.as_asgi()),
]