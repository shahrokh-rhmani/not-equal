<p dir="rtl" align="justify">  
این commit به <span dir="ltr"><code>refactor</code></span> و بهبود ساختار <span dir="ltr"><code>view</code></span>های مربوط به محصولات می‌پردازد. تغییرات اصلی شامل معرفی یک <span dir="ltr"><code>BaseProductView</code></span> به عنوان <span dir="ltr"><code>parent class</code></span> برای <span dir="ltr"><code>ProductListView</code></span> و <span dir="ltr"><code>ProductDetailView</code></span> است که منطق فیلتر کردن محصولات (<span dir="ltr"><code>filtering</code></span>) را در متد <span dir="ltr"><code>apply_filters</code></span> کپسوله می‌کند.
    </p>

<p dir="rtl" align="justify">  
در این تغییرات، فیلترهای مختلف مانند جستجو (<span dir="ltr"><code>search</code></span>)، محدوده قیمت (<span dir="ltr"><code>price range</code></span>) و وضعیت موجودی (<span dir="ltr"><code>availability</code></span>) با استفاده از <span dir="ltr"><code>Django's Q objects</code></span> پیاده‌سازی شده‌اند. همچنین در <span dir="ltr"><code>ProductListView</code></span> از <span dir="ltr"><code>annotate</code></span> برای محاسبه میانگین امتیاز (<span dir="ltr"><code>average_rating</code></span>) و تعداد نظرات (<span dir="ltr"><code>ratings_count</code></span>) استفاده شده است. بخش <span dir="ltr"><code>template</code></span> نیز شامل یک فایل <span dir="ltr"><code>_product_filter.html</code></span> جداگانه برای نمایش فرم فیلترها و یک <span dir="ltr"><code>_base.html</code></span> به عنوان <span dir="ltr"><code>template</code></span> اصلی است که از <span dir="ltr"><code>Bootstrap 5</code></span> و کتابخانه‌های جانبی مانند <span dir="ltr"><code>noUiSlider</code></span> برای رابط کاربری بهره می‌برد. 
</p>



# 1. git branch
```
source venv/bin/activate
```
```
git checkout -b refactor/product-views
```
```
cd src/
```

# 2.
src/shop/views.py
```python
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
```
<details>

<summary>explanation code: (src/shop/views.py)</summary>

## <p dir="rtl" align="justify">1. تعریف کلاس BaseProductView</p>

```python
class BaseProductView(View):
```

<p dir="rtl" align="justify">
کلاس <span dir="ltr"><code>BaseProductView</code></span> یک کلاس پایه در جنگو است که از <span dir="ltr"><code>django.views.View</code></span> ارث‌بری می‌کند. این کلاس به عنوان والد برای تمام ویوهای مرتبط با محصولات عمل می‌کند و منطق مشترک بین آنها را در یک مکان متمرکز می‌سازد.
</p>

<p dir="rtl" align="justify">
با استفاده از این کلاس پایه، می‌توانیم عملکردهای مشترک مانند فیلتر کردن محصولات، مرتب‌سازی، اعمال شرایط خاص و پیکربندی‌های نمایشی را یک بار پیاده‌سازی کنیم و سپس در تمام ویوهای محصول از آن استفاده نماییم. این رویکرد از تکرار کد جلوگیری کرده و نگهداری سیستم را آسان‌تر می‌کند.
</p>

```python
def apply_filters(self, queryset, request):
```

<p dir="rtl" align="justify">
متد <span dir="ltr"><code>apply_filters</code></span> در کلاس <span dir="ltr"><code>BaseProductView</code></span> با دریافت پارامترهای <span dir="ltr"><code>queryset</code></span> (مجموعه اولیه محصولات) و <span dir="ltr"><code>request</code></span> (اطلاعات درخواست کاربر)، عملیات فیلتر کردن را با استخراج پارامترهای جستجو از <span dir="ltr"><code>request.GET</code></span> انجام داده و با اعمال شرایط Filtering مانند محدوده قیمت، دسته‌بندی و وضعیت موجودی، یک <span dir="ltr"><code>QuerySet</code></span> فیلترشده را بازمی‌گرداند.
</p>

