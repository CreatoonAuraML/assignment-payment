from django.contrib import admin
from .models import User, ItemCategory, Item,  Order

admin.site.register(User)
admin.site.register(ItemCategory)
admin.site.register(Item)
admin.site.register(Order)