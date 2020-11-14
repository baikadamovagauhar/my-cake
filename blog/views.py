from .cart import Cart
from .models import Type
from .forms import UserForm
from .models import product
from .models import feedback
from .forms import FeedbackForm
from .models import needforvideo
from django.conf import settings
from .forms import RegistrationForm
from django.views.generic import View
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render,get_object_or_404, get_list_or_404,redirect


#Index
def index(request):
    needforvideos=needforvideo.objects.filter(title='my_cake')
    feedbacks=feedback.objects.order_by('-id')
    if request.method == 'POST':
        form=FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
    forma=FeedbackForm()
    popular=product.objects.order_by('price')[:4]
    latest=product.objects.order_by('-created_date')[:4]
    products=product.objects.all()[:4]
    return render(request, 'blog/index.html', {"video":needforvideos,"feedback":feedbacks,'form': forma,"pop":popular,'last':latest,'prods':products})


#Admin
def admin(request):
    return render(request, 'blog/admin.html', {})


#Idea
def mail(request):
    name=request.GET.get('author')
    number=request.GET.get('number')
    idea=request.GET.get('idea')
    msg = render_to_string('mails/idea_mail.html', {'name':name,'number':number,'idea': idea})
    send_mail('Идеи от клиента', msg, settings.EMAIL_HOST_USER ,['qwertyasdfgzxcvpoiu@mail.ru','My_cake_aktau@mail.ru'] )
    needforvideos=needforvideo.objects.filter(title='my_cake')
    feedbacks=feedback.objects.order_by('-id')
    forma=FeedbackForm()
    popular=product.objects.order_by('price')[:4]
    latest=product.objects.order_by('-created_date')[:4]
    products=product.objects.all()[:4]
    return render(request, 'blog/index.html', {"video":needforvideos,"feedback":feedbacks,'form': forma,"pop":popular,'last':latest,'prods':products} )

#All products
def products(request,type,order):
    products=[]
    if type=="tort":
        if order=="chip":
            products=get_list_or_404(product.objects.order_by('price'),type=1)
        else:
            products=get_list_or_404(product.objects.order_by('-price'),type=1)
    elif type=="pirog":
        if order=="chip":
            products=get_list_or_404(product.objects.order_by('price'),type=5)
        else:
            products=get_list_or_404(product.objects.order_by('-price'),type=5)
    elif type=="konfeta":
        if order=="chip":
            products=get_list_or_404(product.objects.order_by('price'),type=3)
        else:
            products=get_list_or_404(product.objects.order_by('-price'),type=3)
    elif type=="desert":
        if order=="chip":
            products=get_list_or_404(product.objects.order_by('price'),type=2)
        else:
            products=get_list_or_404(product.objects.order_by('-price'),type=2)
    elif type=="domash":
        if order=="chip":
            products=get_list_or_404(product.objects.order_by('price'),type=4)
        else:
            products=get_list_or_404(product.objects.order_by('-price'),type=4)
    elif type=="all":
        if order=="chip":
            products=product.objects.order_by('price')
        else:
            products=product.objects.order_by('-price')
    return render(request, 'blog/products.html', {"prods":products, "type":type} )

#Product details
def detail(request,prod_id):
    prod=get_object_or_404(product,id=prod_id)
    return render(request, 'blog/product-detail.html', {"prod":prod, } )

#Cart
def cart(request):
    cart=Cart(request)
    if(request.POST):
        prod_id=request.POST.get('id')
        prod2=get_object_or_404(product,id=prod_id)
        cart.add(prod2)
    sum=cart.get_total_price()
    cart=request.session.get('cart',{})
    return render(request, 'blog/cart.html', {"list":cart,"sum":sum} )


#Delete
def delete(request):
    cart=Cart(request)
    to_del=request.GET.get('delObj')
    prod=get_object_or_404(product,id=to_del)
    cart.remove(prod)
    sum=cart.get_total_price()
    cart=request.session.get('cart',{})
    return render(request, 'blog/cart.html', {"list":cart,"sum":sum,} )


#Change
def change(request):
    cart=Cart(request)
    to_change=request.POST.get('to_change')
    quantity=int(request.POST.get('quantity'))
    prod=product.objects.filter(id=to_change)
    prod=prod[0]
    cart.add(prod,quantity,True)
    sum=cart.get_total_price()
    cart=request.session.get('cart',{})
    return render(request, 'blog/cart.html', {"list":cart,"sum":sum,} )


#Buy
def buy(request):
    cart=Cart(request)
    sum=cart.get_total_price()
    cart=request.session.get('cart',{})
    number=request.GET.get('number')
    if (request.user.is_authenticated):
        name=request.user.username
    else:
        name="Анонимный покупатель"
    msg = render_to_string('mails/Buy_mail.html', {'name':name,'number':number,"list":cart,"sum":sum})
    send_mail('Заказ от клиента', msg, settings.EMAIL_HOST_USER ,['qwertyasdfgzxcvpoiu@mail.ru','My_cake_aktau@mail.ru'] )
    to_clean=Cart(request)
    to_clean.clear()
    return render(request, 'blog/order.html', {"list":cart,"sum":sum} )

#Search
def search(request):
    query=request.GET.get('search')
    if query:
        template='blog/products.html'
        type=Type.objects.filter(name__icontains=query)
        if not type:
            products = product.objects.filter(title__icontains=query)
        else:
            type=type[0]
            products = product.objects.filter(type=type.id)
        context={"prods":products,"type":'all'}
    else:
        template='blog/index.html'
        needforvideos=needforvideo.objects.filter(title='main slider')
        feedbacks=feedback.objects.all()
        forma=FeedbackForm()
        context={"video":needforvideos,"feedback":feedbacks,'form': forma}
    return render(request, template,context )


#Registration
class UserFormView(View):
    form_class=UserForm
    template_name = "registration/register.html"

    #display blank form
    def get(self,request):
        form = self.form_class(None)
        return render(request,self.template_name,{'form':form})


    #process form data
    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            #dont save
            user=form.save(commit=False)

            #cleaned(normalized) data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()#save

            #Returns user object if all ok
            user=authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect("index")
        return render(request,self.template_name,{'form':form})
