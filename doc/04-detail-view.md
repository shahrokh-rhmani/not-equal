<p dir="rtl" align="justify">
در این feature، یک سیستم امتیازدهی به صفحه جزئیات محصول (<span dir="ltr"><code>detail_view</code></span>) اضافه شده است.
</p>

<p dir="rtl" align="justify">
ابتدا یک مدل جدید به نام <span dir="ltr"><code>Rating</code></span> ایجاد شده که شامل فیلدهای <span dir="ltr"><code>product</code></span> (<span dir="ltr"><code>ForeignKey</code></span> به مدل <span dir="ltr"><code>Product</code></span>)، <span dir="ltr"><code>user</code></span> (<span dir="ltr"><code>ForeignKey</code></span> به مدل <span dir="ltr"><code>User</code></span>)، <span dir="ltr"><code>score</code></span> (امتیاز از 1 تا 5)، <span dir="ltr"><code>comment</code></span> و <span dir="ltr"><code>timestamp</code></span> می‌شود.
</p>

<p dir="rtl" align="justify">
سپس یک <span dir="ltr"><code>RatingForm</code></span> طراحی شده که برای ثبت نظرات کاربران استفاده می‌شود.
</p>

<p dir="rtl" align="justify">
در <span dir="ltr"><code>view</code></span> مربوط به صفحه جزئیات محصول (<span dir="ltr"><code>detail_view</code></span>)، منطق نمایش محصول، مدیریت فرم امتیازدهی، محاسبه <span dir="ltr"><code>average_rating</code></span> و نمایش لیست نظرات کاربران پیاده‌سازی شده است.
</p>

<p dir="rtl" align="justify">
در بخش قالب (<span dir="ltr"><code>template</code></span>) نیز یک صفحه <span dir="ltr"><code>detail_view.html</code></span> ایجاد شده که شامل بخش‌های نمایش محصول، فرم ثبت امتیاز و لیست نظرات کاربران می‌باشد.
</p>

<p dir="rtl" align="justify">
همچنین در صفحه <span dir="ltr"><code>list_view</code></span>، امتیاز متوسط محصولات (<span dir="ltr"><code>average_rating</code></span>) و تعداد نظرات (<span dir="ltr"><code>ratings_count</code></span>) به نمایش درآمده است.
</p>

<p dir="rtl" align="justify">
این ویژگی پس از تکمیل به شاخه <span dir="ltr"><code>develop</code></span> <span dir="ltr"><code>merge</code></span> شده است.
</p>


# 1. git branch
```
source venv/bin/activate
```
```
git checkout -b feature/product-detail-rating
```
```
cd src/
```

# 2.

src/shop/models.py
```python
import os
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
```
```python
class Rating(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='ratings',
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='ratings',
    )
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    comment = models.TextField(
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        unique_together = ['product', 'user']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}'s {self.score}-star rating for {self.product.name}"
```
```
python manage.py makemigrations
python manage.py migrate
```

src/shop/forms.py:
```python
from .models import Rating 
```
```python
class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['score', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-control',
                'placeholder': 'نظر خود درباره این محصول بنویسید...'
            }),
        }
        labels = {
            'score': 'امتیاز',
            'comment': 'نظر (اختیاری)',
        }
        error_messages = {
            'score': {
                'required': 'لطفاً به محصول امتیاز دهید.',
                'min_value': 'حداقل امتیاز 1 است.',
                'max_value': 'حداکثر امتیاز 5 است.',
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['score'].widget = forms.HiddenInput()
```


src/shop/views.py:
```python
from django.db.models import Avg, Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProductFilterForm, RatingForm
from .models import Product, Rating
```

```python
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
```
<details>

<summary>explanation code: (src/shop/views.py)</summary>


## 1. 

```python
product = get_object_or_404(Product, pk=pk)
```

<p dir="rtl" align="justify">
در این خط کد، سیستم سعی می‌کند محصولی را با کلید اصلی (<span dir="ltr"><code>pk</code></span>) دریافت شده از <span dir="ltr"><code>URL</code></span> پیدا کند.
</p>

<p dir="rtl" align="justify">
اگر محصول مورد نظر در دیتابیس وجود داشته باشد، به متغیر <span dir="ltr"><code>product</code></span> اختصاص داده می‌شود و برنامه به کار خود ادامه می‌دهد. اما اگر محصولی با این شناسه وجود نداشته باشد، به جای ایجاد خطا یا نمایش صفحه سفید، به طور خودکار یک پاسخ <span dir="ltr"><code>HTTP 404</code></span> (صفحه یافت نشد) به کاربر نمایش داده می‌شود.
</p>

<p dir="rtl" align="justify">
این رویکرد با استفاده از تابع <span dir="ltr"><code>get_object_or_404</code></span> پیاده‌سازی شده که یک روش امن و کاربرپسند برای مدیریت مواردی است که رکورد مورد نظر در دیتابیس وجود ندارد.
</p>

## 2. 

```python
user_rating = None
if request.user.is_authenticated:
    user_rating = Rating.objects.filter(
        product=product, 
        user=request.user
    ).first()
```

