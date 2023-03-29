from django.shortcuts import render,redirect
from nsetools import Nse
import json
from django.http import JsonResponse
from .models import Room, Buy, Join, Stock, Profile, Consultant, Subscribe
from django.shortcuts import render, redirect, get_object_or_404
import ast
from bs4 import BeautifulSoup as BS
import requests as req
from operator import itemgetter
from .models import Stock,Buy,Room, Join
from User.models import Profile,Subscribe,Consultant
from .forms import CreateForm
from django.contrib import messages
from Stock_Game.lstm import *
import traceback

def index(request):
    return render(request,"Stock_Game/index.html")

    
# creating a Nse object
nse = Nse()
def Create_team(request):
    print("GO to hell")
    if request.method == 'POST':
        print("GO to hell")
        form = CreateForm(request.POST, request.FILES)
        if form.is_valid():
            Profile1 = Profile.objects.filter(user=request.user)
            p = form.save(commit=False)
            print("marja")
            p.reg_user=Profile1[0]
            p.save()
            print("Hell")
            post = Join()
            post.reg_user_id=Profile1[0]
            pol=Room.objects.get(id=(p.pk))
            post.room=pol
            post.user_money=pol.room_money
            post.save()
            return redirect('show',p.pk)
        else:
            print(form.errors)
            return render(request, 'Stock_Game/form.html', {'form': form})
    else:
        form = CreateForm()
        return render(request, 'Stock_Game/form.html', {'form': CreateForm})
def shownum(request,team_hel):
    param={'hex':hex(int(team_hel))}
    return render(request,'Stock_Game/show.html',param)
def join(request):
    if request.method == 'POST':
        if request.POST.get('content'):
            post = Join()
            Profile1 = Profile.objects.filter(user=request.user)
            post.reg_user_id = Profile1[0]
            k=ast.literal_eval(request.POST.get('content'))
            print(k)
            pol = Room.objects.get(id=k)
            post.room = pol
            post.user_money = pol.room_money
            post.save()
            return redirect('main')
    return redirect('main')
def main_home(request):
    room1 = Room.objects.filter(id=1)
    for i in room1:
        k1 = i
    init = room1[0].room_money
    teams = Join.objects.filter(room=k1)
    print(teams)
    nse = Nse()
    Profile1 = Profile.objects.filter(user=request.user)
    room2 = Join.objects.filter(reg_user_id=Profile1[0])
    print(room2)
    subs=Subscribe.objects.filter(reg_user=Profile1[0])
    buy2 = Buy.objects.filter(reg_user_id=Profile1[0]).filter(reg_room_id=1)
    sum1=room2[0].user_money
    sum2 = room2[0].user_money
    print(sum1)
    for j in buy2:
        quote = nse.get_quote(j.reg_stock_id.nse_code)
        sum1 += (quote['open'] * j.no_of_shares)
    print(sum1)
    k3 = 1
    for i in teams:
        p = []
        p.append(i.reg_user_id.user.username)
        buy1 = Buy.objects.filter(reg_user_id=i.reg_user_id).filter(reg_room_id=i.room)
        sum = i.user_money
        k2 = -99999;
        for j in buy1:
            quote = nse.get_quote(j.reg_stock_id.nse_code)
            sum += (quote['open'] * j.no_of_shares)
        if sum>sum1:
            k3+=1
    print(init)
    param={'rank':k3,'avail':sum2,'profit':round(sum1-init, 2),'room':room2,'subs':subs}
    return render(request, 'Stock_Game/main.html',param)
def stocks_list(request,team_name):
    nse = Nse()
    stocks=Stock.objects.all()
    print(stocks)
    k=[]
    for i in stocks:
        d=dict()
        quote = nse.get_quote(i.nse_code)
        d['name']=i.stock_name
        d['Price']=quote['open']
        d['id']=team_name
        d['nse_code']=i.nse_code
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
        p.append(i.reg_user_id.user.username)
        buy1=Buy.objects.filter(reg_user_id=i.reg_user_id).filter(reg_room_id=i.room)
        sum=i.user_money
        print(i.user_money)
        k2=-99999;
        for j in buy1:
            quote = nse.get_quote(j.reg_stock_id.nse_code)
            if k2<quote['open']*j.no_of_shares:
                p1=j.reg_stock_id.stock_name
            sum+=(quote['open']*j.no_of_shares)
            print(quote['open'])
            print(j.no_of_shares)

            print(sum)
        p.append(int(sum))
        p.append(p1)
        k.append(p)
    k.sort(key = lambda x: x[1], reverse=True)
    p2=[]
    k3=1
    for i in k:
        h1=dict()
        h1['rank']=k3
        h1['name']=i[0]
        h1['sum']=i[1]
        k3+=1
        h1['Stock']=i[2]
        p2.append(h1)
    print(p2)
    param={'k':p2}
    return render(request, 'Stock_Game/stocker.html',param)

