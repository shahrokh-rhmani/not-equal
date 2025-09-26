from django.db.models import Q, Avg, Count
from django.shortcuts import redirect
from django.views import View
from django.views.generic import ListView, DetailView

from .forms import ProductFilterForm, RatingForm
from .models import Product, Rating


class BaseProductView(View):
    def apply_filters(self, queryset, request):
        form = ProductFilterForm(request.GET or None)
        filtered_queryset = queryset

        if form.is_valid():
            filters = Q()

            # search filter
            if search := form.cleaned_data.get("search"):
                filters &= Q(name__icontains=search)

            # price filter
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

            filtered_queryset = queryset.filter(filters)

        return filtered_queryset, form
    
class ProductListView(BaseProductView, ListView):
    model = Product
    template_name = "list_view.html"
    context_object_name = "products"
    paginate_by = 4
    ordering = ['-id'] 

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset, form = self.apply_filters(queryset, self.request)
        queryset = queryset.annotate(
            average_rating=Avg('ratings__score'),
            ratings_count=Count('ratings')
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = ProductFilterForm(self.request.GET or None)
        return context


class ProductDetailView(BaseProductView, DetailView):
    model = Product
    template_name = "detail_view.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = ProductFilterForm(self.request.GET or None)
        
        product = self.get_object()
        user_rating = None
        
        if self.request.user.is_authenticated:
            user_rating = Rating.objects.filter(
                product=product, 
                user=self.request.user
            ).first()
        
        form = RatingForm(instance=user_rating)
        ratings = product.ratings.all().order_by('-created_at')
        average_rating = product.ratings.aggregate(Avg('score'))['score__avg']
        ratings_count = product.ratings.count()
        
        context.update({
            'form': form,
            'ratings': ratings,
            'average_rating': average_rating,
            'ratings_count': ratings_count,
            'user_rating': user_rating,
        })
        return context

    def post(self, request, *args, **kwargs):
        if 'submit_rating' in request.POST:
            if not request.user.is_authenticated:
                return redirect('login')
                
            product = self.get_object()
            user_rating = Rating.objects.filter(
                product=product, 
                user=request.user
            ).first()
            
            form = RatingForm(request.POST, instance=user_rating)
            if form.is_valid():
                rating = form.save(commit=False)
                rating.product = product
                rating.user = request.user
                rating.save()
                return redirect('product_detail', pk=product.pk)
            
            # If form is invalid, return to template with the same form
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)
        
        return super().post(request, *args, **kwargs)