<p dir="rtl" align="justify">
در این بخش از کد، سیستم بررسی می‌کند که آیا کاربر فعلی برای محصول مورد نظر قبلاً امتیازی ثبت کرده است یا خیر. ابتدا متغیر <span dir="ltr"><code>user_rating</code></span> با مقدار <span dir="ltr"><code>None</code></span> مقداردهی اولیه می‌شود، که نشان‌دهنده این است که به طور پیش‌فرض فرض می‌شود کاربر هیچ امتیازی نداشته است.
</p>

<p dir="rtl" align="justify">
سپس با استفاده از شرط <span dir="ltr"><code>if request.user.is_authenticated</code></span>، بررسی می‌شود که آیا کاربر فعلی وارد سیستم شده است یا خیر. این بررسی امنیتی مهمی است، زیرا فقط کاربران احراز هویت شده می‌توانند به محصولات امتیاز دهند.
</p>

<p dir="rtl" align="justify">
متد <span dir="ltr"><code>filter()</code></span> دو شرط را بررسی می‌کند:
<ul dir="rtl">
<li><span dir="ltr"><code>product=product</code></span>: امتیاز باید مربوط به محصولی باشد که هم‌اکنون در حال نمایش است</li>
<li><span dir="ltr"><code>user=request.user</code></span>: امتیاز باید متعلق به کاربر فعلی باشد</li>
</ul>
</p>

<p dir="rtl" align="justify">
در نهایت، از <span dir="ltr"><code>first()</code></span> استفاده می‌شود تا فقط اولین امتیاز مطابق با شرایط را برگرداند. نتیجه این جستجو در متغیر <span dir="ltr"><code>user_rating</code></span> ذخیره می‌شود که اگر کاربر قبلاً امتیازی داده باشد، حاوی آن امتیاز خواهد بود.
</p>

<p dir="rtl" align="justify">
این اطلاعات در تمپلیت برای موارد زیر استفاده می‌شود:
<ul dir="rtl">
<li>پر کردن فرم با داده‌های قبلی کاربر</li>
<li>نمایش امتیاز قبلی کاربر</li>
<li>جلوگیری از ارسال امتیازهای تکراری</li>
</ul>
</p>

## <p dir="rtl" align="justify">3. پردازش فرم امتیازدهی:</p>

```python
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
```

<p dir="rtl" align="justify">
این بخش از کد، مسئول پردازش فرم امتیازدهی کاربران به محصولات است. هنگامی که کاربر فرم امتیازدهی را ارسال می‌کند (با تشخیص شرط <span dir="ltr"><code>request.method == 'POST'</code></span> و وجود کلید <span dir="ltr"><code>'submit_rating'</code></span> در داده‌های <span dir="ltr"><code>POST</code></span>)، سیستم یک سری مراحل را برای پردازش این درخواست انجام می‌دهد.
</p>

<p dir="rtl" align="justify">
<strong>بررسی احراز هویت کاربر:</strong><br>
ابتدا سیستم بررسی می‌کند که آیا کاربر وارد سیستم شده است یا خیر. اگر کاربر لاگین نکرده باشد (<span dir="ltr"><code>not request.user.is_authenticated</code></span>)، به صفحه لاگین هدایت می‌شود. این یک مکانیزم امنیتی مهم است که از امتیازدهی کاربران ناشناس جلوگیری می‌کند.
</p>

<p dir="rtl" align="justify">
<strong>ایجاد و اعتبارسنجی فرم:</strong><br>
اگر کاربر احراز هویت شده باشد، سیستم یک نمونه از <span dir="ltr"><code>RatingForm</code></span> ایجاد می‌کند که با دو پارامتر مهم مقداردهی می‌شود:
<ul dir="rtl">
<li><span dir="ltr"><code>request.POST</code></span>: شامل تمام داده‌های ارسالی از فرم</li>
<li><span dir="ltr"><code>instance=user_rating</code></span>: در صورتی که کاربر قبلاً امتیاز داده باشد، فرم با داده‌های قبلی پر می‌شود</li>
</ul>

</p>

<p dir="rtl" align="justify">سپس سیستم اعتبارسنجی فرم را با <span dir="ltr"><code>form.is_valid()</code></span> انجام می‌دهد.</p>
<p dir="rtl" align="justify">
<strong>ذخیره امتیاز:</strong><br>
اگر فرم معتبر باشد، سیستم با استفاده از <span dir="ltr"><code>form.save(commit=False)</code></span> یک شیء <span dir="ltr"><code>Rating</code></span> ایجاد می‌کند و فیلدهای زیر را تنظیم می‌کند:
<ul dir="rtl">
<li><span dir="ltr"><code>rating.product</code></span>: محصول مورد نظر</li>
<li><span dir="ltr"><code>rating.user</code></span>: کاربر فعلی</li>
</ul>
</p>
<p dir="rtl" align="justify">در نهایت، با <span dir="ltr"><code>rating.save()</code></span>، امتیاز در دیتابیس ذخیره می‌شود.</p>
<p dir="rtl" align="justify">
<strong>هدایت کاربر:</strong><br>
کاربر به صفحه جزئیات همان محصول (<span dir="ltr"><code>product_detail</code></span>) هدایت می‌شود. این Redirect از ارسال مجدد فرم در صورت رفرش صفحه جلوگیری می‌کند (الگوی <span dir="ltr"><code>Post/Redirect/Get</code></span>).
</p>

