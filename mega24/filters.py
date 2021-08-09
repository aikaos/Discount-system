from django_filters import rest_framework as filters, OrderingFilter

from .models import Category, City


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class CategoryFilter(filters.FilterSet):
    order_num = OrderingFilter(fields=(("order_num", '0')))

    class Meta:
        model = Category
        fields = ['order_num']


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class CityFilter(filters.FilterSet):
    order_num = OrderingFilter(fields=(('order_num', '0')))

    class Meta:
        model = City
        fields = ['order_num']