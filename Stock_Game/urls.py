from django.urls import path
from . import views


urlpatterns = [
    path('',views.index,name="home"),
    path('stocks/<team_name>/',views.stocks_list,name="stocks"),
    path('portfolio/<team_name>/',views.portfolio,name="stocks"),
    path('ranklist/<team_name>/',views.ranklist,name="stocks"),
    path('stockname/<stock>/',views.stockers,name="stockname"),
    path('createform/',views.Create_team,name="creater"),
    path('showname/<team_hel>',views.shownum,name="show"),
    path('join/',views.join,name="join"),
    path('stock_details/', views.stock_details, name='stock_details')

]