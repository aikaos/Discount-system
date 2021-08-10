from datetime import timezone
from itertools import chain

from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend

from .models import Category, Company, City, CouponOperation
from .serializers import CategorySerializer, CompanySerializer, \
    DetailSerializer, CitySerializer, ReviewSerializer, CouponSerializer, ActivationCouponSerializer
from .dto import get_detail_dto, get_company_dto_list


class CategoryList(ListAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        queryset = Category.objects.all().order_by('order_num')
        return queryset


class CityList(ListAPIView):
    serializer_class = CitySerializer

    def get_queryset(self):
        queryset = City.objects.all().order_by('order_num')
        return queryset


@api_view(['GET'])
def company_list(request):
    if request.method == 'GET':
        category_query = request.query_params.getlist('category')
        city_query = request.query_params.getlist('city')

        queryset = Company.objects.filter(active=True)
        if category_query:
            # sorted_query_set_by_category
            queryset = queryset.filter(active=True, category__name__in=category_query)

        if city_query:
            # sorted_query_set_by_city
            queryset_searched = queryset.filter(active=True, address__city__name__in=city_query)
            queryset_exclude = queryset.exclude(active=True, address__city__name__in=city_query)

            queryset = chain(queryset_searched, queryset_exclude)

        company_dto = get_company_dto_list(queryset)
        serializer = CompanySerializer(company_dto, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def detail_list(request, pk):
    if request.method == 'GET':
        queryset = Company.objects.get(active=True, pk=pk)
        company_dto = get_detail_dto(queryset)
        serializer = DetailSerializer(company_dto)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def create_review(request):
    if request.method == 'POST':
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def create_coupon(request):
    if request.method == 'POST':
        serializer = CouponSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def activation_of_coupon(request):
    if request.method == 'POST':
        discount, customer = request.data['discount'], request.data['customer']
        operation = CouponOperation.objects.get(discount__id=discount, customer__id=customer)
        serializer = ActivationCouponSerializer(operation, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)
