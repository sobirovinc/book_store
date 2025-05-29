import datetime
from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(User, auto_now=True)
    phone = models.CharField(max_length=20, blank=True)
    adress1 = models.CharField(max_length=200, blank=True)
    adress2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200, blank=True)
    state = models.CharField(max_length=200, blank=True)
    zipcode = models.CharField(max_length=200, blank=True)
    country = models.CharField(max_length=200, blank=True)
    cart = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.user.username

    #create a profile when user signs up by djangos auth system
    def create_profile(sender, instance, created, **kwargs):
        if created:
            user_profile = Profile(user=instance)
            user_profile.save()

    #automating creating profile
    post_save.connect(create_profile, sender=User)


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=14)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=8)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1, related_name='products')
    description = models.CharField(max_length=250, default='', blank=True, null=True)
    image = models.ImageField(upload_to='uploads/product/')
    is_sale = models.BooleanField(default=False)
    discount = models.DecimalField(default=0, decimal_places=1, max_digits=3)

    def __str__(self):
        return self.name

    @property
    def discount_price(self):
        if self.is_sale and self.discount > 0:
            discount_amount = self.price * (self.discount / 100)
            return round(self.price - discount_amount, 2)
        return self.price


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    address = models.CharField(max_length=100, default='', blank=True)
    phone = models.CharField(max_length=14, default='', blank=True)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.product



