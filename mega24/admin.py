from django.contrib import admin
from .models import (Category, Company, SocialNetwork,
                     Phone, View, Address,
                     Discount, Customer,
                     Review, CouponOperation,
                     City)

# Register your models here.


admin.site.register(Category)
admin.site.register(Company)
admin.site.register(SocialNetwork)
admin.site.register(Phone)
admin.site.register(View)
admin.site.register(Address)
admin.site.register(Discount)
admin.site.register(Customer)
admin.site.register(Review)
admin.site.register(City)
admin.site.register(CouponOperation)
