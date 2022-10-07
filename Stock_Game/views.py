from django.shortcuts import render
from nsetools import Nse
from operator import itemgetter
from .models import Stock,Buy,Room, Join
from User.models import Profile

# creating a Nse object
nse = Nse()

# getting quote of the sbin
quote = nse.get_quote('hdfc')
def index(request):
    return render(request, 'Stock_Game/main.html')
def stocks_list(request):
    nse = Nse()
    stocks=Stock.objects.all()
    print(stocks)
    k=[]
    for i in stocks:
        d=dict()
        quote = nse.get_quote(i.nse_code)
        d['name']=i.stock_name
        d['Price']=quote['buyPrice1']
        k.append(d)
    param={'k':k}
    return render(request,'Stock_Game/Stock_list.html',param)
def ranklist(request,team_name):
    print(team_name)
    room1=Room.objects.filter(id=team_name)
    print(room1)
    for i in room1:
        k1=i
    teams=Join.objects.filter(room=k1)
    k=[]
    nse = Nse()
    for i in teams:
        p=[]
        p.append(i.reg_user_id)
        buy1=Buy.objects.filter(reg_user_id=i.reg_user_id).filter(reg_room_id=i.room)
        sum=i.user_money
        for j in buy1:
            print(j.reg_stock_id)
            quote = nse.get_quote(j.reg_stock_id.nse_code)
            print(quote['buyPrice1'])
            sum+=(quote['buyPrice1']*j.no_of_shares)
        p.append(sum)
        k.append(p)
    k.sort(key = lambda x: x[1])
    print(k)
    return render(request, 'Stock_Game/stocklist.html')



def portfolio(request,team_name):
    us=request.user
    nse = Nse()
    Room1=Room.objects.filter(id=team_name)
    init=Room1[0].room_money
    Profile1=Profile.objects.filter(user=request.user)
    for i in Profile1:
        k=i
    Buy1=Buy.objects.filter(reg_user_id=k.id).filter(reg_room_id=team_name)
    k=[]
    sum=0
    inv=0
    for i in Buy1:
        k2=dict()
        k2['stock_name']=i.reg_stock_id.stock_name
        k2['no_of_shares']=i.no_of_shares
        quote = nse.get_quote(i.reg_stock_id.nse_code)
        k2['old_price']=i.current_stock_price
        k2['Current_price']=quote['buyPrice1']
        k2['profit']=(quote['buyPrice1']-i.current_stock_price)*(i.no_of_shares)
        sum+=(quote['buyPrice1'])*(i.no_of_shares)
        inv+=(i.current_stock_price)*(i.no_of_shares)
        k.append(k2)
    print(k)
    param={'k':k,'money_left':(init-inv),'Profit':(init-inv+sum),'Initial':init}
    return render(request, 'Stock_Game/portfolio.html',param)
# Create your views here.
def stockers(request,stock):
    nse = Nse()
    param={'stock_name':quote['companyName'],'Stock_price':quote['buyPrice1']}
    return render(request, 'Stock_Game/stocker.html',param)


