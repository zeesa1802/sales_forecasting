from django.urls import path
from .import views


urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_page, name='login'),
    path('all-categories/', views.all_categories, name='all-category'),
    path('add-category/', views.add_category, name='add-category'),
    path('all-product/', views.all_product, name='all-product'),
    path('add-product/', views.add_product, name='add-product'),
    path('user-config/', views.user_config, name='user-config'),
    path('create-order/', views.create_order, name='create-order'),
    path("all-invoices", views.get_transaction, name='all-invoices'),
    path('save-invoice/', views.save_invoice, name='save-invoice'),
    path('transaction/', views.transaction, name='transaction'),
    path('sales-prediction/', views.sales_prediction, name='sales-prediction'),
    path('invoice/', views.invoice, name='invoice'),
    path('market-basket/', views.market_basket, name='market-basket'),
    path('restock-product/', views.restock_product, name='restock-product'),
    path('change-adminpassword/', views.change_adminpassword, name='change-adminpassword'),
    path('update-adminpassword/', views.update_adminpassword, name='update-adminpassword'),
    
    # path('sales-prediction/top-selling', views.top_selling, name='top-selling'),

    path('expiry-alert/', views.expiry_alert, name='expiry-alert'),
    path('low-stock-alert/', views.low_stock_alert, name='low-stock-alert'),
    path('make-rules/', views.make_rules, name='make-rules'),
    path('training/', views.training, name='training'),
   
 
]
