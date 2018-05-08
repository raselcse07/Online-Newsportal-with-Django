from django.conf.urls import url
from . import views


app_name = "Homepage"


urlpatterns = [

    url(r'^$',views.homepage_views,name="home_page"),
]
