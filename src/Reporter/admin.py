from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import MyUser,Profile
from .forms import UserChangeForm,UserCreationForm




class UserAdmin(BaseUserAdmin):

    # The forms to add and change user instances
    
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    
    list_display = ('username','email', 'is_admin','is_staff')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('username','email', 'password')}),
        ('Personal info', {'fields': ('is_editor',)}),
        ('Permissions', {'fields': ('is_admin','is_staff')}),
    )
    
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username','email', 'password1', 'password2')}
        ),
    )
    search_fields = ('username','email',)
    ordering = ('username','email',)
    filter_horizontal = ()

# Now register the new UserAdmin...

admin.site.register(MyUser, UserAdmin)
admin.site.register(Profile)

# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
# admin.site.unregister(Group)