## 4. 

```python
else:
    form = RatingForm(instance=user_rating)
```

<p dir="rtl" align="justify">
این بخش از کد زمانی اجرا می‌شود که کاربر درخواستی از نوع <span dir="ltr"><code>GET</code></span> به صفحه ارسال کرده باشد، یعنی یا برای اولین بار در حال مشاهده صفحه است، یا بدون ارسال فرم، صفحه را رفرش کرده است. در این حالت، سیستم نیاز دارد یک فرم امتیازدهی خالی یا از پیش‌پر شده را برای نمایش در صفحه آماده کند.
</p>

<p dir="rtl" align="justify">
<strong>مکانیزم ایجاد فرم:</strong><br>
متد <span dir="ltr"><code>RatingForm(instance=user_rating)</code></span> یک نمونه از فرم امتیازدهی ایجاد می‌کند که به دو صورت ممکن است مقداردهی شود:
<ul dir="rtl">
<li>اگر کاربر قبلاً برای این محصول امتیاز داده باشد (یعنی <span dir="ltr"><code>user_rating</code></span> مقدار داشته باشد)، فرم به طور خودکار با داده‌های قبلی کاربر پر می‌شود.</li>
<li>اگر کاربر هنوز برای این محصول امتیازی نداده باشد (یعنی <span dir="ltr"><code>user_rating</code></span> برابر <span dir="ltr"><code>None</code></span> باشد)، یک فرم خالی ایجاد می‌شود.</li>
</ul>
</p>

<p dir="rtl" align="justify">
<strong>مزایای این رویکرد:</strong>
<ul dir="rtl">
<li>تجربه کاربری بهتر با امکان مشاهده و ویرایش امتیاز قبلی</li>
<li>جلوگیری از ایجاد امتیازهای تکراری</li>
<li>محدودیت دسترسی فقط برای کاربران احراز هویت شده</li>
<li>حفظ یکپارچگی داده‌ها با استفاده از آخرین امتیاز کاربر</li>
</ul>
</p>

<p dir="rtl" align="justify">
این سیستم با ترکیب <span dir="ltr"><code>GET</code></span> و <span dir="ltr"><code>POST</code></span> در یک ویو، هم امکان نمایش فرم و هم امکان پردازش آن را به صورت یکپارچه فراهم می‌کند.
</p>

## <p dir="rtl" align="justify">5. محاسبات آماری:</p>

```python
ratings = product.ratings.all().order_by('-created_at')
average_rating = product.ratings.aggregate(Avg('score'))['score__avg']
ratings_count = product.ratings.count()
```

<p dir="rtl" align="justify">
در این بخش، سیستم اقدام به جمع‌آوری و محاسبه آمار و اطلاعات مربوط به امتیازات و نظرات محصول می‌کند. این محاسبات سه بخش اصلی دارد:
</p>

<p dir="rtl" align="justify">
<strong>دریافت لیست نظرات:</strong><br>
با استفاده از <span dir="ltr"><code>product.ratings.all().order_by('-created_at')</code></span>، تمام نظرات مرتبط با این محصول از دیتابیس دریافت می‌شوند. دستور <span dir="ltr"><code>order_by('-created_at')</code></span> باعث می‌شود نظرات به ترتیب زمانی نزولی (از جدیدترین به قدیمی‌ترین) مرتب شوند.
</p>

<p dir="rtl" align="justify">
<strong>محاسبه میانگین امتیازها:</strong><br>
سیستم با استفاده از <span dir="ltr"><code>aggregate(Avg('score'))</code></span> میانگین ریاضی تمام امتیازهای داده شده به محصول را محاسبه می‌کند. نتیجه این محاسبه در قالب یک دیکشنری با کلید <span dir="ltr"><code>score__avg</code></span> برگردانده می‌شود.
</p>

<p dir="rtl" align="justify">
<strong>شمارش تعداد نظرات:</strong><br>
تابع <span dir="ltr"><code>count()</code></span> تعداد کل نظرات ثبت شده برای این محصول را می‌شمارد. این عدد به عنوان معیاری از محبوبیت یا توجه به محصول در نظر گرفته می‌شود.
</p>

<p dir="rtl" align="justify">
این اطلاعات در قالب یک دیکشنری به تمپلیت ارسال می‌شوند تا به صورت بصری به کاربران نمایش داده شوند.
</p>
</details>


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
                        <a class="nav-link {% if request.resolver_match.url_name == 'list_view' %}active{% endif %}"
                            href="{% url 'list_view' %}">
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
        {% include '_product_filter.html' %}
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
#
git diff templates/_base.html
```

src/shop/templates/detail_view.html:
```
touch src/shop/templates/detail_view.html
#
touch shop/templates/detail_view.html
```
```html
{% extends '_base.html' %}

