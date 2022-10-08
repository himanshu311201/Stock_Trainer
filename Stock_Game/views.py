from django.shortcuts import render
from nsetools import Nse
from .models import Room, Buy, Join, Stock, Profile, Consultant, Subscribe
from django.shortcuts import render, redirect, get_object_or_404

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
    print(stock)
    nse = Nse()
    quote = nse.get_quote(stock)
    param={'stock_name':quote['companyName'],'Stock_price':quote['buyPrice1']}
    return render(request, 'Stock_Game/stocker.html',param)

def stock_details(request,room_name,stock_name):
    nse = Nse()
    quote = nse.get_quote(stock_name),

    context = {
        'room_name': room_name,
        'stock_name': stock_name,
        'current_stock_price': quote[0]['buyPrice1'],
    }

    room_b = Join.objects.all()
    for i in room_b:
        if i.reg_user_id.user == request.user:
            print(i.reg_user_id.user)
            print(i.user_money)
            context['room_balance'] = i.user_money;

    context['no_of_shares'] = 0;

    sell = Buy.objects.all()
    for i in sell:
        m = str(i.reg_room_id)
        n = str(i.reg_stock_id)
        if (i.reg_user_id.user == request.user) and (m == room_name) and (n == stock_name):
            context['no_of_shares'] = i.no_of_shares;

    if(stock_name == 'SBIN'):
        context['temp'] = "State Bank Of India",
        context['temp'] = context['temp'][0]

    return render(request, 'Stock_Game/stock_details.html', context)

def push_details(request, room_name, stock_name, current_stock_price):
    request.session['POSTVALUES'] = request.POST.copy(),

    post_values = request.session.get('POSTVALUES')
    print(post_values)

    for i in post_values:
        no_of_share = i['quantity'][0],
        total_amount = i['output']

    pr = Profile.objects.all()
    ro = Room.objects.all()
    st = Stock.objects.all()
    print(type(current_stock_price))
    for i in pr:
        print(i.user, request.user)
        if i.user == request.user:
            pr = i
            break

    for i in ro:
        print(i.room_name, room_name)
        if i.room_name == room_name:
            ro = i
            break

    for i in st:
        print(i.nse_code, stock_name)
        if i.nse_code == stock_name:
            st = i
            break

    update_amount = Join.objects.all()
    upd = 15000

    for i in update_amount:
        m = str(i.room)
        print(pr.user,request.user,m,room_name, pr.user == request.user, m == room_name, type(room_name), type(m))
        if (pr.user == request.user) and (m == room_name):
            upd = i.user_money - float(total_amount)
            print(upd)

    if request.method == 'POST':

        data = Buy.objects.create(reg_user_id=pr, reg_room_id=ro, reg_stock_id=st, current_stock_price=current_stock_price, no_of_shares=no_of_share[0]),

        Join.objects.get(reg_user_id = pr, room = ro).delete(),
        data = Join.objects.create(reg_user_id = pr, room = ro, user_money = upd),

        return render(request, 'Stock_Game/main.html')

def pull_details(request,room_name,stock_name,current_stock_price,no_of_shares):
    request.session['POSTVALUES'] = request.POST.copy(),

    post_values = request.session.get('POSTVALUES')
    print(post_values)

    for i in post_values:
        total_amount = i['output1']

    pr = Profile.objects.all()
    ro = Room.objects.all()
    st = Stock.objects.all()
    print(type(current_stock_price))
    for i in pr:
        print(i.user, request.user)
        if i.user == request.user:
            pr = i
            break

    for i in ro:
        print(i.room_name, room_name)
        if i.room_name == room_name:
            ro = i
            break

    for i in st:
        print(i.nse_code, stock_name)
        if i.nse_code == stock_name:
            st = i
            break

    sell_amount = Join.objects.all()

    for i in sell_amount:
        m = str(i.room)
        print(pr.user, request.user, m, room_name, pr.user == request.user, m == room_name, type(room_name), type(m))
        if (pr.user == request.user) and (m == room_name):
            upd = i.user_money + float(total_amount)
            print(upd)

    if request.method == 'POST':
        Buy.objects.get(reg_user_id=pr, reg_room_id=ro, reg_stock_id=st,current_stock_price=current_stock_price, no_of_shares=no_of_shares).delete(),

        Join.objects.get(reg_user_id=pr, room=ro).delete(),

        data = Join.objects.create(reg_user_id=pr, room=ro, user_money=upd),

        return render(request, 'Stock_Game/main.html')