```python
form = ProductFilterForm(request.GET or None)
filtered_queryset = queryset
```

<p dir="rtl" align="justify">
یک نمونه از <span dir="ltr"><code>ProductFilterForm</code></span> ایجاد می‌شود که داده‌های <span dir="ltr"><code>GET</code></span> را دریافت می‌کند و <span dir="ltr"><code>filtered_queryset</code></span> با مقدار اولیه <span dir="ltr"><code>queryset</code></span> مقداردهی می‌شود.
</p>

```python
if form.is_valid():
```

<p dir="rtl" align="justify">بررسی می‌کند که آیا داده‌های ارسالی معتبر هستند یا خیر.</p>

```python
filters = Q()
```

<p dir="rtl" align="justify">
یک شیء <span dir="ltr"><code>Q</code></span> خالی ایجاد می‌شود که برای ساخت شرایط پیچیده فیلتر در جنگو با استفاده از عملگرهای منطقی مانند <span dir="ltr"><code>&</code></span> (AND) و <span dir="ltr"><code>|</code></span> (OR) مورد استفاده قرار می‌گیرد.
</p>

```python
if search := form.cleaned_data.get("search"):
    filters &= Q(name__icontains=search)
```

<p dir="rtl" align="justify">
این بخش با عملگر <span dir="ltr"><code>walrus (:=)</code></span> در پایتون ۳.۸، پارامتر <span dir="ltr"><code>search</code></span> را از داده‌های فرم استخراج و بررسی می‌کند، سپس با <span dir="ltr"><code>Q(name__icontains=search) & = filters</code></span> یک شرط جستجوی غیرحساس به حروف اضافه می‌کند که نتیجه باید تمام شرایط شامل این جستجو باشد.
</p>

```python
if min_price := form.cleaned_data.get("min_price"):
    filters &= Q(price__gte=min_price)
if max_price := form.cleaned_data.get("max_price"):
    filters &= Q(price__lte=max_price)
```

<p dir="rtl" align="justify">
این کد با عملگر <span dir="ltr"><code>walrus (:=)</code></span> فیلترهای قیمت را پردازش می‌کند، به طوری که اگر <span dir="ltr"><code>min_price</code></span> مشخص شده باشد، شرط <span dir="ltr"><code>price__gte</code></span> و اگر <span dir="ltr"><code>max_price</code></span> تعیین شده باشد، شرط <span dir="ltr"><code>price__lte</code></span> با عملگر <span dir="ltr"><code>&=</code></span> به فیلترها اضافه می‌شود تا محدوده قیمتی دقیقی برای جستجوی محصولات ایجاد کند.
</p>

```python
if availability := form.cleaned_data.get("availability"):
    if availability == "available":
        filters &= Q(is_available=True)
    elif availability == "unavailable":
        filters &= Q(is_available=False)
```

<p dir="rtl" align="justify">
این بخش با عملگر <span dir="ltr"><code>walrus (:=)</code></span> وضعیت موجودی را بررسی کرده و براساس مقدار <span dir="ltr"><code>availability</code></span>، شرط <span dir="ltr"><code>is_available=True</code></span> برای محصولات موجود یا <span dir="ltr"><code>is_available=False</code></span> برای محصولات ناموجود را با عملگر <span dir="ltr"><code>&=</code></span> به فیلترها اضافه می‌کند،
</p>

```python
filtered_queryset = queryset.filter(filters)
```

<p dir="rtl" align="justify">
در این مرحله، فیلترهای ترکیبی ذخیره‌شده در <span dir="ltr"><code>filters</code></span> با استفاده از متد <span dir="ltr"><code>filter()</code></span> بر روی <span dir="ltr"><code>queryset</code></span> اصلی اعمال شده و نتیجه نهایی در <span dir="ltr"><code>filtered_queryset</code></span> ذخیره می‌گردد که شامل محصولاتی است که تمام شرایط فیلترگذاری را به صورت همزمان برآورده می‌کنند.
</p>

```python
return filtered_queryset, form
```

