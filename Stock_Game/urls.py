from django.urls import path
from . import views


urlpatterns = [
    path('',views.index,name="home"),
    path('stocks/',views.stocks_list,name="stocks"),
    path('stockname/<stock>/',views.stockers,name="stockname")

]