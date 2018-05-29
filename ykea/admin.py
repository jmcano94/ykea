from django.contrib import admin
from .models import Item
from .models import Customer
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User


class CustomerInline(admin.StackedInline):
    model = Customer
    can_delete = False
    verbose_name_plural = 'customers'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (CustomerInline, )


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Customer)
admin.site.register(Item)
