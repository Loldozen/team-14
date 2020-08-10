from django.db import models
from django.contrib.auth import get_user_model
from django.contrib .auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.text import slugify
from django.utils. translation import gettext_lazy as _

from .managers import CustomUserManager
# Create your models here.

class CustomUser(AbstractBaseUser, PermissionsMixin):
    #User model with granular control

    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=20)
    last_name = models.CharField(_('last name'), max_length=20)
    is_staff = models.BooleanField(_('staff'),default=False)
    is_active = models.BooleanField(_('active'),default=True)
    date_joined = models.DateTimeField(_('date joined'),auto_now_add=True)
    last_login = models.DateTimeField(_('last login'), auto_now=True)
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    def get_email(self):
        return self.email


User = get_user_model()

class Clothing(models.Model):
    
    CATEGORY = (
        ('CLOTHES','Clothes'),
        ('BAGS','Bags'),
        ('SPORTS','Sport'),
        ('SHOES','Shoes'),
        ('ACCESSORIES','Accesories'),
    )
    user = models.ForeignKey(User, related_name='clothings', on_delete=models.CASCADE)
    name = models.CharField(_('Name of clothes'), max_length=100)
    slug = models.SlugField()
    date_created = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(_('Price'), max_digits=10, decimal_places=2)
    category = models.CharField(_('Category'), max_length=15, choices=CATEGORY)
    number = models.PositiveIntegerField(_('Available number'))
    objects = models.Manager()

    def __str__(self):
        return self.name

    def save(self):
        self.slug = slugify(self.name)
        super(Clothing, self).save()

class Payment(models.Model):
    user = models.ForeignKey(User, related_name='payments', on_delete=models.CASCADE)
    clothing = models.ForeignKey(Clothing, related_name='payments', on_delete=models.CASCADE)
    date_created = models.DateTimeField(_('Date created'), auto_now_add=True)
    objects = models.Manager()
