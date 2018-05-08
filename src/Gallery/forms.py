from django import forms
from .models import ImageGallery

class ImageUplaodForm(forms.ModelForm):

    class Meta:
        model=ImageGallery
        fields=[

            "upload_image",
            "image_title",
            "image_description"
        ]
    
