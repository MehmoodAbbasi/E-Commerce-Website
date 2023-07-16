from django.shortcuts import render , redirect
from django.views import View
from .models import Customer , Product , Cart , OrderPlaced
from .forms import CustomerRegistrationForm , CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# Create your views here.

class ProductView(View):
 def get(self, request):
  totalitem = 0
  mobiles = Product.objects.filter(category='M') 
  laptop = Product.objects.filter(category='L') 
  shoes = Product.objects.filter(category='S') 
  jeans = Product.objects.filter(category='J') 
  shirts = Product.objects.filter(category='ST')
  if request.user.is_authenticated:
   totalitem = len(Cart.objects.filter(user=request.user)) 
  return render(request,'home.html',{'mobiles':mobiles,'laptop':laptop,'shoes':shoes,'jeans':jeans,'shirts':shirts,'totalitem':totalitem
  })


# def home(request):
#     return render(request,'home.html')


class ProductDetailView(View):
 def get(self , request, pk):
  product = Product.objects.get(pk=pk)
  already_item = False
  if request.user.is_authenticated:
   already_item = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
  return render(request,'productdetail.html',{'product':product,'already_item':already_item})

# def product_detail(request):
#  return render(request, 'productdetail.html')
@login_required
def add_to_cart(request):
 user =  request.user
 product_id = request.GET.get('prod_id')

 product = Product.objects.get(id=product_id)
 Cart(user=user,product=product).save()
 return redirect('/cart')

def buy_now(request):
 return render(request, 'buynow.html')

@login_required
def show_cart(request):
 totalitem = 0
 if request.user.is_authenticated:  
  totalitem = len(Cart.objects.filter(user=request.user)) 
  user = request.user
  cart = Cart.objects.filter(user=user)
  amount = 0.0
  shipping_amount = 70.0
  total_amunt = 0.0
  cart_product = [p for p in Cart.objects.all() if p.user == user]
  if cart_product:
   for p in cart_product:
    temp_amount = (p.quantity*p.product.discounted_price)
    amount += temp_amount
    totalamount = amount+shipping_amount
    return render(request, 'show_cart.html',{'carts':cart,'totalamount':totalamount,'amount':amount,'totalitem':totalitem})
   else:
    return render(request,'empty_cart.html')

def plus_cart(request):
 if request.method == 'GET':
  prod_id = request.GET['prod_id']
  c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
  c.quantity+=1
  c.save()
  amount = 0.0
  shipping_amount = 70.0
  total_amunt = 0.0
  cart_product = [p for p in Cart.objects.all() if p.user == request.user]
  for p in cart_product:
    temp_amount = (p.quantity*p.product.discounted_price)
    amount += temp_amount
    totalamount = amount+shipping_amount

  data = {
    'quantity':c.quantity,
    'amount':amount,
    'totalamount':totalamount

    }
  return JsonResponse(data)
 

def minus_cart(request):
 if request.method == 'GET':
  prod_id = request.GET['prod_id']
  c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
  c.quantity-=1
  c.save()
  amount = 0.0
  shipping_amount = 70.0
  total_amunt = 0.0
  cart_product = [p for p in Cart.objects.all() if p.user == request.user]
  for p in cart_product:
    temp_amount = (p.quantity*p.product.discounted_price)
    amount += temp_amount
    totalamount = amount+shipping_amount

  data = {
    'quantity':c.quantity,
    'amount':amount,
    'totalamount':totalamount

    }
  return JsonResponse(data)


def remove_cart(request):
 if request.method == 'GET':
  prod_id = request.GET['prod_id']
  c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
  
  c.delete()
  amount = 0.0
  shipping_amount = 70.0
  total_amunt = 0.0
  cart_product = [p for p in Cart.objects.all() if p.user == request.user]
  for p in cart_product:
    temp_amount = (p.quantity*p.product.discounted_price)
    amount += temp_amount

  data = {
    'amount':amount,
    'totalamount':amount + shipping_amount

    }
  return JsonResponse(data)

