from datetime import timedelta, datetime, date
from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.encoding import smart_text
from django.utils.safestring import mark_safe
from django.db.models.signals import pre_save
from django.utils import timezone
from django.utils.timesince import timesince
from .utils import (
                    unique_category_slug_generator,
                    unique_post_slug_generator,
                    unique_divisional_category_slug_generator
                    )

from Gallery.models import ImageGallery

POST_PUBLISH=[
        ("draft","Draft"),
        ("publish","Publish"),
        ("private","Private")
]



FEATURED_POST=[
        
        ("Y","Yes"),
        ("N","No")
        
]


class DivisionName(models.Model):

    division_name       = models.CharField(max_length=200)

    def __str__(self):
        return smart_text(self.division_name)




class PostCategory(models.Model):

    category_name       = models.CharField(max_length=250)
    category_slug       = models.CharField(max_length=250,unique=True,db_index = True)


    class Meta:

        verbose_name='General Category'
        verbose_name_plural='General Category'

    def __str__(self):
        return smart_text(self.category_name)


class DivisionalPostCategory(models.Model):

    name_of_division             = models.ForeignKey(DivisionName,on_delete=models.CASCADE)
    name_of_distict              = models.CharField(max_length=100)
    divisional_category_slug     = models.CharField(max_length=250,unique=True,db_index = True)



    class Meta:

        verbose_name="Divisional Post Category"
        verbose_name_plural="Divisional Post Category"
        ordering=["name_of_distict"]

    def __str__(self):

        return smart_text(self.name_of_distict)

class PostModel(models.Model):

    user                = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    title               = models.CharField(max_length=250)
    slug                = models.CharField(max_length=250,unique=True,db_index = True)
    category            = models.ForeignKey(PostCategory,on_delete=models.CASCADE)
    content             = models.TextField()
    featured_image_id   = models.CharField(max_length=250)
    publish_date        = models.DateField(auto_now=False, auto_now_add=False, default=timezone.now)
    publish             = models.CharField(max_length=100,choices=POST_PUBLISH,default="publish")
    timestamp           = models.DateTimeField(auto_now=False,auto_now_add=True)
    updated             = models.DateTimeField(auto_now=True,auto_now_add=False)
    is_featured         = models.CharField(max_length=100,choices=FEATURED_POST,default="N")
    division            = models.ForeignKey(DivisionName,on_delete=models.CASCADE,blank=True,null=True)
    divisional_category = models.ForeignKey(DivisionalPostCategory,on_delete=models.CASCADE,blank=True,null=True)
    is_image_gallery    = models.CharField(max_length=200,choices=FEATURED_POST,default="N") 
    is_video_gallery    = models.CharField(max_length=200,choices=FEATURED_POST,default="N") 
    total_page_views    = models.IntegerField(default=0)

    class Meta:

        verbose_name='Post'
        verbose_name_plural='Posts'
        ordering=["-timestamp","-updated"]

    def __str__(self):

        return smart_text(self.title)

    def get_absolute_url(self):

        return reverse("Post:post_detail", kwargs={"slug": self.slug})

    @property
    def get_markdown(self):
        content = self.content
        # markdown_text = markdown(content)
        return mark_safe(content)

    @property
    def age(self):
        if self.publish == 'publish':
            now = datetime.now()
            publish_time = datetime.combine(
                                self.publish_date,
                                datetime.now().min.time()
                        )
            try:
                difference = now - publish_time
            except:
                return "Unknown"
            if difference <= timedelta(minutes=1):
                return 'just now'
            return '{time} ago'.format(time= timesince(publish_time).split(', ')[0])
        return "Not published"




def category_pre_save_receiver(sender,instance,*args,**kwargs):

    if not instance.category_slug:

        instance.category_slug=unique_category_slug_generator(instance)


def divisional_category_pre_save_receiver(sender,instance,*args,**kwargs):

    if not instance.divisional_category_slug:

        instance.divisional_category_slug=unique_divisional_category_slug_generator(instance)


def post_pre_save_receiver(sender,instance,*args,**kwargs):

    if not instance.slug:

        instance.slug=unique_post_slug_generator(instance)

pre_save.connect(post_pre_save_receiver, sender=PostModel)
pre_save.connect(category_pre_save_receiver, sender=PostCategory)
pre_save.connect(divisional_category_pre_save_receiver, sender=DivisionalPostCategory)
