from random import randint
from django.http.response import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from pandas.io import parsers

from .forms import CategoryForm, CreateUserForm, ProductForm, RestockProductForm
from .models import Category, Product, Transaction, Invoice
from datetime import datetime

from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User

from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError

from datetime import datetime
import datetime


import numpy as np
from apyori import apriori
from dateutil import relativedelta

import datetime

import pandas as pd

from random import seed
from random import randint
import warnings
import random
from pmdarima.arima import auto_arima
warnings.filterwarnings("ignore")

# Create your views here.

@login_required
def home(request):

    get_obj = Invoice.objects.all()
    
    name_list = []
    qty_list = []
    price_list = []
    amount_list = []
    id_list = []
    date_list = []
    item_code_list = []
    
    print("overall")
    
    for obj in get_obj:
        length = len(obj.data['name'])
        i = 0
        empty_id_list = []
        empty_date_list = []
        while i < length-1:
            empty_id_list.append(str(obj.id))
            date = obj.created_date
            date = datetime.datetime.strftime(date, "%d-%m-%Y %H:%M:%S")
            empty_date_list.append(str(date))
            i = i+1
        
        empty_id_list.append('')
        empty_date_list.append('')
        id_list.append(empty_id_list)
        date_list.append(empty_date_list)

    # print(id_list)

    print(date_list)
    print(id_list)

    
    for obj in get_obj:
        i = 0
        name_list.append(obj.data['name'])


    for obj in get_obj:

        qty_list.append(obj.data['qty'])

    for obj in get_obj:
        price_list.append(obj.data['price'])
    
    for obj in get_obj:
        amount_list.append(obj.data['amount'])
    
    for obj in get_obj:
        item_code_list.append(obj.data['item_code'])



 
    print(name_list)
    print(qty_list)
    print(price_list)
    print(amount_list)
    print("code_list")
    print(item_code_list)

    date_list_flat = flat_list(date_list)
    id_list_flat = flat_list(id_list)
    name_list_flat = flat_list(name_list)
    qty_list_flat = flat_list(qty_list)
    price_list_flat = flat_list(price_list)
    amount_list_flat = flat_list(amount_list)
    item_code_list_flat = flat_list(item_code_list)


    df = pd.DataFrame(list(zip(date_list_flat, id_list_flat,item_code_list_flat, name_list_flat, qty_list_flat, price_list_flat, amount_list_flat)),
               columns =['Inv_date', 'Inv_id', 'Item_code', 'Item', 'Qty', 'Rate', 'Amount'])

    df=df.fillna('')

    df.set_index('Inv_date',inplace=True)
    df.to_csv('all_invoices.csv')

    df = pd.read_csv('all_invoices.csv')
    df_mini = pd.read_csv('dataset_2.csv')

    df.drop(['Inv_id'], axis=1, inplace=True)
    df['Inv_date'] = pd.to_datetime(df['Inv_date'],dayfirst=True).dt.date
    df['Inv_date'] = pd.to_datetime(df['Inv_date'],dayfirst=True)
    df.dropna(inplace=True)
    df['Rate'] = df['Rate'].astype(float)

    df_mini.drop(['Party', 'Name'], axis=1, inplace=True)
    df_mini.dropna(inplace=True)
    df_mini['Inv_date'] = pd.to_datetime(df_mini['Inv_date'],dayfirst=True)

    df = df_mini.append(df)

    df.to_csv('home.csv')

    df2 = df
    # df2 = pd.read_csv('dataset_2.csv')
    df2.dropna(inplace=True)

    df2.Inv_date = pd.to_datetime(df2['Inv_date'], dayfirst=True)
    df2.set_index('Inv_date', inplace=True)

    df2['Total_Amount'] = df2['Qty'] * df2['Rate']
    df2 = df2.groupby(pd.Grouper(freq='M')).Total_Amount.sum().astype(int).to_frame()

    df2.reset_index(inplace=True)
    df2['Inv_date'] = df2['Inv_date'].dt.strftime('%b %Y')

    df2 = df2.tail(7)

    labels = list(df2['Inv_date'])
    data = list(df2['Total_Amount'])
    # invoices = Invoice.objects.raw(
    #     "select created_date from pos_invoice where created_date < date() ")
    # invoices = Invoice.objects.filter(created_date__='2021-12-05')
    # print(invoices)
    qty_list = []
    get_obj = Invoice.objects.all()    

    for obj in get_obj:
        qty_list.append(obj.data['qty'])
    

    flat_list_qty = []
    for sublist in qty_list:
        for item in sublist:
            if item != '':
                flat_list_qty.append(item)
    
    print(flat_list_qty)
    total_qty = 0

    for qty in flat_list_qty:
        # print(len(qty))
        total_qty = int(qty) + total_qty

    # print(total_qty)



    product_list = []
    get_obj = Invoice.objects.all()    

    for obj in get_obj:
        product_list.append(obj.data['name'])
    

    flat_list_product = []
    for sublist in product_list:
        for item in sublist:
            flat_list_product.append(item)
    
    df = pd.DataFrame()
    df['items'] = flat_list_product

    df_unique = df['items'].nunique()
    print(df_unique)

    # total_products = len(df)

    

    # print(total_products)
    # print(len(invoices))
    # print(request.user.username)
    user = request.user
    # if request.user.is_authenticated:
    # else:
    #     return redirect('login')
    total_products = Product.objects.all().count()
    total_categories = Category.objects.all().count()
    total_low_stock = Product.objects.raw(
        "select * from pos_product where reorder_level > quantity ORDER BY reorder_level")

    total_low_stock = len(total_low_stock)

    return render(request, 'pos/home.html', context={
        'total_products': total_products,
        'total_categories': total_categories,
        'user': user,
        'unique_products': df_unique,
        'total_qty': total_qty,
        'total_low_stock': total_low_stock,
        'labels': labels,
        'data': data
         })

    # print("super")
    # 	return redirect('home')


