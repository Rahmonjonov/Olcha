from django.db import models
from django.contrib.auth.models import AbstractUser

class Rates(models.Model):
    name = models.CharField(max_length=255)
    price = models.FileField(default=0)
    text = models.TextField()

    class Meta(AbstractUser.Meta):
        verbose_name = '01)Tarif'

class Company(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    rate = models.ForeignKey(Rates, on_delete=models.CASCADE, null=True, blank=True)

class User(AbstractUser):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    phone  = models.CharField(max_length=13, unique=True, blank=True, null=True)
    is_director = models.BooleanField(default=False)
    limit = models.DateField(null=True, blank=True)


    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class Category(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='category/')

class Products(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    bar_code = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    body_price = models.FloatField(default=0)
    price = models.FloatField(default=0)
    amount = models.IntegerField(default=0)

class Customer(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=13)
    summa = models.FloatField(default=0)
    locaiton = models.CharField(max_length=255, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    date_time = models.DateTimeField(auto_now_add=True)

class Dept(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    phone = models.CharField(max_length=13)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    date_time = models.DateTimeField(auto_now_add=True)

class Expenses(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=255)
    expenses_name = models.CharField(max_length=255)
    summa = models.FloatField(default=0)
    additional = models.FloatField(default=0)
    date = models.DateField(null=True, blank=True)


