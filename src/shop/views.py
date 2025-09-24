from django.shortcuts import render
from .models import Product
from django.db.models import Q

def list_view(request):

    method1 = Product.objects.exclude(price=1000)
    method2 = Product.objects.filter(~Q(price=1000))
    method3 = Product.objects.exclude(price__lt=1000).exclude(price__gt=1000)
    combined = Product.objects.filter(is_available=True).exclude(price=1000)
    
    context = {
        'method1': method1,
        'method2': method2,
        'method3': method3,
        'combined': combined,
    }
    
    return render(request, 'list_view.html', context)