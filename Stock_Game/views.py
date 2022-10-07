from django.shortcuts import render
from nsetools import Nse

# creating a Nse object
nse = Nse()

# getting quote of the sbin
quote = nse.get_quote('hdfc')
def index(request):
    return render(request, 'Stock_Game/main.html')
def stocks_list(request):
    return render(request,'Stock_Game/stocklist.html')
# Create your views here.
def stockers(request,stock):
    nse = Nse()
    quote = nse.get_quote(stock)
    param={'stock_name':quote['companyName'],'Stock_price':quote['buyPrice1']}
    return render(request, 'Stock_Game/stocker.html',param)

def stock_details(request):
    return render(request, 'Stock_Game/stock_details.html')
