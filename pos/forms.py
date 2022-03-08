from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'username', 'password1', 'password2']

# class EditUserForm(UserCreationForm):
# 	class Meta:
# 		model = User
# 		fields = ['first_name', 'last_name', 'username']


class CategoryForm(forms.Form):
	date = forms.DateField()
	category_name = forms.CharField(max_length=20, required=True)
	# is_active = forms.BooleanField()

class ProductForm(forms.Form):
	# product_id = forms.CharField(max_length=20)
	product_name = forms.CharField(max_length=100)
	product_price = forms.FloatField()
	product_quantity = forms.IntegerField()
	reorder_level = forms.IntegerField()
	expiry_date = forms.DateField()
	product_category = forms.CharField(max_length=30)


class RestockProductForm(forms.Form):
	# product_id = forms.CharField(max_length=20)
	product_name = forms.CharField(max_length=100)
	product_price = forms.FloatField()
	product_quantity = forms.IntegerField()
	reorder_level = forms.IntegerField()
	expiry_date = forms.DateField()
	
