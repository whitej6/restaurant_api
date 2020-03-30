from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
from django.utils.text import slugify


class UserManager(BaseUserManager):
    """

    """

    def create_user(self, email, password=None, **extra_fields):
        """

        """

        if not email:
            raise ValueError('User must provide email')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """

        """

        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """

    """
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class DeliveryApp(models.Model):
    """

    """
    name = models.CharField(max_length=255)
    slug = models.SlugField(
        unique=True
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(DeliveryApp, self).save(*args, **kwargs)


class Restaurant(models.Model):
    """

    """
    name = models.CharField(max_length=255)
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=255)
    phonenumber = models.CharField(max_length=255)
    hours = models.CharField(max_length=255)
    dine_in = models.BooleanField(default=False)
    take_out = models.BooleanField(default=False)
    drive_thru = models.BooleanField(default=False)
    curbside = models.BooleanField(default=False)
    delivery = models.BooleanField(default=False)
    delivery_apps = models.ManyToManyField(DeliveryApp, blank=True)
    website = models.URLField(max_length=255)
    email = models.EmailField(max_length=255, blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    notes = models.CharField(max_length=255, blank=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