{% block title %}{{ product.name }}{% endblock %}

{% block content %}
<div class="container" dir="rtl">
    <div class="row">
        <!-- Product Image -->
        <div class="col-md-6">
            <div class="card shadow-sm mb-4">
                {% if product.image_url %}
                <img src="{{ product.image_url }}" class="card-img-top" alt="{{ product.name }}">
                {% else %}
                <div class="text-center py-5 bg-light">
                    <i class="bi bi-image text-muted" style="font-size: 5rem;"></i>
                </div>
                {% endif %}
            </div>
        </div>
        
        <!-- Product Details -->
        <div class="col-md-6">
            <div class="card shadow-sm mb-4">
                <div class="card-body">
                    <h1 class="h3 mb-3">{{ product.name }}</h1>
                    
                    <!-- Rating -->
                    <div class="mb-3">
                        <div class="mb-1 d-flex">
                            {% with ''|center:5 as range %}
                            {% for _ in range %}
                            {% if forloop.counter <= average_rating|default:0 %} <span class="star filled ms-1">★</span>
                                {% else %}
                                <span class="star ms-1">★</span>
                                {% endif %}
                                {% endfor %}
                                {% endwith %}
                                <span class="text-muted me-2">({{ ratings_count }} رأی)</span>
                        </div>
                    </div>
                    
                    <!-- Price & Availability -->
                    <div class="d-flex justify-content-between align-items-center mb-4">
                        <span class="badge bg-{% if product.is_available %}success{% else %}danger{% endif %} fs-6">
                            {% if product.is_available %}
                            <i class="bi bi-check-circle"></i> موجود
                            {% else %}
                            <i class="bi bi-x-circle"></i> ناموجود
                            {% endif %}
                        </span>
                        <h3 class="text-primary mb-0">{{ product.price }} تومان</h3>
                    </div>
                    
                    <!-- Description -->
                    <div class="mb-4">
                        <h5 class="mb-2">توضیحات محصول</h5>
                        <p class="text-muted">{{ product.description|linebreaks }}</p>
                    </div>
                    
                    <!-- Add to Cart Button -->
                    <div class="d-grid">
                        <button class="btn btn-primary btn-lg">
                            <i class="bi bi-cart-plus"></i> افزودن به سبد خرید
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Rating Section -->
    <div class="row mt-4">
        <div class="col-12">
            <div class="card shadow-sm">
                <div class="card-body">
                    <h3 class="h5 mb-4">ثبت نظر و امتیاز</h3>
                    
                    {% if user_rating %}
                    <div class="alert alert-info mb-4">
                        شما قبلاً به این محصول امتیاز داده‌اید.
                    </div>
                    {% endif %}
                    
                    <form method="post">
                        {% csrf_token %}
                        
                        <!-- Score Field - Star Rating -->
                        <div class="mb-4">
                            <label class="form-label">امتیاز شما</label>
                            <div class="rating-reverse" id="star-rating-container">
                                {% for i in "54321" %}
                                <input class="visually-hidden" type="radio" name="score" id="score{{ i }}" 
                                       value="{{ i }}" {% if form.score.value == i|add:"0" %}checked{% endif %}>
                                <label for="score{{ i }}" class="star">
                                    <span>★</span>
                                </label>
                                {% endfor %}
                            </div>
                            {% if form.score.errors %}
                            <div class="text-danger small mt-2">
                                {{ form.score.errors }}
                            </div>
                            {% endif %}
                        </div>

                        <!-- Comment Field -->
                        <div class="mb-4">
                            <label for="{{ form.comment.id_for_label }}" class="form-label">نظر شما (اختیاری)</label>
                            <textarea name="comment" class="form-control {% if form.comment.errors %}is-invalid{% endif %}" 
                                      rows="4" placeholder="نظر خود درباره این محصول بنویسید...">{{ form.comment.value|default:'' }}</textarea>
                            {% if form.comment.errors %}
                            <div class="invalid-feedback">
                                {{ form.comment.errors }}
                            </div>
                            {% endif %}
                        </div>
                        
                        <button type="submit" name="submit_rating" class="btn btn-primary">
                            ثبت نظر
                        </button>
                    </form>
                </div>
            </div>
        </div>
    </div>
    
    <!-- User Reviews -->
    <div class="row mt-4">
        <div class="col-12">
            <div class="card shadow-sm">
                <div class="card-body">
                    <h3 class="h5 mb-4">نظرات کاربران</h3>
                    
                    {% if ratings %}
                    <div class="list-group">
                        {% for rating in ratings %}
                        <div class="list-group-item border-0 py-3">
                            <div class="d-flex justify-content-between mb-2">
                                <div class="d-flex align-items-center">
                                    <div class="rating me-2 d-flex">
                                        {% with ''|center:5 as range %}
                                        {% for _ in range %}
                                        {% if forloop.counter <= rating.score %} <span class="star filled ms-1">★</span>
                                            {% else %}
                                            <span class="star ms-1">★</span>
                                            {% endif %}
                                            {% endfor %}
                                            {% endwith %}
                                    </div>
                                    <strong>{{ rating.user.get_full_name|default:rating.user.username }}</strong>
                                </div>
                                <small class="text-muted">{{ rating.created_at|date:"Y/m/d" }}</small>
                            </div>
                            {% if rating.comment %}
                            <p class="mb-0">{{ rating.comment }}</p>
                            {% else %}
                            <p class="text-muted mb-0">بدون توضیح</p>
                            {% endif %}
                        </div>
                        {% if not forloop.last %}<hr class="my-1">{% endif %}
                        {% endfor %}
                    </div>
                    {% else %}
                    <div class="text-center py-4">
                        <i class="bi bi-chat-square-text text-muted" style="font-size: 3rem;"></i>
                        <p class="mt-3 text-muted">هنوز نظری ثبت نشده است.</p>
                    </div>
                    {% endif %}
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_css %}
<style>
    .star {
        cursor: pointer;
        transition: all 0.2s ease;
        font-size: 1.5rem;
        color: #6c757d;
    }
    
    .star.filled {
        color: #ffc107;
    }
    
    .rating-reverse {
        display: flex;
        flex-direction: row-reverse;
        justify-content: flex-end;
    }
    
    .rating input[type="radio"] {
        display: none;
    }
    
    .rating label:hover,
    .rating label:hover ~ label,
    .rating input[type="radio"]:checked ~ label {
        color: #ffc107;
    }
    
    .visually-hidden {
        position: absolute;
        width: 1px;
        height: 1px;
        padding: 0;
        margin: -1px;
        overflow: hidden;
        clip: rect(0, 0, 0, 0);
        white-space: nowrap;
        border: 0;
    }
