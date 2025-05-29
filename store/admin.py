from django.contrib import admin
from django.contrib.auth.models import User
from .models import Product, Customer, Category, Order, Profile

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Profile)


# mix profile and user models
class ProfileInline(admin.StackedInline):
    model = Profile


# extend the user model
class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ['username', 'first_name', 'last_name', 'email']
    inlines = [ProfileInline]


# unregister the old way
admin.site.unregister(User)

# register the new way
admin.site.register(User, UserAdmin)
