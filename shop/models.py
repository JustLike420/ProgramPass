from django.db import models
from django.conf import settings

# Create your models here.
from django.urls import reverse


class Item(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=255, verbose_name='url', unique=True)
    price = models.FloatField(default=0.0)
    description = models.TextField(max_length=255)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('core:product', kwargs={"slug": self.slug})

    def get_add_to_cart_url(self):
        return reverse('core:add-to-cart', kwargs={"slug": self.slug})

    def get_remove_from_cart_url(self):
        return reverse('core:remove-from-cart', kwargs={"slug": self.slug})


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    # quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"1 of {self.item.title}"


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
