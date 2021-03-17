from django.contrib import admin

# Register your models here.
from .models import Item, OrderItem, Order


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Item, ProductAdmin)
admin.site.register(OrderItem)
admin.site.register(Order)
