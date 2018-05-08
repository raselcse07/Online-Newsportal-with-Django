from django import forms
from .models import (
                PostCategory,
                PostModel,
                DivisionalPostCategory,
                DivisionName
                )

from django_summernote.widgets import SummernoteWidget,SummernoteInplaceWidget

class CategoryCreateForm(forms.ModelForm):

    class Meta:

        model=PostCategory
        fields=[

            "category_name",

        ]

class DivisionalCategoryCreateForm(forms.ModelForm):

    class Meta:

        model=DivisionalPostCategory
        fields=[

            "name_of_division",
            "name_of_distict"

        ]

class PostCreateForm(forms.ModelForm):


    class Meta:
        model=PostModel
        exclude=["user","slug","timestamp","updated","publish_date","total_page_views"]


    content=forms.CharField(widget=SummernoteWidget(attrs={'width': '100%','height':'1020px'}))

    title = forms.CharField(widget=forms.TextInput(
                                    attrs={

                                    'class':'form-control',
                                    'placeholder':'Post Title',

                                    })
                                )
    featured_image_id = forms.CharField(widget=forms.TextInput(
                                    attrs={

                                    'class':'form-control',
                                    'placeholder':'Featured Image ID',

                                    }),
                                label = "Featured Image ID"
                                )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['divisional_category'].queryset = DivisionalPostCategory.objects.none()

        if 'division' in self.data:
            try:
                division_id = int(self.data.get('division'))
                self.fields['divisional_category'].queryset = DivisionalPostCategory.objects.filter(id=division_id)
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        

class PostUpdateForm(forms.ModelForm):

    
    class Meta:
        model=PostModel
        exclude=["user","slug","timestamp","updated","publish_date","total_page_views"]

    content=forms.CharField(widget=SummernoteWidget(attrs={'width': '100%','height':'1400px'}))

    title = forms.CharField(widget=forms.TextInput(
                                    attrs={

                                    'class':'form-control',
                                    'placeholder':'Post Title',

                                    })
                                )
    featured_image_id = forms.CharField(widget=forms.TextInput(
                                    attrs={

                                    'class':'form-control',
                                    'placeholder':'Featured Image ID',

                                    }),
                                label = "Featured Image ID"
                                )
    


class DivisionalCategoryForm(forms.ModelForm):


    class Meta:

        model = DivisionalPostCategory
        exclude = ["divisional_category_slug"]

