from ast import Constant
import re
from django.shortcuts import render,redirect
from User.forms import userForm,registerForm
from User.models import Consultant
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView,ListView
from .forms import CreateBlogs
from .models import Blogs
from django.contrib.auth.decorators import login_required
from django.views import View
from django.http import JsonResponse


# Create your views here.

def register(request):
    if request.method=='POST':
        u=userForm(request.POST)
        r=registerForm(request.POST,request.FILES)
        if u.is_valid() and r.is_valid():
            u1=u.save()
            r1=r.save(commit=False)
            r1.user=u1
            c=r1.save()
            # print(c)
            # print(u1)
            if r.cleaned_data['consultant']:
                g=Consultant(consultant_id=u1.Profile,consultant_name=u1.username)
                g.save()
            
            return redirect("login")
            # print(request.POST)
            # print(request.FILES)

        else:
            print(r.errors)
            print(u.errors)
            param={
            'user':u,
            'register':r,
            }
            return render(request,'User/register.html',param)
    else:
        param={
            'user':userForm,
            'register':registerForm,
        }
        return render(request,'User/register.html',param)



@login_required
def subscribe(request):
    c=Consultant.objects.all()
    return render(request,'User/subscribe.html',{'c':c})

@login_required
def blog_list(request):
    b=Consultant.objects.all()
    c=True
    print(b)
    return render(request,'User/blog_list.html',{'b':b})



class PostCreate(LoginRequiredMixin,CreateView):
    model=Blogs
    form_class=CreateBlogs

    def form_valid(self,form):
        print(self.request.user)
        form.instance.author=self.request.user.Profile.Consultant
        return super().form_valid(form)   

class upvote(View):
    def post(self,request):
        r=request.POST['blog']
        if(Blogs.objects.get(pk=r).upvotes.filter(username=request.user).count()==0):
            b1=Blogs.objects.get(pk=r)
            b1.upvotes.add(request.user)
            print(request.user.username)
            print("jkdhw")
            b1.save()
            return JsonResponse({'bool':True})
        else:
            Blogs.objects.get(pk=r).upvotes.remove(request.user)
            return JsonResponse({'bool':False})