<p dir="rtl" align="justify">
متد مورد نظر یک tuple شامل دو مقدار برمی‌گرداند: <span dir="ltr"><code>filtered_queryset</code></span> که مجموعه محصولات فیلترشده بر اساس معیارهای کاربر است، و <span dir="ltr"><code>form</code></span> که نمونه فرم اعمال فیلترها بوده و برای نمایش مجدد در تمپلیت قابل استفاده می‌باشد.
</p>

## <p dir="rtl" align="justify">2. کلاس ProductListView</p>

```python
class ProductListView(BaseProductView, ListView):
    model = Product
    template_name = "list_view.html"
    context_object_name = "products"
```

<p dir="rtl" align="justify">
کلاس <span dir="ltr"><code>ProductListView</code></span> با ارث‌بری از <span dir="ltr"><code>BaseProductView</code></span> و <span dir="ltr"><code>ListView</code></span>، ویویی برای نمایش لیست محصولات ایجاد می‌کند که با تعریف <span dir="ltr"><code>model = Product</code></span>، <span dir="ltr"><code>template_name = "list_view.html"</code></span> و <span dir="ltr"><code>context_object_name = "products"</code></span>، قابلیت‌های فیلتر کردن پیشرفته از کلاس پایه و نمایش استاندارد لیست از <span dir="ltr"><code>ListView</code></span> را ترکیب می‌نماید.
</p>

```python
def get_queryset(self):
    queryset = super().get_queryset()
    queryset, form = self.apply_filters(queryset, self.request)
    queryset = queryset.annotate(
        average_rating=Avg('ratings__score'),
        ratings_count=Count('ratings')
    )
    return queryset
```

<p dir="rtl" align="justify">
متد <span dir="ltr"><code>get_queryset</code></span> در این کلاس، مسئول تهیه و آماده‌سازی مجموعه‌ای از محصولات برای نمایش است. در مرحله اول، با استفاده از <span dir="ltr"><code>super().get_queryset()</code></span>، مجموعه داده‌های پایه را از کلاس والد (<span dir="ltr"><code>ListView</code></span>) دریافت می‌کند. سپس این مجموعه داده‌ها را به همراه درخواست کاربر به متد <span dir="ltr"><code>apply_filters</code></span> ارسال می‌کند که در کلاس پایه <span dir="ltr"><code>BaseProductView</code></span> تعریف شده است. این متد، فیلترهای اعمال شده توسط کاربر (مانند محدوده قیمت، وضعیت موجودی و جستجوی متنی) را پردازش کرده و یک مجموعه داده فیلترشده برمی‌گرداند.
</p>

<p dir="rtl" align="justify">
در مرحله بعد، این متد با استفاده از قابلیت <span dir="ltr"><code>annotate</code></span> جنگو، دو ویژگی محاسباتی مهم به هر محصول اضافه می‌کند. ویژگی <span dir="ltr"><code>average_rating</code></span> با استفاده از تابع جمعی <span dir="ltr"><code>Avg</code></span>، میانگین امتیازات دریافتی هر محصول را محاسبه می‌کند که از طریق رابطه <span dir="ltr"><code>ratings__score</code></span> به مدل <span dir="ltr"><code>Rating</code></span> دسترسی پیدا می‌کند. ویژگی <span dir="ltr"><code>ratings_count</code></span> نیز با تابع <span dir="ltr"><code>Count</code></span>، تعداد کل نظرات دریافتی برای هر محصول را شمارش می‌کند. در نهایت، مجموعه داده‌های کامل شده که شامل محصولات فیلترشده به همراه اطلاعات آماری مربوط به نظرات است، برای استفاده در تمپلیت بازگردانده می‌شود. این رویکرد، امکان نمایش اطلاعات تکمیلی و فیلترهای پیشرفته را در صفحه لیست محصولات فراهم می‌آورد.
</p>

```python
def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['filter_form'] = ProductFilterForm(self.request.GET or None)
    return context
```

