from django.contrib import admin
# import all models
from jersey_store.models import *
# Register your models here.
admin.site.register(Customer)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Product)
admin.site.register(ShippingAddress)
