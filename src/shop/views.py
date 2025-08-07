from django.shortcuts import render
from django.db.models import Q
from .models import Product
from .forms import ProductFilterForm

def list_view(request):
    form = ProductFilterForm(request.GET or None)
    products = Product.objects.all()

    if form.is_valid():
        # Create Q objects for filters
        filters = Q()

        # search filter
        if search := form.cleaned_data.get("search"):
            filters &= Q(name__icontains=search)

        # price filters
        if min_price := form.cleaned_data.get("min_price"):
            filters &= Q(price__gte=min_price)
        if max_price := form.cleaned_data.get("max_price"):
            filters &= Q(price__lte=max_price)

        # availability filter
        if availability := form.cleaned_data.get("availability"):
            if availability == "available":
                filters &= Q(is_available=True)
            elif availability == "unavailable":
                filters &= Q(is_available=False)

        # Apply all filters at once
        products = products.filter(filters)

    context = {
        "products": products,
        "form": form
    }
    return render(request, "list_view.html", context)