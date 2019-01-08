"""system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from drink.views import main_page,order,add_member,management,customer_info
from drink.views import predict_ingredient,list_ingredient,level_setup

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_page),
    path('drink_system/', main_page),
    path('add_member/', add_member),
    path('order/', order),
    path('management/ingredient', management),
    path('management/customer_info', customer_info),

    path('predictingredient/',predict_ingredient),
    path('listingredient/',list_ingredient),
    path('level_setup/',level_setup),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
