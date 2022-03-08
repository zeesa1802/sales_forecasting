from django.contrib import admin

# from .models import Author, Post, Tag, Comment
from .models import Category, Product, Transaction, Invoice


# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("category_id","category_name", "date",)

class ProductAdmin(admin.ModelAdmin):
    list_display = ("product_id", "product_name", "price", "quantity","reorder_level","expiry_date","category",)


class TransactionAdmin(admin.ModelAdmin):
    list_display = ("transaction_id", "transaction_products_id","transaction_products_name", "transaction_products_price", "transaction_products_quantity", "transaction_totalamount",)


class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("created_date","data",)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Invoice, InvoiceAdmin)



# Register your models here.