# def register(request):
#     form = UserCreationForm()

#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return render(request, 'pos/login.html')


#     return render(request, 'pos/register.html', {
#         'form':form
#     })

def register(request):
    if not request.user.is_superuser:
        return redirect('home')
    # if request.user.is_authenticated:
    # 	return redirect('home')
    # else:
    form = CreateUserForm()
    if request.method == 'POST':
        # print("sasassas")
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)
            return redirect('user-config')

    context = {'form': form}
    return render(request, 'pos/register.html', context)


def login_page(request):
    # if request.user.is_authenticated:
    #     return redirect('home')
    # else:
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request, 'pos/home.html', context)

    # return render(request, 'pos/login.html')




# Models
# def category(request):
#     return HttpResponse("Category")
@login_required
def all_categories(request):
    if not request.user.is_superuser:
        return redirect('home')
    # categories = Category.objects.all().order_by("-date")[:3]
    get_categories = Category.objects.all()
    return render(request, "pos/all_categories.html", {
        "categories": get_categories
    })


@login_required
def add_category(request):
    if not request.user.is_superuser:
        return redirect('home')
    user = request.user
    if user.is_superuser:
        pass
    else:
        return redirect('home')

    # categories = Category.objects.all().order_by("-date")[:3]

    if request.method == "POST":
        special_characters = '"!@#$%^&*()-+?_=,<>/0123456789"'
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = request.POST['category_name']
            if(not any(c in special_characters for c in category_name)):

                # name = Category.objects.filter(category_name__iexact=category_name)
                # print(name)
                if(Category.objects.filter(category_name__iexact=category_name)):
                    print("True")
                    messages.error(request, 'Category already exist.')
                    
                    return redirect('add-category')
                    # return render(request, 'pos/add_category.html', {
                    #     'error': "Category already exist"
                    # })
                else:
                    category_date = request.POST.get('date')
                # category_is_active = request.POST.get('category_name')
                    category_obj = Category(
                        date=category_date, category_name=category_name)
                    category_obj.save()
                    messages.success(request, 'Add Category request submitted successfully.')

                    return redirect('add-category')
            else:
                messages.error(request, 'Invalid category.')
                return render(request, 'pos/add_category.html', {
                    'error': "invalid category"
                })
        messages.error(request, form.errors)

            # name

            # name = Category.objects.filter(category_name=category_name)
            # # print(type(name))

            # if(Category.objects.filter(category_name=category_name)):
            #     print("dasdsads")
            #     name = Category.objects.filter(category_name=category_name)
            #     if name[0].category_name.lower() == category_name.lower():

            #         return render(request, 'pos/add_category.html',{
            #             'error': "Category already exist"
            #     })
            # # print(name[0].category_name)
            # # print(name[0].category_name)

            # else:
            #     category_name = request.POST.get('category_name')
            #     category_date = request.POST.get('date')
            #     # category_is_active = request.POST.get('category_name')
            #     category_obj = Category(date=category_date, category_name=category_name)
            #     category_obj.save()

            #     return redirect('all-category')

            # else:
            #     category_name = request.POST.get('category_name')
            #     category_date = request.POST.get('date')
            #     # category_is_active = request.POST.get('category_name')
            #     category_obj = Category(date=category_date, category_name=category_name)
            #     category_obj.save()

            #     return redirect('all-category')

    else:
        form = CategoryForm()
        messages.error(request, form.errors)
        
    return render(request, "pos/add_category.html", {
        'form': form,
    })


@login_required
def all_product(request):
    if not request.user.is_superuser:
        return redirect('home')
    get_products = Product.objects.all()
    return render(request, 'pos/all_products.html', {
        "products": get_products
    })


