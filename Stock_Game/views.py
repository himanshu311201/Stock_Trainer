from django.shortcuts import render,redirect
from nsetools import Nse
from .models import Room, Buy, Join, Stock, Profile, Consultant, Subscribe
from django.shortcuts import render, redirect, get_object_or_404
import ast
from operator import itemgetter
from .models import Stock,Buy,Room, Join
from User.models import Profile,Subscribe,Consultant
from .forms import CreateForm
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
            print("Cutie")
            return render(request, 'Stock_Game/form.html', {'form': form})
    else:
        form = CreateForm()
        print("Bhaadme jaa")
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
            return redirect('home')
    return redirect('home')
def index(request):
    room1 = Room.objects.filter(id=1)
    for i in room1:
        k1 = i
    init = room1[0].room_money
    teams = Join.objects.filter(room=k1)
    nse = Nse()
    Profile1 = Profile.objects.filter(user=request.user)
    room2 = Join.objects.filter(reg_user_id=Profile1[0])
    subs=Subscribe.objects.filter(reg_user=Profile1[0])
    buy2 = Buy.objects.filter(reg_user_id=Profile1[0]).filter(reg_room_id=1)
    sum1=teams[0].user_money
    sum2 = teams[0].user_money
    for j in buy2:
        quote = nse.get_quote(j.reg_stock_id.nse_code)
        sum1 += (quote['buyPrice1'] * j.no_of_shares)
    k3 = 1
    for i in teams:
        p = []
        p.append(i.reg_user_id.user.username)
        buy1 = Buy.objects.filter(reg_user_id=i.reg_user_id).filter(reg_room_id=i.room)
        sum = i.user_money
        k2 = -99999;
        for j in buy1:
            print(j.reg_stock_id)
            quote = nse.get_quote(j.reg_stock_id.nse_code)
            print(quote['buyPrice1'])
            sum += (quote['buyPrice1'] * j.no_of_shares)
        if sum>sum1:
            k3+=1
    param={'rank':k3,'avail':sum2,'profit':(sum1-init),'room':room2,'subs':subs}
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
        d['Price']=quote['buyPrice1']
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
        k2=-99999;
        for j in buy1:
            print(j.reg_stock_id)
            quote = nse.get_quote(j.reg_stock_id.nse_code)
            print(quote['buyPrice1'])
            if k2<quote['buyPrice1']*j.no_of_shares:
                p1=j.reg_stock_id.stock_name
            sum+=(quote['buyPrice1']*j.no_of_shares)
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
    param={'k':k,'money_left':(init-inv),'Profit':(init-inv+sum),'Initial':init,'name':name,'id':id1}
    return render(request, 'Stock_Game/portfolio.html',param)
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