</style>
{% endblock %}

{% block extra_js %}
<script>
document.addEventListener('DOMContentLoaded', function() {
    // Initialize stars based on current selection
    const checkedStar = document.querySelector('#star-rating-container input[type="radio"]:checked');
    if (checkedStar) {
        const stars = document.querySelectorAll('#star-rating-container label');
        const checkedValue = parseInt(checkedStar.value);
        
        stars.forEach((star, index) => {
            if (5 - index <= checkedValue) {
                star.classList.add('filled');
            } else {
                star.classList.remove('filled');
            }
        });
    }
    
    // Handle click events
    document.querySelectorAll('#star-rating-container input[type="radio"]').forEach(star => {
        star.addEventListener('change', function() {
            const stars = document.querySelectorAll('#star-rating-container label');
            const selectedValue = parseInt(this.value);
            
            stars.forEach((star, index) => {
                if (5 - index <= selectedValue) {
                    star.classList.add('filled');
                } else {
                    star.classList.remove('filled');
                }
            });
        });
    });
});
</script>
{% endblock %}
```
<details>

<summary>explanation code: (src/shop/templates/detail_view.html)</summary>


## 1. Rating 

```html
                    <!-- Rating -->
                    <div class="mb-3">
                        <div class="mb-1 d-flex">
                            {% with ''|center:5 as range %}
                            {% for _ in range %}
                            {% if forloop.counter <= average_rating|default:0 %} <span class="star filled ms-1">★</span>
                                {% else %}
                                <span class="star ms-1">★</span>
                                {% endif %}
                                {% endfor %}
                                {% endwith %}
                                <span class="text-muted me-2">({{ ratings_count }} رأی)</span>
                        </div>
                    </div>