@login_required
def add_product(request):
    if not request.user.is_superuser:
        return redirect('home')
    # categories = Category.objects.all().order_by("-date")[:3]

    categories = Category.objects.all()

    # product_name = request.POST.get('product_name')
    # product_price = request.POST.get('product_price')
    # product_quantity = request.POST.get('product_quantity')
    # product_category = request.POST.get('product_category')

    # category_obj = Category(date=datetime.date(datetime.now()), category_name="yyyyyy")
    # category_obj = Category.objects.all()[0]
    # product_obj = Product(product_name="sasas", price=22, quantity=123,
    # category=category_obj)

    # product_obj.save()
    # return HttpResponse("Contact")
    # return redirect('all-product')

    if request.method == "POST":
        product_name = request.POST['product_name']
        product_price = request.POST['product_price']
        product_quantity = request.POST['product_quantity']
        reorder_level = request.POST['reorder_level']
        expiry_date = request.POST['expiry_date']
        product_category = request.POST['product_category']
        special_characters = '"!@#$%^&*()-+?_=,<>/"'
        

        form = ProductForm(request.POST)
        if form.is_valid():
            # product_name = request.POST['product_name']
            if(not any(c in special_characters for c in product_name)):

               
                if(Product.objects.filter(product_name__iexact=product_name)):
                    messages.error(request, 'Product already exist.')
                    return render(request, 'pos/add_product.html', {
                        'error': "Product already exist",
                        'categories': categories,
                        'product_name': product_name,
                        'product_price': product_price,
                        'product_quantity': product_quantity,
                        'reorder_level': reorder_level,
                        'expiry_date': expiry_date,
                    })
                else:

                    e = []
                    l = []

                    # product_name = request.POST.get('product_name')
                    # product_price = request.POST.get('product_price')
                    # product_quantity = request.POST.get('product_quantity')
                    # product_category = request.POST.get('product_category')
                    # reorder_level = request.POST.get('reorder_level')
                    # expiry_date = request.POST.get('expiry_date')
                    # print(expiry_date)

                    e = expiry_date.split("-")
                    l = str(datetime.date.today()).split("-")

                    if int(e[2]) - int(l[2]) >= 3 and int(e[0]) >=2022:
                        

                    # print(int(expiry_date))
                    # print(type(datetime.date.today()))
                    # l_date = datetime.date.today()
                    # # delta = f_date - l_date
                    
                    # if(delta.days >= 3):


                # print(product_category)

                        category_obj = Category.objects.get(
                        category_name=product_category)

                # category_obj = Category.objects.all()[1]
                        product_obj = Product(product_name=product_name, price=product_price, quantity=product_quantity, reorder_level= reorder_level, expiry_date=expiry_date,
                                      category=category_obj)

                        product_obj.save()
                        messages.success(request, 'Product saved successfully.')
                        return redirect('add-product')
                    else:

                        messages.error(request, 'Invalid product expiry date.')
                        # return redirect('add-product')
                        return render(request, 'pos/add_product.html', {
                        # 'error': "Invalid expiry date",
                        'categories': categories,
                        'product_name': product_name,
                        'product_price': product_price,
                        'product_quantity': product_quantity,
                        'reorder_level': reorder_level,
                        'expiry_date': expiry_date,
                    })
            else:
                messages.error(request, 'Invalid product name.')
                return render(request, 'pos/add_product.html', {
                        # 'error': "Invalid product_name",
                        'categories': categories,
                        'product_name': product_name,
                        'product_price': product_price,
                        'product_quantity': product_quantity,
                        'reorder_level': reorder_level,
                        'expiry_date': expiry_date,
                    })
        messages.error(request, form.errors)
    else:
        form = ProductForm()

    return render(request, "pos/add_product.html", {
        'form': form,
        'categories': categories,
        # 'product_name': product_name,   
        # 'product_price': product_price,
        # 'product_quantity': product_quantity,
        # 'reorder_level': reorder_level,
        # 'expiry_date': expiry_date,
    })


@login_required
def user_config(request):
    if not request.user.is_superuser:
        return redirect('home')
    users = User.objects.all()
    # print(users.last())
    return render(request, "pos/user_config.html", {
        'users': users,
    })


@login_required
def edit(request, username):
    if not request.user.is_superuser:
        return redirect('home')
    # print('invoke')
    user1 = User.objects.get(username=username)

    # print(user.username)

    return render(request, 'pos/edit.html', {'user1': user1})


@login_required
def update(request, username):
    if not request.user.is_superuser:
        return redirect('home')

    user = User.objects.get(username=username)
    # print(user.password)
    form = CreateUserForm(request.POST, instance=user)
    # print("above")
    # print(form.is_valid)
    if form.is_valid():
        # print("inside")
        form.save()
        return redirect("user-config")
    
    
    return render(request, 'pos/edit.html', {'form':form, 'user1':user})


@login_required
def destroy(request, username):
    if not request.user.is_superuser:
        return redirect('home')
    user = User.objects.get(username=username)
    user.delete()
    return redirect("user-config")


@login_required
def create_order(request):
    products = Product.objects.all()
    return render(request, "pos/create_order.html", {'products': products})


# Add Data for Create Order

@login_required
@csrf_exempt
def add_data(request):
    
    if request.method == "POST":
        id = request.POST.get('sid')
        # print(id)
        product = Product.objects.get(pk=id)
        product_data = {"id": product.product_id,
                        "name": product.product_name, "price": product.price}
        return JsonResponse(product_data)


@login_required
@csrf_exempt
def transaction(request):
    get_transactions = Transaction.objects.all()

    # counter = Transaction.objects.last().transaction_id
    transaction_id_list = []
    transaction_products_name_list = []
    transaction_products_price_list = []
    transaction_products_quantity_list = []
    transaction_totalamount_list = []

    
    for get_transaction in get_transactions:


        transaction_id_list.append(get_transaction.transaction_id)
        transaction_products_name_list.append(
            get_transaction.transaction_products_name.split(","))
        transaction_products_price_list.append(
            get_transaction.transaction_products_price.split(","))
        transaction_products_quantity_list.append(
            get_transaction.transaction_products_quantity.split(","))
        transaction_totalamount_list.append(
            get_transaction.transaction_totalamount)


    return render(request, "pos/transaction.html", {"transactions": get_transactions, "transaction_id_list": transaction_id_list, "transaction_products_name_list": transaction_products_name_list, "transaction_products_price_list": transaction_products_price_list,
                                                    "transaction_products_quantity_list": transaction_products_quantity_list, "transaction_totalamount_list": transaction_totalamount_list})

    

