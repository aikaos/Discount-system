from django.urls import path, include

from . import views

urlpatterns = [
    path("category/list/", views.CategoryList.as_view()),
    path("city/list/", views.CityList.as_view()),
    path("company/list/", views.company_list),
    path("detail/<int:pk>/", views.detail_list),
    path('review/list/', views.create_review),
    path('coupon/', views.create_coupon),
    path('coupon/activation/', views.activation_of_coupon),
]