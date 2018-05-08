from django.conf import settings
from django.db import models
from django.core.urlresolvers import reverse
from django.utils.encoding import smart_text
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.core.validators import RegexValidator
from django.db.models.signals import post_save

def upload_location(instance, filename):

    image_name=filename.split(".")[0]
    extension=filename.split(".")[1]

    return "%s" %(str(instance.username)+"."+extension)




USERNAME_REGEX="^[a-zA-Z0-9_.]*$"

class MyUserManager(BaseUserManager):

    def create_user(self, username, email, password=None):

        """
        Creates and saves a User with the given username,email and password.
        """

        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        
        """
        Creates and saves a User with the given username,email and password.
        """

        user = self.create_user(
            username,
            email,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):

    username        = models.CharField(

                                        max_length=120,
                                        validators=[RegexValidator(

                                                regex=USERNAME_REGEX,
                                                message="Username must be Alphanumeric or contain any of the follwoing : '_ .'",
                                                code="Invalid Username"
                                            )],
                                        unique=True
                                    )
    email           = models.EmailField(
                                        verbose_name='email address',
                                        max_length=255,
                                        unique=True,
                                    )
    is_active       = models.BooleanField(default=True)
    is_staff        = models.BooleanField(default=False)
    is_admin        = models.BooleanField(default=False)
    is_editor       = models.BooleanField(default=False)

    objects         = MyUserManager()

    USERNAME_FIELD  = 'username'
    REQUIRED_FIELDS = ['email']

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    # @property
    # def is_staff(self):
    #     "Is the user a member of staff?"
    #     # Simplest possible answer: All admins are staff
    #     return self.is_admin

    @property
    def get_absolute_url(self):

        return reverse("Reporter:user_dashboard",kwargs={"user":self.username})



class Profile(models.Model):


    username                = models.OneToOneField(settings.AUTH_USER_MODEL)
    name_of_reporter        = models.CharField(max_length=225)
    display_name            = models.CharField(max_length=225)
    user_image              = models.ImageField(upload_to=upload_location,
                                null=True,
                                blank=True,
                                width_field="width_field",
                                height_field="height_field")
    height_field            = models.IntegerField(default=0)
    width_field             = models.IntegerField(default=0)




    def __str__(self):

        return smart_text(self.username.username)



def profile_post_save_receiver(sender,instance,created,*args,**kwargs):

    if created:

        try:
            Profile.objects.create(username=instance)
        except:
            pass


post_save.connect(profile_post_save_receiver,sender=settings.AUTH_USER_MODEL)