def portfolio(request,team_name):
    us=request.user
    nse = Nse()
    Room1=Room.objects.filter(id=team_name)
    init=Room1[0].room_money
    name=Room1[0].room_name
    id1=Room1[0].id
    Profile1=Profile.objects.filter(user=request.user)
    for i in Profile1:
        k=i
    Buy1=Buy.objects.filter(reg_user_id=k.id).filter(reg_room_id=team_name)
    k=[]
    sums=0
    inv=0
    sum = 0
    var = 0
    for i in Buy1:
        sums = 0
        k2=dict()
        k2['stock_nse'] = i.reg_stock_id.nse_code
        k2['stock_name']=i.reg_stock_id.stock_name
        k2['no_of_shares']=i.no_of_shares
        quote = nse.get_quote(i.reg_stock_id.nse_code)
        k2['old_price']=i.current_stock_price
        k2['Current_price']=quote['open']
        k2['profit'] = round((quote['open']-i.current_stock_price) * i.no_of_shares, 2)
        sum = sum + (quote['open']) * i.no_of_shares
        sums = sums + (quote['open']) * i.no_of_shares
        inv = inv + i.current_stock_price * i.no_of_shares
        print(inv)
        k2['sums'] = sums
        k2['var'] = var
        var = var + 1
        k.append(k2)
    print(init)
    param={'k':k,'money_left':(init-inv),'Profit':round(sum-inv, 2),'Initial':init,'name':name,'id':id1}
    return render(request, 'Stock_Game/portfolio.html',param)

# Create your views here.
def stockers(request,stock):
    print(stock)
    nse = Nse()
    quote = nse.get_quote(stock)
    param={'stock_name':quote['companyName'],'Stock_price':quote['open']}
    return render(request, 'Stock_Game/stocker.html',param)

def stock_details(request,room_name,stock_name):
    nse = Nse()
    quote = nse.get_quote(stock_name)
    x = Room.objects.filter(id=room_name)
    x = x[0].room_name
    print(room_name)

    context = {
        'room_id': room_name,
        'room_name': x,
        'stock_name': stock_name,
        'current_stock_price': quote['open'],
    }
    p = Profile.objects.filter(user = request.user)[0]
    room_b = Join.objects.filter(reg_user_id = p, room = room_name)
    context['room_balance'] = room_b[0].user_money
    context['no_of_shares'] = 0;
    print(p, x, int(room_name), stock_name)
    x = Stock.objects.filter(nse_code = stock_name)[0].stock_name
    context['temp'] = x
    return render(request, 'Stock_Game/stock_details.html', context)




def getval(request,stock):

    # TO GET THE TPYE OF CLASS
    # HERE 'a' STANDS FOR ANCHOR TAG IN WHICH NEWS IS STORED
    nse = Nse()
    quote = nse.get_quote(stock)
    contem = {
        'code': quote['open'],
    }
    return JsonResponse(contem)

def push_details(request, room_name, stock_name, current_stock_price):

    try:
        # print("Mai hi hoon")
        request.session['POSTVALUES'] = request.POST.copy(),

        post_values = request.session.get('POSTVALUES')
        # print(post_values)

        x = post_values[0]
        no_of_share = x['quantity'],
        total_amount = x['output'],

        pr = Profile.objects.filter(user=request.user)[0]
        ro = Room.objects.filter(id=room_name)[0]
        st = Stock.objects.filter(nse_code=stock_name)[0]
        print(type(current_stock_price), current_stock_price)

        imp = Join.objects.filter(reg_user_id=pr, room=ro)

        upd = imp[0].user_money - float(total_amount[0])
        print(upd)

        if request.method == 'POST':
            if(Buy.objects.filter(reg_user_id=pr, reg_room_id=ro, reg_stock_id=st, current_stock_price=current_stock_price).exists()):
                x = Buy.objects.get(reg_user_id=pr, reg_room_id=ro, reg_stock_id=st, current_stock_price=current_stock_price)
                x = x.no_of_shares
                y = int(x) + int(no_of_share[0])
                Buy.objects.filter(reg_user_id=pr, reg_room_id=ro, reg_stock_id=st, current_stock_price=current_stock_price).update(no_of_shares=y)

            else:
                Buy.objects.create(reg_user_id=pr, reg_room_id=ro, reg_stock_id=st, current_stock_price=current_stock_price, no_of_shares=no_of_share[0]),

            Join.objects.filter(reg_user_id=pr, room=ro).update(user_money=upd),

        x = '/portfolio/' + room_name + '/'
        return redirect(to=x)

    except:
        traceback.print_exc()
        return redirect('push_details', room_name=room_name, stock_name=stock_name)



