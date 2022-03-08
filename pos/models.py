
from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL
from django.utils.text import slugify
from django.core.validators import MinLengthValidator

# Create your models here.
class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    date = models.DateField(editable=False)
    category_name = models.CharField(max_length=50)
    # is_active = models.BooleanField()
    def __str__(self):
        return self.category_name



class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=100)
    price = models.IntegerField()
    quantity = models.IntegerField()
    reorder_level = models.IntegerField()
    expiry_date = models.DateField()
   
    
    
    
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name="product")
    

    def __str__(self):
        return self.product_name




class Transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    transaction_products_id = models.CharField(max_length=1000)
    transaction_products_name = models.CharField(max_length=1000)
    transaction_products_price = models.CharField(max_length=100)
    transaction_products_quantity = models.CharField(max_length=100)
    transaction_totalamount = models.FloatField()

    def __str__(self):
        return self.transaction_products_name


class Invoice(models.Model):
    # id = models.AutoField()
    # name = models.CharField(max_length=15)
    created_date = models.DateTimeField(auto_now=True)
    data = models.JSONField()