<p dir="rtl" align="justify">
متد <span dir="ltr"><code>get_context_data</code></span> در اینجا با گسترش context پایه از کلاس والد، یک فرم فیلتر (<span dir="ltr"><code>ProductFilterForm</code></span>) به داده‌های ارسالی به تمپلیت اضافه می‌کند. این متد ابتدا با استفاده از <span dir="ltr"><code>super().get_context_data(**kwargs)</code></span>، تمام contextهای اصلی شامل لیست محصولات و اطلاعات صفحه‌بندی را از کلاس والد (<span dir="ltr"><code>ListView</code></span>) دریافت می‌کند، سپس یک نمونه جدید از فرم فیلتر ایجاد کرده و آن را با نام <span dir="ltr"><code>filter_form</code></span> به context اضافه می‌نماید. نکته مهم این است که فرم با داده‌های <span dir="ltr"><code>GET</code></span> دریافتی از کاربر (در صورت وجود) مقداردهی اولیه می‌شود، که این امکان را فراهم می‌آورد تا در صورت بازگشت کاربر به صفحه، فیلترهای اعمال شده قبلی در فرم باقی بمانند و تجربه کاربری بهتری ایجاد شود. در نهایت، context کامل شامل هم داده‌های اصلی و هم فرم فیلتر برای استفاده در تمپلیت بازگردانده می‌شود.
</p>

## <p dir="rtl" align="justify">3. کلاس ProductDetailView</p>

```python
class ProductDetailView(BaseProductView, DetailView):
    model = Product
    template_name = "detail_view.html"
    context_object_name = "product"
```

<p dir="rtl" align="justify">
این کلاس با تعیین <span dir="ltr"><code>model = Product</code></span>، به مدل محصولات متصل شده و از طریق <span dir="ltr"><code>template_name = "detail_view.html"</code></span>، تمپلیت مخصوص نمایش جزئیات محصول را مشخص می‌کند. نام متغیر <span dir="ltr"><code>product</code></span> که در تمپلیت قابل دسترسی خواهد بود توسط <span dir="ltr"><code>context_object_name</code></span> تعریف شده است.
</p>

```python
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
```

<p dir="rtl" align="justify">
متد <span dir="ltr"><code>get_context_data</code></span> در این ویو، وظیفه آماده‌سازی و تکمیل داده‌های ارسالی به تمپلیت را بر عهده دارد. در مرحله اول، این متد با استفاده از <span dir="ltr"><code>super().get_context_data(**kwargs)</code></span>، زمینه پایه را از کلاس والد دریافت می‌کند که شامل اطلاعات اصلی محصول می‌شود. سپس یک نمونه از فرم فیلتر محصولات (<span dir="ltr"><code>ProductFilterForm</code></span>) ایجاد کرده و آن را به زمینه اضافه می‌نماید تا امکان فیلتر کردن در صفحه جزئیات نیز وجود داشته باشد. در ادامه، محصول جاری را با متد <span dir="ltr"><code>get_object()</code></span> دریافت کرده و برای کاربران احراز هویت شده، امتیاز قبلی آنها را جستجو می‌کند. این رویکرد امکان نمایش فرم امتیازدهی با داده‌های قبلی کاربر (در صورت وجود) را فراهم می‌آورد.
</p>

<p dir="rtl" align="justify">
در مرحله دوم، این متد اطلاعات تکمیلی مربوط به نظرات محصول را جمع‌آوری می‌کند. تمام نظرات محصول به ترتیب تاریخ ایجاد (از جدید به قدیم) دریافت می‌شوند و میانگین امتیازها و تعداد کل نظرات محاسبه می‌گردد. تمام این اطلاعات شامل فرم امتیازدهی (<span dir="ltr"><code>form</code></span>)، لیست نظرات (<span dir="ltr"><code>ratings</code></span>)، میانگین امتیاز (<span dir="ltr"><code>average_rating</code></span>)، تعداد نظرات (<span dir="ltr"><code>ratings_count</code></span>) و امتیاز کاربر جاری (<span dir="ltr"><code>user_rating</code></span>) با استفاده از متد <span dir="ltr"><code>update</code></span> به context اصلی اضافه می‌شوند.
</p>

```python
def post(self, request, *args, **kwargs):
```

<p dir="rtl" align="justify">
این متد، درخواست‌های <span dir="ltr"><code>POST</code></span> ارسالی به صفحه جزئیات محصول را پردازش می‌کند و به طور خاص مسئول مدیریت عملیات امتیازدهی کاربران به محصولات است.
</p>

```python
if 'submit_rating' in request.POST:
```

