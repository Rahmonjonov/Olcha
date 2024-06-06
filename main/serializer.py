from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import *
from drf_yasg.utils import swagger_auto_schema



class RatesSerializer(ModelSerializer):

    class Meta:
        model = Rates
        fields = '__all__'



class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'



class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class UserCreateSerializer(serializers.Serializer):
    location = serializers.CharField(max_length=255)
    name = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)
    phone = serializers.CharField(max_length=13)
    is_director = serializers.BooleanField()

class CompanySerializer(ModelSerializer):

    class Meta:
        model = Company
        fields = '__all__'


class CategorySerializer(ModelSerializer):

    company = CompanySerializer(read_only=True)

    class Meta:
        model = Category
        fields = '__all__'

class CategoryADDSerializer(serializers.Serializer):
    name = serializers.CharField()
    image = serializers.ImageField()


class ProductsSerializer(ModelSerializer):
    company = CompanySerializer(read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Products
        fields = '__all__'

class ProductADDSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    bar_code = serializers.CharField(max_length=255)
    category = serializers.IntegerField()
    body_price = serializers.FloatField()
    price = serializers.FloatField()
    amount = serializers.IntegerField()

class CustomerSerializer(ModelSerializer):

    company = CompanySerializer(read_only=True)

    class Meta:
        model = Customer
        fields = '__all__'


class CustomerADDSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    locaiton = serializers.CharField(max_length=255)
    phone = serializers.CharField(max_length=13)
    summa = serializers.FloatField(default=0)
    start_date = serializers.DateField()
    end_date = serializers.DateField()


class DeptSerializer(ModelSerializer):

    company = CompanySerializer(read_only=True)

    class Meta:
        model = Dept
        fields = '__all__'

class DeptADDSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    location = serializers.CharField(max_length=255)
    phone = serializers.CharField(max_length=13)
    start_date = serializers.DateField()
    end_date = serializers.DateField()

class ExpensesSerializer(ModelSerializer):

    company = CompanySerializer(read_only=True)

    class Meta:
        model = Expenses
        fields = '__all__'


class ExpensesADDSerializer(serializers.Serializer):
    user_name = serializers.CharField(max_length=255)
    expenses_name = serializers.CharField(max_length=255)
    summa = serializers.FloatField(default=0)
    additional = serializers.FloatField(default=0)
    date = serializers.DateField()


class CompanySerializer(ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class CompanyADDSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    location = serializers.CharField(max_length=255)



