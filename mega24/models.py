from datetime import timedelta

from django.db import models

from random import randint
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)
    order_num = models.IntegerField()

    def __str__(self):
        return self.name


def get_random_pin():
    return randint(1000, 9999)


class Company(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    logo = models.URLField()
    active = models.BooleanField(default=True)
    working_hours = models.CharField(max_length=200)
    max_coupon = models.IntegerField()
    pin = models.CharField("Пин-код", max_length=4, default=get_random_pin)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING,
                                 related_name='categories')
    address = models.ForeignKey('Address', on_delete=models.DO_NOTHING,
                                related_name='cities')

    def __str__(self):
        return self.name


class SocialNetwork(models.Model):
    link = models.URLField()
    name = models.CharField(max_length=100)
    choices = [('Instagram', 'Instagram'),
               ('Facebook', 'Facebook'),
               ('YouTube', 'YouTube')]
    type = models.CharField(max_length=200, choices=choices)
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name


class Phone(models.Model):
    phone_number = models.CharField(max_length=50)
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.phone_number


class View(models.Model):
    id = models.OneToOneField(Company, on_delete=models.DO_NOTHING, primary_key=True)
    count = models.IntegerField()

    def __str__(self):
        return str(self.count)


class Address(models.Model):
    street = models.CharField(max_length=100)
    str_num = models.IntegerField()
    lan = models.FloatField()
    lon = models.FloatField()
    city = models.ForeignKey('City', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.street


class City(models.Model):
    name = models.CharField(max_length=100)
    order_num = models.IntegerField()

    def __str__(self):
        return self.name


class Discount(models.Model):
    percent = models.FloatField()
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    valid_until = models.DurationField('Coupon is valid until', default=timedelta())
    active = models.BooleanField(default=True)
    order_num = models.IntegerField()
    condition = models.CharField(max_length=1000)
    id = models.OneToOneField(Company, on_delete=models.CASCADE,
                              primary_key=True)

    def __str__(self):
        return str(self.percent)


class Customer(models.Model):
    phone_number = models.CharField(max_length=100)

    def __str__(self):
        return self.phone_number


class Review(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    review = models.CharField(max_length=1000)
    date_publish = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING,
                                 related_name='customer')
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING,
                                related_name='reviews')

    def __str__(self):
        return self.review


class CouponOperation(models.Model):
    STATUS_CHOICES = [(0, 'not active'),
                      (1, 'activated'),
                      (2, 'expired')]
    create_date = models.DateTimeField(auto_now_add=True)
    valid_to = models.DateTimeField()
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    discount = models.ForeignKey(Discount, on_delete=models.DO_NOTHING)
