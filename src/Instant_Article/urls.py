from django.conf.urls import url
from .feeds import LatestEntriesFeed

app_name = "Instant_Article"

urlpatterns = [

     url(r'^feed/$', LatestEntriesFeed()),
]