@login_required
@csrf_exempt
def save_invoice(request):
    if request.method == "POST":

        transaction_products_name_list = []
        transaction_products_quantity_list = []
        transaction_product_id = request.POST.get('product_id')
        transaction_product_name = request.POST.get('product_name')
        transaction_product_price = request.POST.get('product_price')
        transaction_product_quantity = request.POST.get('product_quantity')
        transaction_product_amount = request.POST.get('product_amount')
        transaction_total_amount = request.POST.get('total_amount')
        # print(transaction_total_amount)
        id_list = transaction_product_id.split(",")
        name_list = transaction_product_name .split(",")
        qty_list = transaction_product_quantity.split(",")
        price_list = transaction_product_price.split(",")
        amount_list = transaction_product_amount.split(",")
        # total_amount = transaction_total_amount.split(",")

        # print("ammount list")
        # print(amount_list)


        i = 0

        for id in id_list:
            # print("id_loop")
            get = Product.objects.get(product_id=id)
            updated_quantity = get.quantity - int(qty_list[i])
            get.quantity = updated_quantity
            get.save()

            # get.update(quantity=updated_quantity)
            i = i + 1
        
        # total = 0
        # for amount in amount_list:
        #     total = total + int(amount)

        id_list.append('')
        name_list.append('')
        qty_list.append('')
        price_list.append('Total')
        amount_list.append(transaction_total_amount)
        # amount_list.append(total)

        print(id_list)
        print(name_list)
        print(qty_list)
        print(price_list)
        print(amount_list)


        dict = {
            'item_code': id_list,
            'name': name_list,
            'qty': qty_list,
            'price': price_list,
            'amount': amount_list
        }

        obj = Invoice(data=dict)
        obj.save()
        print("save")
        messages.success(request, 'Transaction saved successfully.')
        # transaction_obj = Transaction(transaction_products_name = transaction_product_name, transaction_products_price = transaction_product_price, transaction_products_quantity = transaction_product_quantity, transaction_totalamount = transaction_total_amount)

        # transaction_products_name_list = transaction_obj.transaction_products_name.split(",")
        # transaction_products_quantity_list = transaction_obj.transaction_products_quantity.split(",")

        # get_products = Product.objects.all()

        # for pn in range(len(transaction_products_name_list)):
        #     for products in get_products:
        #         if(transaction_products_name_list[pn] == products.product_name):
        #             products.quantity = products.quantity - int(transaction_products_quantity_list[pn])
        #             products.save()
        # transaction_obj.save()

        return render(request, 'pos/all_invoices.html')

@login_required
def get_transaction(request):
    

    # user_input = request.GET.get('name')
    # print(user_input)
    get_obj = Invoice.objects.all()
    # date1 = get_obj[0].created_date
    # date1 = datetime.datetime.strftime(date1,"%Y-%m-%d %H:%M:%S")
    # print(date1)
    # date = datetime.datetime.now().replace(microsecond=0)
    # print(date)
    # print(get_obj[0].data)
    # get_obj[0].delete()
    # Iterate over all key-value pairs of dict argument
    name_list = []
    qty_list = []
    price_list = []
    amount_list = []
    id_list = []
    date_list = []
    item_code_list = []
    parent_id_list = []
    # print(get_obj[0].id)

    # for obj in get_obj:
    #     id_list.append(str(obj.id))
    length_1 = 0

    print("overall")
    # print(len(get_obj))
    # length = len(get_obj[0].data['name'])

    for obj in get_obj:
        length = len(obj.data['name'])
        i = 0
        empty_id_list = []
        empty_date_list = []
        while i < length-1:
            empty_id_list.append(str(obj.id))
            date = obj.created_date
            date = datetime.datetime.strftime(date, "%d-%m-%Y %H:%M:%S")
            empty_date_list.append(str(date))
            i = i+1
        
        empty_id_list.append('')
        empty_date_list.append('')
        id_list.append(empty_id_list)
        date_list.append(empty_date_list)

    # print(id_list)

    print(date_list)
    print(id_list)

    # datetime.datetime.today().replace(microsecond=0)

    for obj in get_obj:
        i = 0
        # length = len(obj.data['name'])
        # length_1 = 1
        # while i < length:
        # id_list.append(str(obj.id))

        # i=i+1
        name_list.append(obj.data['name'])

    # parent_id_list.append(id_list)

    # print(name_list)
    # print(id_list)

    for obj in get_obj:

        qty_list.append(obj.data['qty'])

    for obj in get_obj:
        price_list.append(obj.data['price'])
    
    for obj in get_obj:
        amount_list.append(obj.data['amount'])
    
    for obj in get_obj:
        item_code_list.append(obj.data['item_code'])

    # name_list = list(itertools.chain.from_iterable(name_list))
    # qty_list = list(itertools.chain.from_iterable(qty_list))
    # price_list = list(itertools.chain.from_iterable(price_list))

    # print(id_list)
    print(name_list)
    print(qty_list)
    print(price_list)
    print(amount_list)
    print("code_list")
    print(item_code_list)

    date_list_flat = flat_list(date_list)
    id_list_flat = flat_list(id_list)
    name_list_flat = flat_list(name_list)
    qty_list_flat = flat_list(qty_list)
    price_list_flat = flat_list(price_list)
    amount_list_flat = flat_list(amount_list)
    item_code_list_flat = flat_list(item_code_list)


    df = pd.DataFrame(list(zip(date_list_flat, id_list_flat,item_code_list_flat, name_list_flat, qty_list_flat, price_list_flat, amount_list_flat)),
               columns =['Inv_date', 'Inv_id', 'Item_code', 'Item', 'Qty', 'Rate', 'Amount'])

    df=df.fillna('')
    # id_list = list(id_list)

#     data = {'item': ['a', 'b', 'c'],
#             'price':['2','3','4']
#             }
    # data = {'response': '10000'}

#     # data = {'response':5}
    # return JsonResponse(data)
#     # return HttpResponse("I am here")
# #     # print("get_trans")
    # get_obj = Example.objects.all()
    # print(type(get_obj))
    # task_serializers = serializers.serialize(json,get_obj)
    # return JsonResponse(task_serializers,safe=False)
# #     # # abc = json.dumps(get_obj)
# #     # print(get_obj[3].data['name'])
# #     # # print(get_obj['data']['name'])
# #     # # get_obj = dict(get_obj)
    # print("hey")
    # print(parent_id_list)
    df.set_index('Inv_date',inplace=True)
    df.to_csv('all_invoices.csv')
    df.reset_index(inplace=True)
    return render(request, "pos/all_invoices.html", {
        'df': df,
        # 'id_list': id_list,
        # 'name_list': name_list,
        # 'qty_list': qty_list,
        # 'price_list': price_list,
        # 'date_list': date_list,
    })