<p dir="rtl" align="justify">
این شرط بررسی می‌کند آیا درخواست <span dir="ltr"><code>POST</code></span> حاوی کلید <span dir="ltr"><code>'submit_rating'</code></span> است که نشان‌دهنده ارسال فرم امتیازدهی توسط کاربر می‌باشد.
</p>

```python
if not request.user.is_authenticated:
    return redirect('login')
```

<p dir="rtl" align="justify">
این کد دسترسی غیرمجاز به فرم امتیازدهی را با بررسی <span dir="ltr"><code>user authentication</code></span> مسدود می‌کند و در صورت <span dir="ltr"><code>not logged in</code></span>، کاربر را به صفحه <span dir="ltr"><code>login</code></span> هدایت می‌نماید.
</p>

```python
product = self.get_object()
user_rating = Rating.objects.filter(
    product=product, 
    user=request.user
).first()
```

<p dir="rtl" align="justify">
این بخش <span dir="ltr"><code>محصول موردنظر</code></span> را دریافت کرده و بررسی می‌کند آیا کاربر قبلاً برای این محصول <span dir="ltr"><code>امتیازی ثبت کرده</code></span> است یا خیر، تا در صورت وجود، <span dir="ltr"><code>امتیاز قبلی</code></span> را برای ویرایش بازیابی کند.
</p>

```python
form = RatingForm(request.POST, instance=user_rating)
if form.is_valid():
    rating = form.save(commit=False)
    rating.product = product
    rating.user = request.user
    rating.save()
    return redirect('product_detail', pk=product.pk)
```

<p dir="rtl" align="justify">
این کد <span dir="ltr"><code>فرم امتیازدهی</code></span> را با داده‌های ارسالی کاربر و <span dir="ltr"><code>امتیاز قبلی</code></span> (در صورت وجود) ایجاد می‌کند، سپس پس از <span dir="ltr"><code>اعتبارسنجی</code></span>، امتیاز جدید را با مرتبط کردن به <span dir="ltr"><code>product</code></span> و <span dir="ltr"><code>user</code></span> ذخیره می‌نماید.
</p>

<p dir="rtl" align="justify">
در نهایت کاربر پس از ثبت موفقیت‌آمیز امتیاز، به صفحه <span dir="ltr"><code>جزئیات همان محصول</code></span> هدایت می‌شود تا نتیجه را مشاهده کند. این رویکرد هم از ثبت <span dir="ltr"><code>داده‌های نامعتبر</code></span> جلوگیری می‌کند و هم با استفاده از <span dir="ltr"><code>commit=False</code></span>، امکان تنظیم مقادیر محصول و کاربر قبل از ذخیره نهایی را فراهم می‌آورد.
</p>

```python
context = self.get_context_data(**kwargs)
context['form'] = form
return self.render_to_response(context)
```

<p dir="rtl" align="justify">
این کد در صورت <span dir="ltr"><code>نامعتبر بودن فرم امتیازدهی</code></span>، همان صفحه را با نمایش <span dir="ltr"><code>form</code></span> و <span dir="ltr"><code>خطاهای مربوطه</code></span> بازسازی می‌کند تا کاربر بتواند <span dir="ltr"><code>اصلاحات لازم</code></span> را انجام دهد.
</p>

```python
return super().post(request, *args, **kwargs)
```

<p dir="rtl" align="justify">
این خط درخواست‌های <span dir="ltr"><code>POST</code></span> غیرمرتبط با <span dir="ltr"><code>امتیازدهی</code></span> را به متد <span dir="ltr"><code>post</code></span> اصلی کلاس والد (<span dir="ltr"><code>DetailView</code></span>) منتقل می‌کند تا <span dir="ltr"><code>پردازش استاندارد</code></span> انجام شود.
</p>
</details>







src/shop/urls.py:
```python
from django.urls import path
from .views import ProductListView, ProductDetailView

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
]
```

