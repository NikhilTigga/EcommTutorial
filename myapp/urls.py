
from django.urls import path

from .views import *

urlpatterns =[

    path('', indexView , name='indexpage'),

    path('registerviewform/',registerViewform, name='registerviewform'),

    path('login/',loginView, name ='loginpage'),

    path('register/',registerView , name='registerpage'),

    path('logout/',logoutView , name = "logoutpage"),

    path('viewProductDetailsView/<int:product_id>/',viewProductDetailsView , name = "viewProductDetailsView"),

    path('add_to_cart/<int:product_id>/',AddTocartView ,name = "AddTocartView"),

    path('showcartitems/',ShowCartItemsView , name = "showcartitems"),

    path('cartcountByJSView/',cartcountByJSView , name ="cartcountByJSView"),

    path('placedOrderView/',PlacedOrderView, name="placedOrderView"),

    path('myordersdetails', ViewOrdersDetailsView , name = "myordersdetails"),

    
]