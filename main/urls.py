from django.urls import path
from .views import *


urlpatterns = [
    # -----  ----- #
    path('sign-in/', sign_in),
    path('sign-up/', sign_up),
    path('logout/', user_logout),
    # ------- ----- #
    # -------------#
    path('category/',category_view),
    path('category_add/',category_add),
    path('category_change/<int:id>/',category_change),
    path('category_del/<int:id>/',category_del),
    # -------------#
    # -------------#
    path('product/',products_view),
    path('product_add/',product_add),
    path('product_change/<int:id>/',product_change),
    path('product_del/<int:id>/',product_del),
    # -------------#
    # -------------#
    path('customer/',customer_view),
    path('customer_add/',customer_add),
    path('customer_change/<int:id>/',customer_change),
    path('customer_del/<int:id>/',customer_del),
    # -------------#
    # -------------#
    path('dept/',dept_view),
    path('dept_add/',dept_add),
    path('dept_change/<int:id>/',dept_change),
    path('dept_del/<int:id>/',dept_del),
    # -------------#
    # -------------#
    path('expenses/',expenses_view),
    path('expenses_add/',expenses_add),
    path('expenses_change/<int:id>/',expenses_change),
    path('expenses_del/<int:id>/',expenses_del),
    # -------------#
]