```
<p dir="rtl" align="justify">تولید ۵ ستاره:</p>

```django
{% with ''|center:5 as range %}
{% for _ in range %}
```

<p dir="rtl" align="justify">
فیلتر <span dir="ltr"><code>center</code></span> در جنگو معمولاً برای وسط‌چین کردن متن استفاده می‌شود، اما در اینجا برای تولید یک لیست با ۵ عضو به کار رفته است. وقتی از <span dir="ltr"><code>''|center:5</code></span> استفاده می‌کنیم، در واقع به جنگو می‌گوییم: "یک رشته خالی را طوری تنظیم کن که در وسط یک فضای ۵ واحدی قرار بگیرد".
</p>

<p dir="rtl" align="justify">
<strong>مکانیزم کار:</strong><br>
نتیجه این عمل ایجاد یک لیست با ۵ عنصر خالی است.
<ul dir="rtl">
<li>ایجاد حلقه با تعداد تکرار مشخص (۵ بار)</li>
<li>بدون نیاز به تعریف متغیرهای اضافی</li>
<li>با استفاده از امکانات موجود در خود سیستم تمپلیت جنگو</li>
</ul>
</p>

<p dir="rtl" align="justify">
<strong>اجرای حلقه:</strong><br>
با دستور <span dir="ltr"><code>{% for _ in range %}</code></span>:
<ul dir="rtl">
<li>حلقه دقیقاً ۵ بار اجرا می‌شود (به ازای هر ستاره)</li>
<li>از underline (<span dir="ltr"><code>_</code></span>) به عنوان نام متغیر استفاده شده که نشان‌دهنده عدم استفاده از مقدار متغیر است</li>

</ul>
</p>

<p dir="rtl" align="justify">تعیین وضعیت پر/خالی ستاره‌ها:</p>

```django
{% if forloop.counter <= average_rating|default:0 %}
  <span class="star filled ms-1">★</span>
{% else %}
  <span class="star ms-1">★</span>
{% endif %}
```

<p dir="rtl" align="justify">
این بخش از کد، منطق نمایش ستاره‌های پر و خالی را بر اساس میانگین امتیاز محصول پیاده‌سازی می‌کند. هر ستاره در حلقه بر اساس موقعیت خود (که با <span dir="ltr"><code>forloop.counter</code></span> مشخص می‌شود) با میانگین امتیاز محصول (<span dir="ltr"><code>average_rating</code></span>) مقایسه می‌گردد.
</p>

<p dir="rtl" align="justify">
<strong>مکانیزم مقایسه:</strong><br>
<span dir="ltr"><code>forloop.counter</code></span> شماره تکرار فعلی را از ۱ تا ۵ در اختیار قرار می‌دهد. مقایسه به این صورت انجام می‌شود:
<ul dir="rtl">
<li>اگر <span dir="ltr"><code>forloop.counter <= average_rating</code></span>:
<ul>
<li>کلاس <span dir="ltr"><code>filled</code></span> اضافه می‌شود</li>
<li>ستاره به صورت پر (معمولاً با رنگ طلایی) نمایش داده می‌شود</li>
</ul>
</li>
<li>اگر <span dir="ltr"><code>forloop.counter > average_rating</code></span>:
<ul>
<li>ستاره بدون کلاس <span dir="ltr"><code>filled</code></span> نمایش داده می‌شود</li>
<li>معمولاً به صورت خاکستری یا خالی دیده می‌شود</li>
</ul>
</li>
</ul>
</p>


## <p dir="rtl" align="justify">2. مقداردهی اولیه ستاره‌ها</p>

```js
const checkedStar = document.querySelector('#star-rating-container input[type="radio"]:checked');
if (checkedStar) {
    const stars = document.querySelectorAll('#star-rating-container label');
    const checkedValue = parseInt(checkedStar.value);
    
    stars.forEach((star, index) => {
        if (5 - index <= checkedValue) {
            star.classList.add('filled');
        } else {
            star.classList.remove('filled');
        }
    });
}
```

<p dir="rtl" align="justify">
این بخش از کد <span dir="ltr"><code>JavaScript</code></span> مسئول مقداردهی اولیه و نمایش وضعیت فعلی امتیاز ستاره‌ای هنگام بارگذاری صفحه است. هنگامی که صفحه به طور کامل لود می‌شود (رویداد <span dir="ltr"><code>DOMContentLoaded</code></span>)، این کد اجرا می‌شود تا وضعیت فعلی امتیاز کاربر را به درستی نمایش دهد.
</p>

<p dir="rtl" align="justify">
<strong>مکانیزم انتخاب ستاره:</strong><br>
سیستم با استفاده از <span dir="ltr"><code>document.querySelector</code></span> به دنبال ستاره‌ای می‌گردد که قبلاً انتخاب شده باشد (دارای ویژگی <span dir="ltr"><code>:checked</code></span>). این کار با جستجو درون element والد با id <span dir="ltr"><code>star-rating-container</code></span> و میان <span dir="ltr"><code>input</code></span>های نوع <span dir="ltr"><code>radio</code></span> انجام می‌شود.
</p>

<p dir="rtl" align="justify">
<strong>پردازش امتیاز کاربر:</strong><br>
اگر ستاره‌ای انتخاب شده باشد، سیستم:
<ul dir="rtl">
<li>تمام برچسب‌های (<span dir="ltr"><code>label</code></span>) مربوط به ستاره‌ها را جمع‌آوری می‌کند</li>
<li>مقدار عددی ستاره انتخاب شده را با <span dir="ltr"><code>parseInt</code></span> به عدد صحیح تبدیل می‌کند</li>
<li>با حلقه <span dir="ltr"><code>forEach</code></span> روی تمام ستاره‌ها، وضعیت پر یا خالی بودن آنها را تنظیم می‌کند</li>
</ul>
</p>

<p dir="rtl" align="justify">
<strong>منطق نمایش ستاره‌ها:</strong><br>
برای هر ستاره، محاسبه <span dir="ltr"><code>5 - index</code></span> انجام می‌شود تا تطابق صحیحی بین موقعیت بصری و مقدار عددی ایجاد شود. اگر این مقدار کمتر یا مساوی امتیاز کاربر باشد، کلاس <span dir="ltr"><code>filled</code></span> اضافه می‌شود.
</p>
<p dir="rtl" align="justify">نحوه محاسبه برای امتیاز ۳:</p>

```html
<div id="star-rating-container">
  <input type="radio" id="star5" value="5"><label for="star5"></label> <!-- ایندکس 0 -->
  <input type="radio" id="star4" value="4"><label for="star4"></label> <!-- ایندکس 1 -->
  <input type="radio" id="star3" value="3"><label for="star3"></label> <!-- ایندکس 2 -->
  <input type="radio" id="star2" value="2"><label for="star2"></label> <!-- ایندکس 3 -->
  <input type="radio" id="star1" value="1"><label for="star1"></label> <!-- ایندکس 4 -->