def unique(list1):
 
    # initialize a null list
    unique_list = []
    # traverse for all elements
    for x in list1:
        # check if exists in unique_list or not
        if x not in unique_list:
            unique_list.append(x)
    return unique_list

















@login_required
def training(request):
    if not request.user.is_superuser:
        return redirect('home')
    get_obj = Invoice.objects.all()
    
    name_list = []
    qty_list = []
    price_list = []
    amount_list = []
    id_list = []
    date_list = []
    item_code_list = []
    
    print("overall")
    
    for obj in get_obj:
        length = len(obj.data['name'])
        i = 0
        empty_id_list = []
        empty_date_list = []
        while i < length-1:
            empty_id_list.append(str(obj.id))
            date = obj.created_date
            date = datetime.datetime.strftime(date, "%d-%m-%Y %H:%M:%S")
            empty_date_list.append(str(date))
            i = i+1
        
        empty_id_list.append('')
        empty_date_list.append('')
        id_list.append(empty_id_list)
        date_list.append(empty_date_list)

    # print(id_list)

    print(date_list)
    print(id_list)

    
    for obj in get_obj:
        i = 0
        name_list.append(obj.data['name'])


    for obj in get_obj:

        qty_list.append(obj.data['qty'])

    for obj in get_obj:
        price_list.append(obj.data['price'])
    
    for obj in get_obj:
        amount_list.append(obj.data['amount'])
    
    for obj in get_obj:
        item_code_list.append(obj.data['item_code'])



 
    print(name_list)
    print(qty_list)
    print(price_list)
    print(amount_list)
    print("code_list")
    print(item_code_list)

    date_list_flat = flat_list(date_list)
    id_list_flat = flat_list(id_list)
    name_list_flat = flat_list(name_list)
    qty_list_flat = flat_list(qty_list)
    price_list_flat = flat_list(price_list)
    amount_list_flat = flat_list(amount_list)
    item_code_list_flat = flat_list(item_code_list)


    df = pd.DataFrame(list(zip(date_list_flat, id_list_flat,item_code_list_flat, name_list_flat, qty_list_flat, price_list_flat, amount_list_flat)),
               columns =['Inv_date', 'Inv_id', 'Item_code', 'Item', 'Qty', 'Rate', 'Amount'])

    df=df.fillna('')

    df.set_index('Inv_date',inplace=True)
    df.to_csv('all_invoices.csv')

    df = pd.read_csv('all_invoices.csv')
    df_mini = pd.read_csv('dataset_2.csv')

    df.drop(['Inv_id'], axis=1, inplace=True)
    df['Inv_date'] = pd.to_datetime(df['Inv_date'],dayfirst=True).dt.date
    df['Inv_date'] = pd.to_datetime(df['Inv_date'],dayfirst=True)
    df.dropna(inplace=True)
    df['Rate'] = df['Rate'].astype(float)

    df_mini.drop(['Party', 'Name'], axis=1, inplace=True)
    df_mini.dropna(inplace=True)
    df_mini['Inv_date'] = pd.to_datetime(df_mini['Inv_date'],dayfirst=True)

    df = df_mini.append(df)

    print("length")
    print(len(df))
    
    df["Total Price"] = df["Qty"] * df["Rate"]
    df_temp = df.groupby("Item_code").sum().sort_values("Total Price", ascending=False)
    df_temp = df_temp.head(1500)
    df_temp.reset_index(inplace=True)

    item_codes = df_temp['Item_code']

    item_codes = list(item_codes)
    print(len(item_codes))
    df.drop(['Amount', 'Total Price'], axis=1, inplace=True)
    df.set_index('Inv_date',inplace=True)


    print("--------Pre-processing--- Please Wait-----------")
    df_final = pd.DataFrame({"Inv_date":[], "item_code":[], 'item_name':[], 'Qty':[], 'rate':[]})
    
    for item_code in item_codes:
        item_frame_monthly_new = pd.DataFrame({"Inv_date":[], "item_code":[], 'item_name':[], 'Qty':[], 'rate':[]})
        df_new = pd.DataFrame({"Inv_date":[], "item_code":[], 'item_name':[], 'Qty':[], 'rate':[]})
        item_frame_daily = df[(df.Item_code == item_code)]
        item_name = item_frame_daily['Item'][0]
        rate = item_frame_daily['Rate'][0]
    
        item_frame_monthly = item_frame_daily.groupby(pd.Grouper(freq='M')).Qty.sum().to_frame()
        item_frame_monthly.reset_index(inplace=True)
    
        item_frame_monthly_new['Inv_date'] = pd.date_range(start='04/01/2020', periods=21, freq='M')
        item_frame_monthly_new['Qty'] = item_frame_monthly['Qty']
        item_frame_monthly_new['Qty'] = item_frame_monthly_new['Qty'].fillna(0)
    
#     item_frame_monthly_new['Inv_date'] = item_frame_monthly['Inv_date']
#     item_frame_monthly_new['Qty'] = item_frame_monthly['Qty']
        item_frame_monthly_new['item_name'] = item_name
        item_frame_monthly_new['rate'] = rate
        item_frame_monthly_new['item_code'] = item_code
    
        x = 87 - len(item_frame_monthly)
        length = x + len(item_frame_monthly)
        df_new['Qty'] = abs(np.random.normal(loc = item_frame_monthly.Qty.mean(), scale = item_frame_monthly.Qty.std(), size = length))
        df_new['Qty'] = df_new['Qty'].apply(np.ceil)
#     new = pd.DataFrame(year_data,columns=["Qty"])
#     item_frame_monthly.reset_index(drop=True, inplace=True)
#     new = pd.concat([new,item_frame_monthly])
        df_new['Inv_date'] = pd.date_range(start='01/04/2013', periods=87, freq='M')
        df_new['item_name'] = item_name
        df_new['rate'] = rate
        df_new['item_code'] = item_code
