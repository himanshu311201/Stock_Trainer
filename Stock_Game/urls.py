from django.urls import path
from . import views


urlpatterns = [
    path('',views.index,name="home"),
    path('stocks/',views.stocks_list,name="stocks"),
    path('portfolio/<team_name>/',views.portfolio,name="stocks"),
    path('ranklist/<team_name>/',views.ranklist,name="stocks"),
    path('stockname/<stock>/',views.stockers,name="stockname")

]