@method_decorator(login_required,name='dispatch')
class ProfileView(View):
 def get (self,request):
  form = CustomerProfileForm()
  return render(request, 'profile.html',{'form':form,'active':'btn-primary'})
 def post (self,request):
  form = CustomerProfileForm(request.POST)
  if form.is_valid():
   usr = request.user
   name = form.cleaned_data['name']
   locality = form.cleaned_data['locality']
   city = form.cleaned_data['city']
   state = form.cleaned_data['state']
   zipcode = form.cleaned_data['zipcode']
   reg = Customer(user=usr,name=name,locality=locality,city=city,state=state,zipcode=zipcode)
   reg.save()
   messages.success(request, 'Congratulations!! ')
  return render(request, 'profile.html',{'form':form,'active':'btn-primary'}) 

@login_required
def address(request):
 add = Customer.objects.filter(user=request.user)
 return render(request, 'address.html',{'add':add,'active':'btn-primary'})


@login_required
def orders(request):
 totalitem = 0

 op = OrderPlaced.objects.filter(user=request.user)
 if request.user.is_authenticated:
    totalitem = len(Cart.objects.filter(user=request.user)) 
 return render(request, 'orders.html',{'order_placed':op,"totalitem":totalitem})

# def changepassword(request):
#  return render(request, 'changepassword.html')
def imageupload(request):
 return render(request, 'image_upload.html')

def mobile(request,data=None):
 if data == None:
  mobiles = Product.objects.filter(category = 'M')
 elif data == 'Samsung' or data == 'Oppo' or data =='xiaomi':
  mobiles = Product.objects.filter(category = 'M').filter(brand=data)
 elif data == 'below':
  mobiles = Product.objects.filter(category = 'M').filter(discounted_price__lt=10000)
 elif data == 'above':
  mobiles = Product.objects.filter(category = 'M').filter(discounted_price__gt=10000)

 return render(request, 'mobile.html', {'mobiles':mobiles})

def login(request):
 return render(request, 'login.html')

# def customerregistration(request):
#  return render(request, 'customerregistration.html')

class CustomerRegistrationView(View):
  def get(self,request):
   form = CustomerRegistrationForm()
   return render(request, 'customerregistration.html',{'form':form})
  def post(self,request):
   form = CustomerRegistrationForm(request.POST)
   if form.is_valid():
    messages.success(request,"Your account has been created successfully! You are now able to log in ")
    form.save()
    return render(request, 'customerregistration.html',{'form':form})   
 
  

@login_required
def checkout(request):
 totalitem = 0
 user = request.user
 adres = Customer.objects.filter(user=user)
 cart_items = Cart.objects.filter(user=user)
 amount = 0.0
 shipping_amount = 70.0
 total_amunt = 0.0
 cart_product = [p for p in Cart.objects.all() if p.user == request.user]
 if  cart_product:
  for p in cart_product:
    temp_amount = (p.quantity*p.product.discounted_price)
    amount += temp_amount
  totalamount = amount+shipping_amount
  if request.user.is_authenticated:
   totalitem = len(Cart.objects.filter(user=request.user)) 
  return render(request, 'checkout.html',{'adres':adres,'totalamount':totalamount,'cart_items':cart_items,'totalitem':totalitem})


@login_required
def payment_done(request):
 user =  request.user
 custid = request.GET.get('custid')
 customer = Customer.objects.get(id=custid)
 cart = Cart.objects.filter(user=user)
 for c in cart:
  OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity).save()
  c.delete()
  return redirect("orders")



# def jeans(request,data=None):
#  if data == None:
#   jeans = Product.objects.filter(category = 'J')
#  elif data == 'Tommy' or data == 'Cat' or data == 'Qadri' or data == 'Max 3':
#     jeans = Product.objects.filter(category = 'J').filter(brand=data)

#  return render(request, 'jeans.html', {'jeans':jeans} )
# def shirts(request):
#  return render(request, 'shirts.html')
# def shoes(request):
#  return render(request, 'shoes.html')