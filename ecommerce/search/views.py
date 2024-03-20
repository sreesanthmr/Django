from django.shortcuts import render
from shop.models import Products
from django.db.models import Q
def search(request):
    q=""
    products=None
    if(request.method=="POST"):
        query=request.POST['q']
        if(query):
            products=Products.objects.filter(Q(name__icontains=query) | Q(desc__icontains=query))

    return render(request,'search.html',{'query':query,'p':products})
