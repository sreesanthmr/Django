from django.shortcuts import render
from shop.models import Products
from cart.models import Cart,Account,Order
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
@login_required
def cartview(request):
    u=request.user
    cart=Cart.objects.filter(user=u)
    total=0
    for i in cart:
        total+=i.quantity*i.product.price
    return render(request,'cartview.html',{'c':cart,'total':total})
@login_required
def addtocart(request,n):
    p=Products.objects.get(name=n)
    u=request.user
    try:
        cart=Cart.objects.get(user=u,product=p)
        if(cart.product.stock > 0):
            cart.quantity+=1
            cart.save()
            p.stock-=1
            p.save()
    except:
        if(p.stock>0):
            cart=Cart.objects.create(product=p,user=u,quantity=1)
            cart.save()
            p.stock-=1
            p.save()
    return cartview(request)
@login_required
def cart_remove(request,n):
    p=Products.objects.get(name=n)
    u=request.user
    try:
        cart=Cart.objects.get(user=u,product=p)
        if(cart.quantity>1):
            cart.quantity-=1
            cart.save()
            p.stock+=1
            p.save()
        else:
            cart.delete()
    except:
        pass
    return cartview(request)
@login_required
def full_remove(request,n):
    p = Products.objects.get(name=n)
    u = request.user
    try:
        cart = Cart.objects.get(user=u, product=p)

        cart.delete()
    except:
        pass
    return cartview(request)
@login_required
def orderform(request):
    if(request.method=="POST"):
        a=request.POST['a']
        p=request.POST['p']
        n=request.POST['n']

        u=request.user
        cart=Cart.objects.filter(user=u)
        print(n,cart)
        total = 0
        for i in cart:
            total += i.quantity * i.product.price
        try:
            num=int(n)
            test = Account.objects.get(accttype='savings')
            print(test)
            print('num',num, n)
            ac=Account.objects.get(acctnum=n)

            if(ac.amount>=total):
                ac.amount=ac.amount-total
                ac.save()
                for i in cart:
                    o=Order.objects.create(user=u,product=i.product,address=a,phone=p,no_of_items=i.quantity,order_status="paid")
                    o.save()
                cart.delete()
                msg="Your order placed successfully"
                print('hello after loop')
                return render(request,'orderdetails.html',{'msg':msg})
            else:
                msg="Insufficient amount. You cant place order"
                return render(request, 'orderdetails.html', {'msg': msg})
        except Exception as e:
            print(e)
    return render(request,'orderform.html')
@login_required
def orderview(request):
    u=request.user
    o=Order.objects.filter(user=u)

    return render(request,"orderview.html",{'o':o})
