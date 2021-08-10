import datetime
from django.utils import timezone

from django.utils.timezone import now
from rest_framework import serializers, status
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import ValidationError

from .models import Category, SocialNetwork, City, Review, CouponOperation, Discount, Company


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class CompanySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=1000)
    logo = serializers.URLField()
    working_hours = serializers.CharField(max_length=200)
    city = serializers.CharField(max_length=50)
    percent = serializers.FloatField()
    count = serializers.IntegerField()


class SocialNetworkSerializers(serializers.ModelSerializer):
    class Meta:
        model = SocialNetwork
        fields = "__all__"


class DetailSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=100)
    condition = serializers.CharField()
    description = serializers.CharField(max_length=1000)
    logo = serializers.URLField()
    lan = serializers.FloatField()
    lon = serializers.FloatField()
    percent = serializers.FloatField()
    count = serializers.IntegerField()
    social_networks = SocialNetworkSerializers(many=True)


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['name', 'customer', 'review', 'company']


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = CouponOperation
        exclude = ['status', 'valid_to', 'create_date']

    def create(self, validated_data):

        valid_to = datetime.datetime.now() + validated_data['discount'].valid_until

        coupon = CouponOperation.objects.create(valid_to=valid_to,
                                                customer=validated_data['customer'],
                                                discount=validated_data['discount'])

        return coupon

    def validate(self, data):

        customer = data['customer']
        discount = data['discount']

        # Is the coupon already exist?

        if CouponOperation.objects.filter(customer=customer, discount=discount):
            raise serializers.ValidationError("Coupon already exists!.")

        # Has been reached the limit of coupon?
        max_coupon = CouponOperation.objects.filter(discount=discount, status__in=['0', '1'])
        if len(max_coupon) >= discount.id.max_coupon:
            discount.id.active = False
            discount.id.save()
            raise serializers.ValidationError("Coupon limit has been reached.")

        return data


class ActivationCouponSerializer(serializers.ModelSerializer):
    pin = serializers.IntegerField()

    class Meta:
        model = CouponOperation
        fields = ["pin", "customer", "discount"]

    def validate(self, data):
        pin = data['pin']
        discount = data['discount']
        customer = data['customer']

        operation = CouponOperation.objects.get(discount=discount, customer=customer)
        if operation.valid_to < timezone.now():
            CouponOperation.objects.update(status='3')
            raise ValidationError('Coupon has expired!')

        elif pin != int(discount.id.pin):
            raise ValidationError('Incorrect pin!')

        return data

    # The status of coupon
    def update(self, instance, validated_data):
        instance.status = 1
        instance.save()
        return instance

    def to_representation(self, instance):
        return {'1': 'Coupon is active!'}