</div>
```



| ستاره     | Index | محاسبه (5 - index) | شرط (≤ 3) | نتیجه |
|------------|-------|---------------------|-----------|--------|
| ★★★★★  | 0     | 5 - 0 = 5            | 5 ≤ 3 خیر | خالی   |
| ★★★★   | 1     | 5 - 1 = 4            | 4 ≤ 3 خیر | خالی   |
| ★★★    | 2     | 5 - 2 = 3            | 3 ≤ 3 بله | پر     |
| ★★     | 3     | 5 - 3 = 2            | 2 ≤ 3 بله | پر     |
| ★      | 4     | 5 - 4 = 1            | 1 ≤ 3 بله | پر     |

<p dir="rtl" align="justify">
این مکانیزم تضمین می‌کند که هنگام بارگذاری صفحه، امتیاز قبلی کاربر به درستی نمایش داده شود و تجربه کاربری یکپارچه‌ای ایجاد گردد.
</p>


## <p dir="rtl" align="justify">3. مدیریت کلیک روی ستاره‌ها</p>

```js
document.querySelectorAll('#star-rating-container input[type="radio"]').forEach(star => {
    star.addEventListener('change', function() {
        const stars = document.querySelectorAll('#star-rating-container label');
        const selectedValue = parseInt(this.value);
        
        stars.forEach((star, index) => {
            if (5 - index <= selectedValue) {
                star.classList.add('filled');
            } else {
                star.classList.remove('filled');
            }
        });
    });
});
```

<p dir="rtl" align="justify">
این بخش از کد، سیستم واکنشگرای امتیازدهی ستاره‌ای را پیاده‌سازی می‌کند که به انتخاب‌های کاربر پاسخ می‌دهد. هسته اصلی این کد بر اساس اضافه کردن <span dir="ltr"><code>Event Listener</code></span> به هر یک از دکمه‌های رادیویی (ستاره‌ها) کار می‌کند.
</p>

<p dir="rtl" align="justify">
<strong>مکانیزم رویداد:</strong><br>
وقتی کاربر ستاره‌ای را انتخاب می‌کند، رویداد <span dir="ltr"><code>change</code></span> فعال می‌شود. استفاده از این رویداد به جای <span dir="ltr"><code>click</code></span> مزیت مهمی دارد:
<ul dir="rtl">
<li>کد فقط زمانی اجرا می‌شود که مقدار واقعاً تغییر کرده باشد</li>
<li>از اجرای بی‌مورد کد با کلیک‌های مکرر روی همان گزینه جلوگیری می‌کند</li>
</ul>
</p>

<p dir="rtl" align="justify">
<strong>پردازش انتخاب کاربر:</strong><br>
پس از فعال شدن رویداد، سیستم سه کار اصلی انجام می‌دهد:
<ul dir="rtl">
<li>تمام <span dir="ltr"><code>label</code></span>های مربوط به ستاره‌ها را جمع‌آوری می‌کند</li>
<li>مقدار انتخاب شده توسط کاربر را با <span dir="ltr"><code>parseInt</code></span> به عدد تبدیل می‌نماید</li>
<li>ظاهر ستاره‌ها را بر اساس انتخاب کاربر به‌روزرسانی می‌کند</li>
</ul>
</p>


<p dir="rtl" align="justify">
<strong>مدیریت ظاهر:</strong><br>
کلاس <span dir="ltr"><code>filled</code></span> به صورت پویا مدیریت می‌شود:
<ul dir="rtl">
<li>به ستاره‌های انتخاب شده و ستاره‌های قبل از آن اضافه می‌شود</li>
<li>از ستاره‌های بعدی حذف می‌گردد</li>
</ul>
</p>

<p dir="rtl" align="justify">

</p>

</details>





### or 
```html
                    <!-- Rating -->
                    <div class="mb-3">
                        <div class="mb-1 d-flex">
                            {% for i in "12345" %}
                            {% if forloop.counter <= average_rating|default:0 %} <span class="star filled ms-1">★</span>
                                {% else %}
                                <span class="star ms-1">★</span>
                                {% endif %}
                                {% endfor %}
                                <span class="text-muted me-2">({{ ratings_count }} رأی)</span>
                        </div>
                    </div>
```
```html
                                    <div class="rating me-2 d-flex">
                                        {% for i in "12345" %}
                                        {% if forloop.counter <= rating.score %} <span class="star filled ms-1">★</span>
                                            {% else %}
                                            <span class="star ms-1">★</span>
                                            {% endif %}
                                            {% endfor %}
                                    </div>
```

src/shop/urls.py:
```python
from .views import list_view, detail_view
```
```python
path('<int:pk>/', detail_view, name='product_detail'),
```

# 3. 

src/shop/views.py/list_view:
```python
from django.db.models import Avg, Q, Count
```
```python
    products = Product.objects.annotate(
        average_rating=Avg('ratings__score'),
        ratings_count=Count('ratings')
    )