# 3. 
src/templates/_product_filter.html:
```html
    <!-- Filter Card -->
    <div class="card shadow mb-4">
        <div class="card-header py-3 d-flex justify-content-between align-items-center">
            <h6 class="m-0 font-weight-bold text-white"><i class="bi bi-funnel"></i> فیلتر محصولات</h6>
            <button class="btn btn-sm btn-light" type="button" data-bs-toggle="collapse"
                data-bs-target="#filterCollapse">
                <i class="bi bi-chevron-down"></i>
            </button>
        </div>

        <div class="card-body collapse show" id="filterCollapse">
            <form method="get" class="row g-3" action="{% url 'product_list' %}">
                <!-- search -->
                <div class="col-md-3">
                    <label class="form-label">{{ filter_form.search.label_tag }}</label>
                    {{ filter_form.search }}
                </div>

                <!-- Inventory status -->
                <div class="col-md-2">
                    <label class="form-label">{{ filter_form.availability.label_tag }}</label>
                    {{ filter_form.availability }}
                </div>

                <!-- Price range -->
                <div class="col-md-4">
                    <label for="price-range" class="form-label text-end">محدوده قیمت</label>
                    <div class="d-flex justify-content-between mb-2">
                        <div class="input-group" style="width: 48%;">
                            <span class="input-group-text"><i class="bi bi-currency-dollar"></i></span>
                            <input type="number" class="form-control text-end" id="min_price" name="min_price"
                                value="{{ form.min_price.value|default:0 }}" placeholder="حداقل" min="0">
                        </div>
                        <div class="input-group" style="width: 48%;">
                            <span class="input-group-text"><i class="bi bi-currency-dollar"></i></span>
                            <input type="number" class="form-control text-end" id="max_price" name="max_price"
                                value="{{ form.max_price.value|default:1000000 }}" placeholder="حداکثر" min="0">
                        </div>
                    </div>

                    <div id="price-range" class="mt-5"></div>
                </div>

                <!-- Apply filter button -->
                <div class="col-md-3 filter-btn-container">
                    <div class="mt-auto">
                        <button type="submit" class="btn btn-primary filter-btn w-100">
                            <i class="bi bi-filter"></i> اعمال فیلتر
                        </button>
                    </div>
                </div>
            </form>
        </div>
    </div>
```
```
git diff src/templates/_product_filter.html
```

src/templates/_base.html:
```html
{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Default Title{% endblock %}</title>
    <!-- Bootstrap 5 CSS RTL -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Bootstrap Icons -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css">
    <!-- Vazirmatn font -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/rastikerdar/vazirmatn@v33.003/fonts.css">
    <!-- noUiSlider -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/noUiSlider/15.7.1/nouislider.min.css" />
    <!-- Custom styles-->
    <link rel="stylesheet" href="{% static 'css/main.css' %}">

    {% block extra_css %}{% endblock %}
</head>
<body>
    <!-- Navigation Bar -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark mb-4">
        <div class="container">
            <a class="navbar-brand" href="#">
                <i class="bi bi-shop"></i> فروشگاه آنلاین
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link {% if request.resolver_match.url_name == 'product_list' %}active{% endif %}"
                            href="{% url 'product_list' %}">
                            <i class="bi bi-house"></i> خانه
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#"><i class="bi bi-person"></i> حساب کاربری</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <main class="container mb-5">
        {% if filter_form %}
        {% include '_product_filter.html' %}
        {% endif %}
        {% block content %}{% endblock %}
    </main>

    <!-- Footer -->
    <footer class="bg-dark text-white py-4 mt-5">
        <div class="container text-center">
            <p class="mb-0">© 2023 فروشگاه آنلاین. تمام حقوق محفوظ است.</p>
        </div>
    </footer>

    <!-- Bootstrap 5 JS Bundle with Popper -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <!-- noUiSlider -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/noUiSlider/15.7.1/nouislider.min.js"></script>
    <!-- wnumb -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/wnumb/1.2.0/wNumb.min.js"></script>
    <!-- price-range-slider.js -->
    <script src="{% static 'js/price-range-slider.js' %}"></script>

    {% block extra_js %}{% endblock %}
</body>
</html>
```
```
git diff src/templates/_base.html
```

# 4.

cd .. or terminal 2
```
cd ..
```
```
git status
git add .
git commit -m "Refactor product views with BaseProductView and filter logic" 
```


```
git checkout develop
git merge refactor/product-views
```
remove branch:
```
git branch -d refactor/product-views
```