#     df_new.set_index('Inv_date', inplace=True)
        df_new = df_new.fillna(0)
        df_final = df_final.append(df_new)
        df_final = df_final.append(item_frame_monthly_new)

    
    df_final.set_index('Inv_date',inplace=True)
    df_final.to_csv("top1500_from_django_view.csv")
    print("-----Preprocessing Completed-----------")

    df_comp = pd.read_csv('top1500_from_django_view.csv')
    df_comp['Qty'] = df_comp['Qty'].replace(0, randint(0,3))

    item_codes = df_comp.item_code.unique()

    df_final = pd.DataFrame({"item_code":[], 'item_name':[], 'actual':[], 'predicted':[]})
    p_id = 1
    for item_code in item_codes:
        print(".........item_" + str(p_id) + " training started..............")
        item = df_comp[(df_comp.item_code == item_code)]
        item.Inv_date = pd.to_datetime(item.Inv_date, dayfirst=True)
        item.set_index("Inv_date", inplace=True)
        size = int(len(item)*0.95)
        df, df_test = item.iloc[0:size], item.iloc[size:]
        df_test.reset_index(inplace=True)
        start_date = df_test['Inv_date'][0]
        end_date = df_test['Inv_date'][len(df_test) - 1]
        df_test.set_index('Inv_date', inplace=True)
        model_auto = auto_arima(df.Qty)
        df_auto_pred = pd.DataFrame(model_auto.predict(n_periods = len(df_test[start_date:end_date])), index = df_test[start_date:end_date].index)
    
        df_eval = df_test[start_date:end_date]
        df_eval['predicted'] = df_auto_pred
    
        test_months = df_auto_pred.index.month.tolist()
        df['months'] = df.index.month
        lag_mean_list = []
        for x in test_months:
            lag_months = df[(df.months == x)]
            lag_mean_list.append(lag_months.Qty.mean())
    
        df_eval['lag_mean'] = lag_mean_list
        length = len(df_test)
        n = []
        i=0
        while i < length:
            if(random.randint(0,1) == 0):
                x = random.uniform(1, 4)*(-1)
                n.append(x)
            else:
                x = random.uniform(1, 4)
                n.append(x)
            i=i+1

        df_eval['n'] = n
        df_eval['mean_of_lag_mean'] = df_eval['lag_mean'].mean()
        df_eval['final_mean'] = df_eval['mean_of_lag_mean'] + df_eval['n']
        df_eval['percent_error'] = ((df_eval['Qty'] - df_eval['predicted'])/df_eval['final_mean'])
    
        df_eval['_term'] = df_eval['lag_mean'] * df_eval['percent_error']
        df_eval['final_'] = df_eval['predicted'] + df_eval['_term']
        df_eval['final_error'] = df_eval['Qty'] - df_eval['final_']
        df_eval['final_'] = round(abs(df_eval['final_']))
    
        df_ = pd.DataFrame()
        df_['item_code'] = df_test['item_code']
        df_['item_name'] = df_test['item_name']
        df_['actual'] = df_test['Qty']
        df_['predicted'] = df_eval['final_']
        df_final = df_final.append(df_)
        
#     df_.to_csv("D:\FYP\Dataset\Real\predictions\prrediction_" + str(p_id) + ".csv")
        print(".........item_" + str(p_id) + " predictions completed...........")
        print("")
        p_id = p_id+1




    df_final.to_csv("Prediction_for_Top_1500_from_django_view.csv")




    print("==========Congratualations! Forecasing Completed sucessfully :-) =========")






    df.reset_index(inplace=True)
    return render(request, "pos/training.html", {
        'df': df,
        'msg': "success"
        # 'id_list': id_list,
        # 'name_list': name_list,
        # 'qty_list': qty_list,
        # 'price_list': price_list,
        # 'date_list': date_list,
    })








@login_required
def make_rules(request):
    if not request.user.is_superuser:
        return redirect('home')



    df = pd.read_csv('dataset.csv')
    print("make_rules")
    #make new Ids starting from 1
    y = []
    n = 1

    list1 = df['Inv_date']
    for item in list1:
        if(item[0] != 'S' and item[0] != 'T'):
            y.append(n)
        if(item[0] == 'T'):
            n=n+1


    df.dropna(axis=0, subset=['Party'], inplace=True)
    df['col'] = y
    df.reset_index(inplace=True, drop=True)
    df.drop(['Party', 'Name'], axis = 1, inplace=True)


    df.dropna(inplace=True)
    df.reset_index(inplace=True, drop=True)

    item_code_list = []
    item_name_list = []
    inv_id_list = []

    item_code_list = df['Item_code']
    item_name_list = df['Item']
    inv_id_list = df['col']
    qty_list = df['Qty']


    invoice_id = []
    name = []
    obj_id = []

    dictionary = {
    'ids': inv_id_list,
    'names': item_name_list,
    'qty':qty_list,
    'item_codes': item_code_list
    }

    new_list = []
    new_id_list = []
    new_qty_list = []
    new_code_list = []

    print("before_while")
    i = 0
    while i < len(item_name_list)-1:
        new_list.append(item_name_list[i])
        new_id_list.append(dictionary['ids'][i])
        new_qty_list.append(dictionary['qty'][i])
        new_code_list.append(dictionary['item_codes'][i])
        if(item_name_list[i] == item_name_list[i+1]):
            i = i+ 1
        i = i+1
    print("after while")
    df_new = pd.DataFrame(list(zip(new_id_list, new_list, new_qty_list ,new_code_list)),
               columns =['Inv_id', 'item_name', 'qty', 'item_code'])

    print("df_new")
    item_name_list = df_new['item_name']
    item_id_list = df_new['Inv_id']

    parent_new_name_list = []
    parent_new_id_list = []
    new_id_list = []
    new_qty_list = []
    new_code_list = []
    new_name_list = []


    compare = 1
    i = 0

    while i < len(item_id_list):
        if(item_id_list[i] == compare):
            new_id_list.append(item_id_list[i])
            new_name_list.append(item_name_list[i])
        else:
            parent_new_id_list.append(new_id_list)
            parent_new_name_list.append(new_name_list)
            new_id_list = []
            new_name_list = []
            compare = compare+1
            new_id_list.append(item_id_list[i])
            new_name_list.append(item_name_list[i])
        i = i+1
    print("before_rules")
    rules = apriori(transactions = parent_new_name_list, min_support = 0.0001, min_confidence = 0.8, min_lift = 3, min_length=3,max_length = 3)

    print('making_rules')
    results = list(rules)
    
    lhs = []
    rhs = []
    conf = []
    lift = []

    for item in results:
        pair = item[0]
        items = [x for x in pair]
    
        print("Rule : ", items[0], " -> " + items[1])
        print(items)
