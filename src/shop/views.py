from django.shortcuts import render
from .models import Product
from django.db.models import Q

def list_view(request):
    search_query = request.GET.get('search', '')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    availability = request.GET.get('availability')

    products = Product.objects.all()

    filters = Q()

    if search_query:
        filters &= Q(name__icontains=search_query)
    
    if min_price:
        filters &= Q(price__gte=min_price)
    
    if max_price:
        filters &= Q(price__lte=max_price)
    
    if availability == 'available':
        filters &= Q(is_available=True)
    elif availability == 'unavailable':
        filters &= Q(is_available=False)

    products = products.filter(filters)

    context = {
        'products': products,
        'search_query': search_query,
        'filters': {
            'min_price': min_price,
            'max_price': max_price,
            'availability': availability,
        }
    }
    
    return render(request, 'list_view.html', context)