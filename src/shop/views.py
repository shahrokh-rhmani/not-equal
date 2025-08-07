from django.db.models import Avg, Q, Count
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProductFilterForm, RatingForm
from .models import Product, Rating

def list_view(request):
    form = ProductFilterForm(request.GET or None)
    products = Product.objects.annotate(
        average_rating=Avg('ratings__score'),
        ratings_count=Count('ratings')
    )

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


def detail_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    # Get or create user rating
    user_rating = None
    if request.user.is_authenticated:
        user_rating = Rating.objects.filter(
            product=product, 
            user=request.user
        ).first()
    
    # Handle rating submission
    if request.method == 'POST' and 'submit_rating' in request.POST:
        if not request.user.is_authenticated:
            return redirect('login')
            
        form = RatingForm(request.POST, instance=user_rating)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.product = product
            rating.user = request.user
            rating.save()
            return redirect('product_detail', pk=product.pk)
    else:
        form = RatingForm(instance=user_rating)
    
    # Get all ratings for this product
    ratings = product.ratings.all().order_by('-created_at')
    
    # Calculate average rating
    average_rating = product.ratings.aggregate(Avg('score'))['score__avg']
    ratings_count = product.ratings.count()
    
    context = {
        'product': product,
        'form': form,
        'ratings': ratings,
        'average_rating': average_rating,
        'ratings_count': ratings_count,
        'user_rating': user_rating,
    }
    return render(request, 'detail_view.html', context)