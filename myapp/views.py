from django.shortcuts import render ,redirect
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate ,login, logout
from .models import *
# Create your views here.
#import meaasge
from django.contrib import messages



# def loginView(request):

#     if request.method == 'POST':

#         user

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def registerViewform(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        profile_pic = request.FILES.get('profile_picture')

        if password != confirm_password:
            return redirect ("registerpage")

        createuser = User.objects.create_user(username = username , email = email , password = password )

        createuser.save()















        return redirect('loginpage')






def indexView(request):
    

    productis = Products.objects.all()

    if request.user.is_authenticated:

        cartis , created = UserCart.objects.get_or_create(user = request.user) 

       
        addtocart_count = CartItems.objects.filter(cart = cartis.id).count()
    else:
        addtocart_count = 0


    context = {
        'productdata':productis,
        
    }

    return render( request,'pages/indexpage.html',context)



from django.http import JsonResponse
@csrf_exempt
def cartcountByJSView(request):

    if request.user.is_authenticated:

        print("Request is Comming ")

        cartis, created = UserCart.objects.get_or_create(
            user=request.user
        )

        addtocart_count = CartItems.objects.filter(
            cart=cartis
        ).count()

        return JsonResponse({
            'status': True,
            'addtocart_count': addtocart_count
        })

    return JsonResponse({
        'status': False,
        'message': 'User not authenticated'
    })
    







@csrf_exempt
def loginView(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request , username = username , password = password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('indexpage')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('loginpage')
            
    return render(request , 'pages/loginpage.html')


@csrf_exempt
def logoutView(request):
    logout(request)
    return redirect('loginpage')



def registerView(request):
    return render(request, 'pages/registerpage.html')

@csrf_exempt
def viewProductDetailsView(request, product_id):

    product_is = Products.objects.get(id = product_id)
    cartis , created = UserCart.objects.get_or_create(user = request.user) 
    
           
    addtocart_count = CartItems.objects.filter(cart = cartis.id).count()

    context ={
        'productdata':product_is,
        
    }

    return render(request , 'pages/viewproductdetails.html',context)



@csrf_exempt
def AddTocartView(request , product_id):
    if request.user.is_authenticated:

        cartis , created = UserCart.objects.get_or_create(user = request.user) 

        cartitemis , productcreated = CartItems.objects.get_or_create(cart = cartis , product_id = product_id)

        if not  productcreated :
            cartitemis.quantity = cartitemis.quantity  +1
            cartitemis.save()


        return redirect('indexpage')

    else:
        return redirect('loginpage')



from decimal import Decimal
@csrf_exempt 
def ShowCartItemsView(request):

    if request.user.is_authenticated:

        cartis , created = UserCart.objects.get_or_create(user = request.user)

        cartitemis = CartItems.objects.filter(cart = cartis.id)

        total_price = Decimal("0.00")
        for item in cartitemis:
            item.item_total_price = item.quantity * item.product.price
            total_price += item.item_total_price
        context ={

            'cartitemsdata':cartitemis,
            'total_price':total_price
        }

        return render(request , 'pages/showcartitems.html',context)






@csrf_exempt
def PlacedOrderView(request):
    if not request.user.is_authenticated:

        return redirect('loginpage')

    if request.method == "POST":

        product_id = request.POST.get("productid")
        qty = request.POST.get("qty")
        total_amt = request.POST.get("totalamount")
        paid_amt = request.POST.get("paid_amount")


        payment_method = request.POST.get("payment_method")

        productis = Products.objects.get(id = product_id)

        if not productis:
            messages.error(request, 'Product not Found')
            return redirect ('indexpage')

        create_order = PlacedOrder.objects.create(
            user_name = request.user.username,
            user= request.user,
            products_name = productis.product_name,
            product = productis,
            qty = qty,
            total_amount = total_amt,
            paid_amount = paid_amt,
            payment_method = payment_method,

        )
        CartItems.objects.filter(cart=request.user.usercart , product=product_id).delete()

        messages.success(request, 'OrderPlaced successfually ')
        return redirect ('indexpage')




def  ViewOrdersDetailsView(request):
    if not request.user.is_authenticated:
        return redirect('loginpage')

    orders = PlacedOrder.objects.filter(user = request.user)

    context = {
        'ordersdata':orders
    }

    return render(request, 'pages/myordersdetails.html',context)

    


    