```

src/shop/templates/list_view.html:
```html
{% extends '_base.html' %}

{% block title %}لیست محصولات{% endblock %}

{% block content %}
<div class="container" dir="rtl">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1 class="h3 mb-0 text-gray-800"><i class="bi bi-grid"></i> لیست محصولات</h1>
    </div>

    <!-- Products Grid -->
    {% if products %}
    <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 row-cols-xl-4 g-4">
        {% for product in products %}
        <div class="col">
            <div class="card h-100">
                {% if product.image_url %}
                <img src="{{ product.image_url }}" class="card-img-top product-img" alt="{{ product.name }}">
                {% else %}
                <div class="text-center py-4 bg-light">
                    <i class="bi bi-image text-muted" style="font-size: 3rem;"></i>
                </div>
                {% endif %}
                <div class="card-body">
                    <h5 class="card-title text-end">{{ product.name }}</h5>
                    
                    <!-- Rating Stars -->
                    <div class="mb-2">
                        <div class="d-flex ">
                            {% with ''|center:5 as range %}
                            {% for _ in range %}
                            {% if forloop.counter <= product.average_rating|default:0 %}
                                <span class="star filled ms-1">★</span>
                            {% else %}
                                <span class="star ms-1">★</span>
                            {% endif %}
                            {% endfor %}
                            {% endwith %}
                            <span class="text-muted small me-2">({{ product.ratings_count|default:0 }})</span>
                        </div>
                    </div>
                    
                    <div class="d-flex justify-content-between align-items-center mb-2">
                        <span class="badge bg-{% if product.is_available %}success{% else %}danger{% endif %}">
                            {% if product.is_available %}
                            <i class="bi bi-check-circle"></i> موجود
                            {% else %}
                            <i class="bi bi-x-circle"></i> ناموجود
                            {% endif %}
                        </span>
                        <h5 class="text-primary mb-0">{{ product.price }} تومان</h5>
                    </div>
                    <p class="card-text text-muted small text-end">{{ product.description|truncatechars:60 }}</p>
                </div>
                <div class="card-footer bg-transparent">
                    <div class="d-grid gap-2">
                        <a href="{% url 'product_detail' pk=product.pk %}" class="btn btn-outline-primary btn-sm">
                            <i class="bi bi-eye"></i> مشاهده جزئیات
                        </a>
                    </div>
                </div>
            </div>
        </div>
        {% endfor %}
    </div>
    {% else %}
    <div class="card shadow">
        <div class="card-body empty-state text-center">
            <i class="bi bi-exclamation-circle"></i>
            <h5 class="mt-3">محصولی یافت نشد</h5>
            <p class="text-muted">با تغییر فیلترهای جستجو مجدداً امتحان کنید</p>
            <a href="?" class="btn btn-primary mt-2">
                <i class="bi bi-arrow-counterclockwise"></i> بازنشانی فیلترها
            </a>
        </div>
    </div>
    {% endif %}

    <!-- Pagination -->
    <nav class="mt-4">
        <ul class="pagination justify-content-center">
            <li class="page-item">
                <a class="page-link" href="#">بعدی</a>
            </li>
            <li class="page-item active"><a class="page-link" href="#">1</a></li>
            <li class="page-item"><a class="page-link" href="#">2</a></li>
            <li class="page-item"><a class="page-link" href="#">3</a></li>
            <li class="page-item">
                <a class="page-link" href="#">قبلی</a>
            </li>
        </ul>
    </nav>
</div>
{% endblock %}

{% block extra_css %}
<style>
    .star {
        cursor: pointer;
        transition: all 0.2s ease;
        font-size: 1.5rem;
        color: #6c757d;
    }
    
    .star.filled {
        color: #ffc107;
    }
</style>
{% endblock %}
```
```
git diff src/shop/templates/list_view.html
# 
git diff shop/templates/list_view.html
```
or 
```html
                    <!-- Rating Stars -->
                    <div class="mb-2">
                        <div class="d-flex">
                            {% for i in "12345" %}
                            {% if forloop.counter <= product.average_rating|default:0 %} <span class="star filled ms-1">
                                ★</span>
                                {% else %}
                                <span class="star ms-1">★</span>
                                {% endif %}
                                {% endfor %}
                                <span class="text-muted small me-2">({{ product.ratings_count|default:0 }})</span>
                        </div>
                    </div>
```
shortcut format HTML
```
Windows: Shift + Alt + F
Linux: Ctrl + Shift + I
```

### tip (rating product):
### error:
```
Reverse for 'login' not found. 'login' is not a valid view function or pattern name.
```
### login admin:
```
http://127.0.0.1:8000/admin/login/?next=/admin/
```

# 4.

cd .. or terminal 2
```
cd ..
```
```
git status
git add .
git commit -m "Implement product detail view with rating functionality" 
```


```
git checkout develop
git merge feature/product-detail-rating
```

remove branch:
```
git branch -d feature/product-detail-rating
```