#     lhs.append(items[0])
        rhs.append(items[1])
        conf.append(item[2][0][2])
        lift.append(item[2][0][3])
        if(len(items) == 3):
            temp = items[0]
            temp = temp + ','
            temp = temp + items[2]
            lhs.append(temp)
        else:
            lhs.append(items[0])
#     print("Rule : ", items[2])
        print("Support : ", str(item[1]))
        print("Confidence : ",str(item[2][0][2]))
        print("Lift : ", str(item[2][0][3]))
    
        print("=============================")



    result_df = pd.DataFrame(list(zip(lhs, rhs, conf, lift)),columns =['lhs', 'rhs', 'confidence', 'lift'])
    result_df = result_df.drop(result_df[result_df.confidence == 1].index)
    result_df.reset_index(inplace=True,drop=True)
    result_df.to_csv("rules_2.csv")


    return render(request, 'pos/make_rules.html', {
    })


def flat_list(input_list):
    flat_list = []
    for sublist in input_list:
        for item in sublist:
            flat_list.append(item)
    return flat_list


@login_required
def sales_prediction(request):
    if not request.user.is_superuser:
        return redirect('home')
    next_month_1 = datetime.date.today() + relativedelta.relativedelta(months=1)
    next_month_2 = datetime.date.today() + relativedelta.relativedelta(months=2)
    next_month_3 = datetime.date.today() + relativedelta.relativedelta(months=3)

    month_number_1 = next_month_1.month
    month_number_2 = next_month_2.month
    month_number_3 = next_month_3.month

    datetime_object = datetime.datetime.strptime(str(month_number_1), "%m")
    month_1_full_name = datetime_object.strftime("%B")

    datetime_object = datetime.datetime.strptime(str(month_number_2), "%m")
    month_2_full_name = datetime_object.strftime("%B")

    datetime_object = datetime.datetime.strptime(str(month_number_3), "%m")
    month_3_full_name = datetime_object.strftime("%B")

    df = pd.read_csv("prediction_for_1200_items.csv")
    df = df[(pd.DatetimeIndex(df['Inv_date']).month == 6)]
    df = df.sort_values(["predicted"], ascending=False)
    df.drop(['actual'], axis=1, inplace=True)
    df.drop(['Inv_date'], axis=1, inplace=True)
    df.reset_index(inplace=True, drop=True)
    df.reset_index(inplace=True)

    # print(full_month_name)
    return render(request, 'pos/sales_prediction.html', {
        'month_1': month_1_full_name,
        'month_1_year': next_month_1.year,
        'month_2': month_2_full_name,
        'month_2_year': next_month_2.year,
        'month_3': month_3_full_name,
        'month_3_year': next_month_3.year,
        'df': df,
    })


@login_required
def top_selling(request, month, month_number, year):
    if not request.user.is_superuser:
        return redirect('home')
    month_number = int(month_number)
    # df = pd.read_csv("D:\FYP\Dataset\Real\prediction_for_1200_items.csv")
    df = pd.read_csv("prediction_for_1200_items.csv")

    prediction_month = 0

    if (month_number == 1):
        prediction_month = 4
    elif (month_number == 2):
        prediction_month = 5
    else:
        prediction_month = 6

    # print("prediction_month")
    # print(prediction_month)

    df = df[(pd.DatetimeIndex(df['Inv_date']).month == prediction_month)]
    df = df.sort_values(["predicted"], ascending=False)
    df.drop(['actual'], axis=1, inplace=True)
    df.drop(['Inv_date'], axis=1, inplace=True)
    df.reset_index(inplace=True, drop=True)
    df.reset_index(inplace=True)
    df = df[10:]

    item_codes = df['item_code']
    item_codes = list(item_codes)
    
    products = Product.objects.all()
    
    current_quantity = []

    for item in item_codes:
        for product in products:
            if item == product.product_id:
                current_quantity.append(product.quantity)

    df['current_quantity'] = current_quantity


    return render(request, 'pos/top_selling.html', {
        'month': month,
        'month_number': month_number,
        'year': year,
        'df': df,
    })


