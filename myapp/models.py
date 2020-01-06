from django.db import models
import random
import datetime
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
import os
from django.conf import settings
from django.utils.safestring import mark_safe


class Publisher(models.Model):
    name = models.CharField(max_length=200)
    website = models.URLField()
    city = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=20, default='USA')
    def __str__(self):
        return self.name

class Book(models.Model):
    CATEGORY_CHOICES = [
        ('S', 'Scinece&Tech'),
        ('F', 'Fiction'),
        ('B', 'Biography'),
        ('T', 'Travel'),
        ('O', 'Other')
    ]
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=1, choices=CATEGORY_CHOICES, default='S')
    num_pages = models.PositiveIntegerField(default=100)
    price = models.DecimalField(max_digits=10, decimal_places=2,validators=[MaxValueValidator(1000), MinValueValidator(0)])
    publisher = models.ForeignKey(Publisher, related_name='books', on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    num_reviews = models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.title

class Member(User):
    STATUS_CHOICES = [
        (1, 'Regular member'),
        (2, 'Premium Member'),
        (3, 'Guest Member'),
    ]

    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    address = models.CharField(max_length=300, blank=True)
    city = models.CharField(max_length=20, default='Windsor')
    province = models.CharField(max_length=2, default='ON')
    last_renewal = models.DateField(default=timezone.now)
    auto_renew = models.BooleanField(default=True)
    borrowed_books = models.ManyToManyField(Book, blank=True)
    image = models.ImageField(upload_to='media', blank=True)
    externalURL = models.URLField(blank=True)

    def url(self):

        if self.externalURL:
            return self.externalURL
        else:

            return os.path.join('/', settings.MEDIA_URL, os.path.basename(str(self.image)))

    def image_tag(self):

        return mark_safe('<img src="{}" width="150" height="150" />'.format(self.url()))

    image_tag.short_description = 'Image'




    def url(self):
        # returns a URL for either internal stored or external image url
        if self.externalURL:
            return self.externalURL
        else:
            # is this the best way to do this??
            return os.path.join('/', settings.MEDIA_URL, os.path.basename(str(self.image)))

    def image_tag(self):
        # used in the admin site model as a "thumbnail"
        return mark_safe('<img src="{}" width="50" height="50" />'.format(self.url()))

    image_tag.short_description = 'Image'

class Order(models.Model):
    ORDER_CHOICES = [
        (0, 'Purchase'),
        (1, 'Borrow')
    ]
    books = models.ManyToManyField(Book)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='books')
    order_type = models.IntegerField(choices=ORDER_CHOICES, default=1)
    order_date = models.DateField(default=timezone.now)
    def __str__(self):
        return str(self.id)

    def total_items(self):
        return self.books.count()

class Review(models.Model):
    reviewer = models.EmailField()
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comments = models.TextField(blank=True)
    date = models.DateField(default=timezone.now)
    def __str__(self):
        return str(self.id)