def pull_details(request,room_name,stock_name,current_stock_price,no_of_shares):

    request.session['POSTVALUES'] = request.POST.copy(),

    post_values = request.session.get('POSTVALUES')[0]
    print(post_values)

    total_amount = post_values['output1']

    pr = Profile.objects.filter(user=request.user)[0]
    print(pr)
    ro = Room.objects.filter(id=room_name)[0]
    print(ro)
    st = Stock.objects.filter(nse_code=stock_name)[0]
    print(st)
    print(type(current_stock_price))

    imp = Join.objects.filter(reg_user_id=pr, room=ro)[0]
    upd = imp.user_money + float(total_amount)
    print(upd)

    if request.method == 'POST':
        Buy.objects.get(reg_user_id=pr, reg_room_id=ro, reg_stock_id=st).delete(),

        Join.objects.filter(reg_user_id=pr, room=ro).update(user_money=upd)

        return redirect(to='/')

def predict(request,room_name,stock_name,current_stock_price,no_of_shares):
    nse = Nse()
    quote = nse.get_quote(stock_name),
    context = {}

    se = "NSE"
    stock_symbol = stock_name
    predicted_result_df = lstm_prediction(se, stock_symbol)
    context["predicted_result_df"] = predicted_result_df

    x = Stock.objects.filter(nse_code=stock_name)[0].stock_name
    print(room_name)
    context['room_name'] = room_name
    context['temp'] = x
    context['stock_name'] = stock_name

    print(context['temp'])

    return render(request, 'Stock_Game/predict.html', context)

def portfolio_pull(request,room_name,stock_name,invested_stock_price,current_stock_price,no_of_shares):

    print('Portfolio')
    pr = Profile.objects.filter(user=request.user)[0]
    print(pr)
    ro = Room.objects.filter(id=room_name)[0]
    print(ro)
    st = Stock.objects.filter(nse_code=stock_name)[0]
    print(st)
    print(type(current_stock_price))

    x = float(current_stock_price)
    y = int(no_of_shares)

    print(type(x), type(y), x*y)
    total_amount = x*y

    print(total_amount, type(total_amount))
    imp = Join.objects.filter(reg_user_id=pr, room=ro)[0]
    upd = imp.user_money + float(total_amount)
    print(upd)

    Buy.objects.get(reg_user_id=pr, reg_room_id=ro, reg_stock_id=st, current_stock_price = invested_stock_price, no_of_shares = no_of_shares).delete(),

    Join.objects.filter(reg_user_id=pr, room=ro).update(user_money=upd)

    print(room_name, type(room_name))

    x = '/portfolio/' + room_name + '/'
    return redirect(to=x)

def port_push(request,room_name,stock_name,invested_stock_price,current_stock_price,no_of_shares,var):

    request.session['POSTVALUES'] = request.POST.copy(),

    post_values = request.session.get('POSTVALUES')[0],
    print(post_values),

    m = 'quantity' + str(var)
    n = 'output' + str(var)

    x = post_values[0]
    no_of_share = x[m],
    total_amount = x[n],
    print(no_of_share, total_amount)
    m,n = int(no_of_share[0]), float(total_amount[0])

    pr = Profile.objects.filter(user=request.user)[0]
    ro = Room.objects.filter(id=room_name)[0]
    st = Stock.objects.filter(nse_code=stock_name)[0]
    print(type(current_stock_price))

    print(m,n)
    print(Join.objects.filter(reg_user_id=pr, room=ro))
    imp = Join.objects.filter(reg_user_id=pr, room=ro)

    upd = imp[0].user_money + n,
    upd = upd[0]
    print(upd)
    print(pr,ro,st,current_stock_price,no_of_shares)
    if request.method == 'POST':
        if(Buy.objects.filter(reg_user_id=pr, reg_room_id=ro, reg_stock_id=st, current_stock_price=invested_stock_price,no_of_shares=no_of_shares).exists()):
            x = Buy.objects.get(reg_user_id=pr, reg_room_id=ro, reg_stock_id=st, current_stock_price=invested_stock_price)
            x = x.no_of_shares
            if(int(x) == m):
                Buy.objects.get(reg_user_id=pr, reg_room_id=ro, reg_stock_id=st,
                                current_stock_price=invested_stock_price, no_of_shares=no_of_shares).delete(),
            else:
                y = int(x) - m
                Buy.objects.filter(reg_user_id=pr, reg_room_id=ro, reg_stock_id=st, current_stock_price=invested_stock_price).update(no_of_shares=y)

    Join.objects.filter(reg_user_id=pr, room=ro).update(user_money=upd)

    x = '/portfolio/' + room_name + '/'
    return redirect(to=x)