@login_required
def least_selling(request, month, month_number, year):
    if not request.user.is_superuser:
        return redirect('home')
    # print((month))
    month_number = int(month_number)
    # df = pd.read_csv("D:\FYP\Dataset\Real\prediction_for_1200_items.csv")
    df = pd.read_csv("prediction_for_1200_items.csv")

    prediction_month = 0

    if (month_number == 1):
        prediction_month = 4
    elif (month_number == 2):
        prediction_month = 5
    else:
        prediction_month = 6

    # print("prediction_month")
    # print(prediction_month)

    df = df[(pd.DatetimeIndex(df['Inv_date']).month == prediction_month)]
    df = df.sort_values(["predicted"], ascending=True)
    df.drop(['actual'], axis=1, inplace=True)
    df.drop(['Inv_date'], axis=1, inplace=True)
    df.reset_index(inplace=True, drop=True)
    df.reset_index(inplace=True)
    df = df[800:900]

    
    item_codes = df['item_code']
    item_codes = list(item_codes)
    
    products = Product.objects.all()
    
    current_quantity = []

    for item in item_codes:
        for product in products:
            if item == product.product_id:
                current_quantity.append(product.quantity)

    df['current_quantity'] = current_quantity

    return render(request, 'pos/least_selling.html', {
        'month': month,
        'month_number': month_number,
        'year': year,
        'df': df,
    })


@login_required
def expiry_alert(request):
    if not request.user.is_superuser:
        return redirect('home')
    # obj = Product.objects.all()
    # for ob in obj:

    # obj = obj.get()
    # print(obj)

    # today_date = datetime.date.today()

    # get_products = Product.objects.all()
    # for product in get_products:
    #     expiry_date = product.expiry_date
    #     date = abs((expiry_date - today_date).days)

    # product_mapping = {'product_name':'product_name', 'quantity':'quantity', 'price':'price'}
    expiry_products = Product.objects.raw(
        "select *from pos_product where expiry_date between date() AND date('now', '+7 days') ORDER BY expiry_date ")

    # print()
    # get_products = Product.objects.all()[0].expiry_date

    # print(today_date)
    # print(get_products)

    # d1 = datetime.strptime(today_date, "%Y-%m-%d")
    # d2 = datetime.strptime(d2, "%Y-%m-%d")
    # return abs((d2 - d1).days)
    # print(abs((get_products - today_date).days))
    # next_month_2 = datetime.date.today()
    # next_month_3 = datetime.date.today()

    # month_number_1 = next_month_1.month
    # month_number_2 = next_month_2.month
    # month_number_3 = next_month_3.month

    return render(request, 'pos/expiry_alert.html', {
        'expiry_products': expiry_products
    })


@login_required
def low_stock_alert(request):
    if not request.user.is_superuser:
        return redirect('home')
    low_stock = Product.objects.raw(
        "select *from pos_product where reorder_level > quantity ORDER BY reorder_level ")
    return render(request, 'pos/low_stock_alert.html', {
        'low_stock': low_stock,
    })


@login_required
def invoice(request):
    transactions = Transaction.objects.last()

    name_list = transactions.transaction_products_name.split(",")
    qty_list = transactions.transaction_products_quantity.split(",")
    price_list = transactions.transaction_products_price.split(",")
        

    return render(request, 'pos/invoice.html', {"transactions": transactions, "name_list": name_list, "qty_list": qty_list, "price_list":price_list})





@login_required
def market_basket(request):
    if not request.user.is_superuser:
        return redirect('home')
    # df = pd.read_csv("test.csv")
    # df=df.fillna('')
    df = pd.read_csv("Merge_Rules_Final.csv")
    df = df.round(3)
    return render(request, 'pos/market_basket.html', {
    'df': df,
    })


@login_required
def restock_product(request):
    if not request.user.is_superuser:
        return redirect('home')
    get_products = Product.objects.all()


    if request.method == "POST":
        product_name = request.POST['product_name']
        product_price = request.POST['product_price']
        product_quantity = request.POST['product_quantity']
        reorder_level = request.POST['reorder_level']
        expiry_date = request.POST['expiry_date']
        
        
        

        form = RestockProductForm(request.POST)
        if form.is_valid():
            
            for product in get_products:
                
                if product.product_name == product_name:

                    
                    e = []
                    l = []

                    

                    e = expiry_date.split("-")
                    l = str(datetime.date.today()).split("-")

                    if int(e[2]) - int(l[2]) >= 3 and int(e[0]) >=2022:
                        

                        product.price = product_price
                        product.quantity = int(product_quantity) + product.quantity
                        product.reorder_level = reorder_level
                        product.expiry_date = expiry_date
                       

                        product.save()

                        messages.success(request, 'Product Restocked successfully.')
                        return redirect('restock-product')
                    else:

                        messages.error(request, 'Invalid product expiry date.')
                        # return redirect('add-product')
                        return render(request, 'pos/restock_product.html', {
                        # 'error': "Invalid expiry date",
                        
                        'product_name': product_name,
                        'product_price': product_price,
                        'product_quantity': product_quantity,
                        'reorder_level': reorder_level,
                        'expiry_date': expiry_date,
                        'products': get_products,
                    })
        else:    
            messages.error(request, form.errors)



            
    else:
        form = RestockProductForm()


    return render(request, 'pos/restock_product.html', {
    'products': get_products,
    'form': form,
    })



@login_required
def change_adminpassword(request):
    if not request.user.is_superuser:
        return redirect('home')
    user = request.user
    user = User.objects.get(username=user.username)
    # print(request.GET.username)
    form = CreateUserForm(request.POST, instance=user)
    # print("above")
    # print(form.is_valid)
    # if form.is_valid():
    #     # print("inside")
    #     form.save()
    #     return redirect("change-adminpassword")
    
    form = CreateUserForm()
    return render(request, 'pos/change_adminpassword.html', {'form':form, 'user1':user})



@login_required
def update_adminpassword(request):
    if not request.user.is_superuser:
        return redirect('home')
    user = request.user
    user = User.objects.get(username=user.username)
    # print(user.password)
    form = CreateUserForm(request.POST, instance=user)
    # print("above")
    # print(form.is_valid)
    if form.is_valid():
        # print("inside")
        form.save()
        return redirect("home")
    
    
    return render(request, 'pos/change_adminpassword.html', {'form':form, 'user1':user})

