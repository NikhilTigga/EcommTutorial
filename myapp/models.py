from django.db import models

# Create your models here.


class Products(models.Model):

    user = models.ForeignKey('auth.User', on_delete = models.CASCADE)
    product_name = models.CharField(max_length = 200)
    descriotion = models.TextField()
    qty = models.IntegerField(default = 1)

    product_image = models.ImageField(upload_to = 'product_images/', blank = True , null = True)

    price = models.DecimalField(max_digits = 10 , decimal_places =2)

    crated_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.product_name


class UserCart(models.Model):

    user = models.OneToOneField('auth.User', on_delete = models.CASCADE)
    created_at = models.DateField(auto_now_add = True)

    def __str__(self):
        return self.user.username


class CartItems(models.Model):

    cart = models.ForeignKey(UserCart , on_delete = models.CASCADE)

    product = models.ForeignKey(Products , on_delete = models.CASCADE)

    quantity = models.IntegerField(default = 1)



class PlacedOrder(models.Model):

    PAYMENT_CHOICE =[
        ("cod","COD"),
        ("online","Online")
    ]


    user_name = models.CharField(max_length=200)
    user = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True , blank=True)
    products_name = models.CharField(max_length=200)
    product = models.ForeignKey(Products, on_delete=models.SET_NULL, null=True , blank=True )
    qty = models.IntegerField(default=1)
    total_amount = models.DecimalField(max_digits=10,decimal_places=2 )
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2)

    payment_method = models.CharField(max_length=200, choices= PAYMENT_CHOICE ,default="cod")
