from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import get_user_model
from .models import Profile
from Homepage.models import (
                    HomepageMiddleSection,
                    InsertHeaderFooter,
                    HomepageMiddleSectionBelow,
                    HomepageMiddleSectionBelowTwo,
                    FooterAboveSection,
                    GeneralSettings,
                    HomepageAds,
                    PostDetailPageAds,
                    CopyRightSection,SEO
                    )
from Instant_Article.models import InstantArticleModel

from django_summernote.widgets import SummernoteWidget,SummernoteInplaceWidget

User=get_user_model()


class UserLoginForm(forms.Form):

	username        = forms.CharField(label="Username")

	password 		= forms.CharField(label='Password', widget=forms.PasswordInput)


	def clean(self,*args,**kwargs):

		username = self.cleaned_data.get("username")
		password = self.cleaned_data.get("password")
		user_obj = User.objects.filter(username=username).first()

		if not user_obj:

			raise  forms.ValidationError("Invalid Username or Password !")

		else:

			if not user_obj.check_password(password):

				raise forms.ValidationError("Invalid Username or Password !")
		return super(UserLoginForm,self).clean(*args,**kwargs)




class UserCreationForm(forms.ModelForm):

    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username','email','is_staff','is_admin','is_editor')

    def clean_password2(self):

        # Check that the two password entries match

        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):

        # Save the provided password in hashed format

        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

    def clean_username(self):
        username = self.cleaned_data.get('username')

        qs_exists = User.objects.filter(username=username).exists()
        if qs_exists:
            raise forms.ValidationError('Username already exists.')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')

        qs_exists = User.objects.filter(email=email).exists()
        if qs_exists:
            raise forms.ValidationError('Email already exists.')
        return email



class UserChangeForm(forms.ModelForm):

    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'is_active', 'is_staff','is_admin','is_editor')

    def clean_password(self):

        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value

        return self.initial["password"]

class UserUpdateForm(forms.ModelForm):

    class Meta:

        model = Profile
        exclude=["username","height_field","width_field"]


class HomepageMiddleWidgetForm(forms.ModelForm):

    class Meta:

        model =  HomepageMiddleSection
        fields= '__all__'



class InsertHeaderFooterForm(forms.ModelForm):

    class Meta:

        model =  InsertHeaderFooter
        fields= '__all__'


class HomepageMiddleWidgetFormBelow(forms.ModelForm):

    class Meta:

        model =  HomepageMiddleSectionBelow
        fields= '__all__'

class HomepageMiddleWidgetFormBelowTwo(forms.ModelForm):

    class Meta:

        model =  HomepageMiddleSectionBelowTwo
        fields= '__all__'


class FooterAboveSectionForm(forms.ModelForm):

    class Meta:

        model =  FooterAboveSection
        fields= '__all__'

class GeneralSettingsForm(forms.ModelForm):

    class Meta:

        model =  GeneralSettings
        exclude=["height_field","width_field","height_field_fav","width_field_fav"]

class HomepageAdsForm(forms.ModelForm):

    class Meta:
        model = HomepageAds
        fields='__all__'

class PostDetailAdsForm(forms.ModelForm):

    class Meta:
        model = PostDetailPageAds
        fields='__all__'

class CopyRightSectionForm(forms.ModelForm):


    class Meta:
        model = CopyRightSection
        fields='__all__'

    copy_right_text= forms.CharField(widget=SummernoteWidget(attrs={'width': '100%','height':'250px'}))
    about_summary = forms.CharField(widget=SummernoteWidget(attrs={'width': '100%','height':'250px'}))
    about_full = forms.CharField(widget=SummernoteWidget(attrs={'width': '100%'}))
    privary_policy = forms.CharField(widget=SummernoteWidget(attrs={'width': '100%'}))
    conatct = forms.CharField(widget=SummernoteWidget(attrs={'width': '100%'}))
    advertisement = forms.CharField(widget=SummernoteWidget(attrs={'width': '100%'}))

    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(CopyRightSectionForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['copy_right_text'].required = False
        self.fields['about_summary'].required = False
        self.fields['about_full'].required = False
        self.fields['privary_policy'].required = False
        self.fields['advertisement'].required = False
        self.fields['editor_email'].required = False
        self.fields['conatct'].required = False



class InstantArticleModelForm(forms.ModelForm):

    class Meta:
        model = InstantArticleModel
        fields='__all__'



class SEOForm(forms.ModelForm):

    class Meta:
        model = SEO
        fields='__all__'
