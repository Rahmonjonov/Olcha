from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from .models import *
from django.contrib.auth import logout, authenticate, login
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializer import *


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

@swagger_auto_schema(method='post', request_body=LoginSerializer, tags=['Auth'])
@api_view(['POST'])
def sign_in(request):
    try:
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = request.data['username']
            password = request.data['password']
            user_get = User.objects.get(username=username)
            user = authenticate(username=username, password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                data = {
                        'id': user_get.id,
                        'username': username,
                        'is_director': user_get.is_director,
                        'limit':user_get.limit,
                        'token': token,
                        'status':user_get.company.rate
                        }
                login(request, user)
                return Response(data, status.HTTP_200_OK)
            else:
                return Response({'Messages': 'Username or password is incorrect !'}, status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(status=400, data={'Messages': serializer.errors})
    except Exception:
         return Response({'Messages': 'Error'}, status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(method='post', request_body=UserCreateSerializer,tags=['Auth'])
@api_view(['POST'])
def sign_up(request):
    try:
        data = request.data
        company  = Company.objects.create(
            name = data.get('name'),
            location = data.get('location'),
        )
        company.save()
        User.objects.create_user(
            username=data.get('username'),
            password=data.get('password'),
            phone=data.get('phone'),
            is_director=data.get('is_director', False),
            company=company

        )
        return Response({"Messages": 'Success'}, status=status.HTTP_201_CREATED)
    except Exception as err :
        return Response({'Messages': 'Error'}, status=status.HTTP_401_UNAUTHORIZED)

@swagger_auto_schema(method='get', tags=['Auth'])
@api_view(['GET'])
def user_logout(request):
    try:
        logout(request)
        return Response({"Messages": 'Success'}, status=status.HTTP_200_OK)
    except Exception:
        return Response({'data': 'Error messages'}, status=status.HTTP_400_BAD_REQUEST)

"""  Category View  """

@swagger_auto_schema(method='get', tags=['Category'])
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def category_view(request):
    category = Category.objects.filter(company=request.user.company)
    serializer = CategorySerializer(category, many=True).data
    return Response(serializer, status=status.HTTP_200_OK)


@swagger_auto_schema(method='post', request_body=CategoryADDSerializer, tags=['Category'])
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def category_add(request):
    try:
        data = request.data
        Category.objects.create(
            company=request.user.company,
            name=data.get('name'),
            image=data.get('image'),
        )
        return Response({"Messages": 'Success'}, status=status.HTTP_201_CREATED)
    except Exception:
        return Response({'data': 'error messages'}, status=status.HTTP_401_UNAUTHORIZED)

@swagger_auto_schema(method='put', request_body=CategoryADDSerializer, tags=['Category'])
@api_view(['PUT'])
def category_change(request, id):
    data = request.data
    category = Category.objects.get(id=id)
    if data.get('image') is not None:
        category.image = data.get('image')
    category.name=data.get('name')
    category.save()
    return Response({"Messages": 'Success'}, status=status.HTTP_200_OK)


@swagger_auto_schema(method='delete',  tags=['Category'])
@api_view(['DELETE'])
def category_del(request, id):
    Category.objects.get(id=id).delete()
    return Response({"Messages": 'Success'}, status=status.HTTP_200_OK)


"""  Category View  """


"""  Product  View  """

@swagger_auto_schema(method='get',  tags=['Product'])
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def products_view(request):
    category = Products.objects.filter(company=request.user.company)
    serializer = ProductsSerializer(category, many=True).data
    return Response(serializer, status=status.HTTP_200_OK)

@swagger_auto_schema(method='post', request_body=ProductADDSerializer, tags=['Product'])
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def product_add(request):
    try:
        data = request.data
        Products.objects.create(
            company=request.user.company,
            name=data.get('name'),
            bar_code=data.get('bar_code'),
            category_id=data.get('category'),
            body_price=data.get('body_price'),
            price=data.get('price'),
            amount=data.get('amount'),
        )
        return Response({"Messages": 'Success'}, status=status.HTTP_201_CREATED)
    except Exception:
        return Response({'data': 'error messages'}, status=status.HTTP_401_UNAUTHORIZED)

@swagger_auto_schema(method='put', request_body=ProductADDSerializer, tags=['Product'])
@api_view(['PUT'])
def product_change(request, id):
    data = request.data
    Products.objects.filter(id=id).update(
        name=data.get('name'),
        bar_code=data.get('bar_code'),
        category_id=data.get('category'),
        body_price=data.get('body_price'),
        price=data.get('price'),
        amount=data.get('amount'),
    )
    return Response({"Messages": 'Success'}, status=status.HTTP_200_OK)

@swagger_auto_schema(method='put', tags=['Product'])
@api_view(['PUT'])
def product_del(request, id):
    Products.objects.get(id=id).delete()
    return Response({"Messages": 'Success'}, status=status.HTTP_200_OK)

"""  Product  View  """

"""  Customer  View  """


@swagger_auto_schema(method='get', tags=['Customer'])
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def customer_view(request):
    category = Customer.objects.filter(company=request.user.company)
    serializer = CustomerSerializer(category, many=True).data
    return Response(serializer, status=status.HTTP_200_OK)


@swagger_auto_schema(method='post', request_body=CustomerADDSerializer, tags=['Customer'])
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def customer_add(request):
    try:
        data = request.data
        Customer.objects.create(
            company=request.user.company,
            name=data.get('name'),
            phone=data.get('phone'),
            summa=data.get('summa'),
            locaiton=data.get('locaiton'),
            start_date=data.get('start_date'),
            end_date=data.get('end_date'),
        )
        return Response({"Messages": 'Success'}, status=status.HTTP_201_CREATED)
    except Exception:
        return Response({'data': 'error messages'}, status=status.HTTP_401_UNAUTHORIZED)


@swagger_auto_schema(method='put', request_body=CustomerADDSerializer, tags=['Customer'])
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def customer_change(request, id):
    try:
        data = request.data
        Customer.objects.filter(id=id).update(
            name=data.get('name'),
            phone=data.get('phone'),
            summa=data.get('summa'),
            start_date=data.get('start_date'),
            end_date=data.get('end_date'),
            locaiton=data.get('locaiton'),
        )
        return Response({"Messages": 'Success'}, status=status.HTTP_200_OK)
    except Exception:
        return Response({'data': 'error messages'}, status=status.HTTP_401_UNAUTHORIZED)
    

@swagger_auto_schema(method='delete',  tags=['Customer'])
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def customer_del(request, id):
    Customer.objects.get(id=id).delete()
    return Response({"Messages": 'Success'}, status=status.HTTP_200_OK)

"""  Customer  View  """


"""  Dept  View  """

@swagger_auto_schema(method='get', tags=['Dept'])
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dept_view(request):
    category = Dept.objects.filter(company=request.user.company)
    serializer = DeptSerializer(category, many=True).data
    return Response(serializer, status=status.HTTP_200_OK)

@swagger_auto_schema(method='post', request_body=DeptADDSerializer, tags=['Dept'])
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def dept_add(request):
    try:
        data = request.data
        Dept.objects.create(
            company=request.user.company,
            name=data.get('name'),
            location=data.get('location'),
            phone=data.get('phone'),
            start_date=data.get('start_date'),
            end_date=data.get('end_date'),
            date_time=data.get('date_time'),
        )
        return Response({"Messages": 'Success'}, status=status.HTTP_201_CREATED)
    except Exception:
        return Response({'data': 'error messages'}, status=status.HTTP_401_UNAUTHORIZED)



@swagger_auto_schema(method='put', request_body=DeptADDSerializer, tags=['Dept'])
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def dept_change(request, id):
    try:
        data = request.data
        Dept.objects.filter(id=id).update(
            company=request.user.company,
            name=data.get('name'),
            location=data.get('location'),
            phone=data.get('phone'),
            start_date=data.get('start_date'),
            end_date=data.get('end_date'),
            date_time=data.get('date_time'),
        )
        return Response({"Messages": 'Success'}, status=status.HTTP_200_OK)
    except Exception:
        return Response({'data': 'error messages'}, status=status.HTTP_401_UNAUTHORIZED)

@swagger_auto_schema(method='delete',  tags=['Dept'])
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def dept_del(request, id):
    Dept.objects.get(id=id).delete()
    return Response({"Messages": 'Success'}, status=status.HTTP_200_OK)

"""  Dept  View  """

"""  Expenses  View  """

@swagger_auto_schema(method='get',  tags=['Expenses'])
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def expenses_view(request):
    category = Expenses.objects.filter(company=request.user.company)
    serializer = ExpensesSerializer(category, many=True).data
    return Response(serializer, status=status.HTTP_200_OK)


@swagger_auto_schema(method='post', request_body=ExpensesADDSerializer, tags=['Expenses'])
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def expenses_add(request):
    try:
        data = request.data
        Expenses.objects.create(
            company=request.user.company,
            user_name=data.get('user_name'),
            expenses_name=data.get('expenses_name'),
            summa=data.get('summa'),
            additional=data.get('additional'),
            date=data.get('date'),
        )
        return Response({"Messages": 'Success'}, status=status.HTTP_201_CREATED)
    except Exception:
        return Response({'data': 'error messages'}, status=status.HTTP_401_UNAUTHORIZED)
    

@swagger_auto_schema(method='put', request_body=ExpensesADDSerializer, tags=['Expenses'])
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def expenses_change(request, id):
    try:
        data = request.data
        Expenses.objects.filter(id=id).update(
            company=request.user.company,
            user_name=data.get('user_name'),
            expenses_name=data.get('expenses_name'),
            summa=data.get('summa'),
            additional=data.get('additional'),
            date=data.get('date'),
        )
        return Response({"Messages": 'Success'}, status=status.HTTP_200_OK)
    except Exception:
        return Response({'data': 'error messages'}, status=status.HTTP_401_UNAUTHORIZED)

@swagger_auto_schema(method='delete',  tags=['Expenses'])
@api_view(['DELETe'])
@permission_classes([IsAuthenticated])
def expenses_del(request, id):
    Expenses.objects.get(id=id).delete()
    return Response({"Messages": 'Success'}, status=status.HTTP_200_OK)


"""  Expenses  View  """


"""  Company  View  """


@swagger_auto_schema(method='get', tags=['Company'])
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def company_view(request):
    category = Company.objects.filter(company=request.user.company)
    serializer = CompanySerializer(category, many=True).data
    return Response(serializer, status=status.HTTP_200_OK)

@swagger_auto_schema(method='put', request_body=CompanyADDSerializer, tags=['Company'])
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def company_change(request, id):
    try:
        data = request.data
        Company.objects.filter(id=id).update(
            name=data.get('name'),
            location=data.get('location'),
        )
        return Response({"Messages": 'Success'}, status=status.HTTP_200_OK)
    except Exception:
        return Response({'data': 'error messages'}, status=status.HTTP_401_UNAUTHORIZED)


"""  Company  View  """


@swagger_auto_schema(method='get', tags=['Tarif'])
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def rate_view(request):
    rate = Rates.objects.all()
    serializer = RatesSerializer(rate, many=True).data
    return Response(serializer, status=status.HTTP_200_OK)
