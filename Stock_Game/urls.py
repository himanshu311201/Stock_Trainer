from django.urls import path
from . import views


urlpatterns = [
    path('',views.index,name="home"),
    path('stocks/',views.stocks_list,name="stocks"),
    path('stockname/<stock>/',views.stockers,name="stockname"),
    path('<room_name>/<stock_name>/', views.stock_details, name='stock_details'),
    path('<room_name>/<stock_name>/<current_stock_price>/', views.push_details, name='push_details'),
    path('<room_name>/<stock_name>/<current_stock_price>/<no_of_shares>/', views.pull_details, name='pull_details')
]