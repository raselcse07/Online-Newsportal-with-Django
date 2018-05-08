from django.conf.urls import url
from . import views

app_name="Gallery"

urlpatterns = [
    url(r'^upload_images/$',views.ImageUpload,name="upload_image"),

]
