from django.contrib import admin
from .models import (

                        PostCategory,
                        PostModel,
                        DivisionalPostCategory,
                        DivisionName
                  
                    )

from django_summernote.admin import SummernoteModelAdmin

class PostModelAdmin(SummernoteModelAdmin):

    fields=[
        "user",
        "title",
        "slug",
        "category",
        "content",
        "featured_image_id",
        "publish",
        "publish_date",
        "timestamp",
        "updated",
        "is_featured",
        "division",
        "divisional_category",
        "is_image_gallery",
        "is_video_gallery",
        "post_age",
        "total_page_views"

    ]
    readonly_fields=["timestamp","updated","post_age"]
    def post_age(self, obj, *args, **kwargs):
        return str(obj.age)

    class Meta:
        model=PostModel

admin.site.register(PostCategory)
admin.site.register(DivisionalPostCategory)
admin.site.register(PostModel,PostModelAdmin)
admin.site.register(DivisionName)


