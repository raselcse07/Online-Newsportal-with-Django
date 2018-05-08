from django.db import models
from django.db.models.signals import pre_save
from Post.utils import random_string_generator


def upload_location(instance, filename):

    image_name=filename.split(".")[0]
    extension=filename.split(".")[1]

    if not instance.image_title:

        return "%s" %(image_name+"."+extension)

    else:
        return "%s" %(instance.image_title+"."+extension)

class ImageGallery(models.Model):

    upload_image        = models.ImageField(upload_to=upload_location,
                                null=True,
                                blank=True,
                                width_field="width_field",
                                height_field="height_field")
    height_field        = models.IntegerField(default=0)
    width_field         = models.IntegerField(default=0)
    image_title         = models.CharField(max_length=250,blank=True)
    image_description   = models.TextField(blank=True)
    image_id            = models.CharField(max_length=250,unique=True)



    def __str__(self):

        return self.image_id

        


def post_pre_save_receiver(sender,instance,*args,**kwargs):

    if not instance.image_id:

        instance.image_id=random_string_generator(size=10)



pre_save.connect(post_pre_save_receiver, sender=ImageGallery)

