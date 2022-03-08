"""point_of_sale URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from pos import views
# from registration import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pos.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    # path('', views.login_page),
    path('edit/<username>', views.edit),
    path('update/<username>', views.update),
    path('delete/<username>', views.destroy),

    path('add/', views.add_data, name="add"),

    # path('save/', views.save_transaction, name="save-transaction"),

    path('sales-prediction/top-selling/<month>/<year>/<month_number>', views.top_selling),
    path('sales-prediction/least-selling/<month>/<year>/<month_number>', views.least_selling),
    # path('sales-prediction/top-selling/<month>/<month_number>', views.top_selling),

]

