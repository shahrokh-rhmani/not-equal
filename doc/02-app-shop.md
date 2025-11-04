<p dir="rtl" align="justify">
ابتدا یک <span dir="ltr"><code>branch</code></span> جدید می‌سازیم و یک اپلیکیشن به نام <span dir="ltr"><code>shop</code></span> ایجاد می‌کنیم. سپس یک <span dir="ltr"><code>model</code></span> به نام <span dir="ltr"><code>Product</code></span> تعریف می‌کنیم که فیلدهای پایه‌ای مانند <span dir="ltr"><code>name</code></span>, <span dir="ltr"><code>price</code></span> و <span dir="ltr"><code>is_available</code></span> دارد. برای فیلد تصویر نیز از <span dir="ltr"><code>ImageField</code></span> استفاده می‌کنیم که نیاز به کتابخانه‌ی <span dir="ltr"><code>pillow</code></span> دارد.

پس از آن، با استفاده از <span dir="ltr"><code>fixtures</code></span>، یک سری داده‌ی نمونه مانند لپ‌تاپ، موبایل و... را در دیتابیس وارد می‌کنیم. برای نمایش محصولات، یک <span dir="ltr"><code>list_view</code></span> ایجاد می‌کنیم که با روش‌های مختلف (مانند <span dir="ltr"><code>exclude</code></span> و <span dir="ltr"><code>Q objects</code></span>) محصولات را فیلتر و نمایش می‌دهد. همچنین یک <span dir="ltr"><code>template</code></span> ساده برای آن طراحی می‌شود.

تست‌ها نیز بررسی می‌کنند که فیلترها به درستی کار می‌کنند یا خیر. در نهایت، تغییرات را در <span dir="ltr"><code>branch</code></span> اصلی <span dir="ltr"><code>merge</code></span> می‌کنیم.
</p>

# 1. git branch:
```
source venv/bin/activate
```
```
git checkout -b feature/shop-app
```

# 2. startapp shop:
```
cd src
```
```
python manage.py startapp shop
```

src/config/settings.py
```python
INSTALLED_APPS = [
    ...
    'shop',
]
```

```
touch src/shop/urls.py
#
touch shop/urls.py
```

src/shop/urls.py
```python
from django.urls import path

urlpatterns = [
    path('', ),
]
```

src/shop/templates/
```
mkdir src/shop/templates/
#
mkdir shop/templates/
```

### git commit:
```
git status
git add .
git commit -m "Add new shop app with basic setup" 
```

# 3. Model Product:
src/shop/models.py
```python
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    is_available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='products/', null=True, blank=True)

    def __str__(self):
        return self.name
```

install pillow:
```
pip install pillow
```

requirements.txt:
```
pip freeze > requirements.txt
cat requirements.txt
```

migrations:
```
python manage.py makemigrations
python manage.py migrate
```

# 4. Fixtures:

<details>

<summary>what is Fixture:</summary>
<p dir="rtl" align="justify">Fixtures راهی برای بارگذاری داده‌های اولیه یا نمونه (sample data) در پایگاه داده Django هستند. </p>
</details>

src/media/
```
mkdir src/media/
mkdir src/media/products
#
mkdir media/
mkdir media/products
```

fixtures:
```
mkdir src/shop/fixtures/
touch src/shop/fixtures/products.json
#
mkdir shop/fixtures/
touch shop/fixtures/products.json
```

src/shop/fixtures/products.json
```json
[
  {
    "model": "shop.product",
    "pk": 1,
    "fields": {
      "name": "لپ‌تاپ",
      "price": 1500,
      "is_available": true,
      "image": "products/laptop.jpg"
    }
  },
  {
    "model": "shop.product",
    "pk": 2,
    "fields": {
      "name": "موبایل",
      "price": 2000,
      "is_available": true,
      "image": "products/mobile.jpg"
    }
  },
  {
    "model": "shop.product",
    "pk": 3,
    "fields": {
      "name": "تبلت",
      "price": 1000,
      "is_available": false,
      "image": "products/tablet.jpg"
    }
  },
  {
    "model": "shop.product",
    "pk": 4,
    "fields": {
      "name": "ps4",
      "price": 500,
      "is_available": false,
      "image": "products/ps4.jpg"
    }
  },
  {
    "model": "shop.product",
    "pk": 5,
    "fields": {
      "name": "ps5",
      "price": 1000,
      "is_available": true,
      "image": "products/ps5.jpg"
    }
  }
]
```

run command in terminal
```
python manage.py loaddata products
```

test
```
python manage.py shell
```

```python
from shop.models import Product
Product.objects.all().count()
```

```
exit()
```

cd .. or terminal 2
```
git status
git add .
git commit -m "Add initial product fixtures" 
```

# 5. list view:

### src/shop/admin.py
```python
from django.contrib import admin
from .models import Product

admin.site.register(Product)
```

### src/shop/views.py
```python
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
```

<details>

<summary>explanation code: (src/shop/views.py)</summary>

## <p dir="rtl" align="justify"> روش اول: استفاده از متد exclude()</p>

```python
method1 = Product.objects.exclude(price=1000)
```


<p dir="rtl" align="justify">
در این روش از متد <span dir="ltr"><code>exclude()</code></span> برای فیلتر کردن محصولات استفاده شده است. عبارت  
<span dir="ltr"><code>method1 = Product.objects.exclude(price=1000)</code></span>  
به سادگی تمام محصولاتی را که قیمت آنها برابر با ۱۰۰۰ نیست را از پایگاه داده بازیابی می‌کند.
</p>

<p dir="rtl" align="justify">متد <span dir="ltr"><code>exclude()</code></span> در Django ORM به عنوان یک فیلتر معکوس عمل می‌کند، به این معنا که به جای انتخاب رکوردهای منطبق با شرط، تمام رکوردهایی که با شرط داده شده مطابقت ندارند را انتخاب می‌کند. این متد برای مواردی که می‌خواهیم رکوردها را بر اساس عدم وجود یک ویژگی خاص فیلتر کنیم بسیار مناسب و خوانا است.</p>

<p dir="rtl" align="justify">مزیت اصلی این روش سادگی و خوانایی بالای آن است، به خصوص برای شرایط ساده‌تر. وقتی نیاز به فیلتر کردن بر اساس یک شرط منفی داریم، استفاده از <span dir="ltr"><code>exclude()</code></span> معمولاً مستقیم‌تر و گویاتر از سایر روش‌ها خواهد بود. این متد معادل SQL به صورت <code>WHERE NOT (price = 1000)</code>اجرا می‌شود.</p>

## <p dir="rtl" align="justify"> روش دوم: استفاده از Q object با عملگر NOT</p>

```python
method2 = Product.objects.filter(~Q(price=1000))
```

<p dir="rtl" align="justify">در این روش از <code>Q object</code> همراه با عملگر <code>NOT (~)</code> برای فیلتر کردن محصولات استفاده شده است. عبارت <code>method2 = Product.objects.filter(~Q(price=1000))</code> دقیقاً همان نتیجه‌ای را تولید می‌کند که method1 با استفاده از <code>exclude()</code></span> ایجاد کرد، اما با سینتکس متفاوت.</p>

<p dir="rtl" align="justify">در اینجا، <code>Q(price=1000)</code> یک شرط کوئری ایجاد می‌کند که قیمت محصول باید برابر با 1000 باشد. وقتی این شرط را با عملگر <code>NOT (~)</code> ترکیب می‌کنیم، معنی آن معکوس می‌شود و به "قیمت محصول برابر با 1000 نباشد" تبدیل می‌شود. این روش انعطاف‌پذیری بیشتری دارد، به خصوص وقتی بخواهیم شرایط پیچیده‌تری با ترکیب AND و OR ایجاد کنیم.</p>

<p dir="rtl" align="justify">تفاوت اصلی این روش با <span dir="ltr"><code>exclude()</code></span> در این است که <code>Q object</code> می‌تواند برای ساخت کوئری‌های بسیار پیچیده‌تر استفاده شود، در حالی که <span dir="ltr"><code>exclude()</code></span> ساده‌تر و مستقیم‌تر است. </p>

## <p dir="rtl" align="justify"> روش سوم: ترکیب دو شرط exclude برای یافتن مقادیر دقیق</p>

```python
method3 = Product.objects.exclude(price__lt=1000).exclude(price__gt=1000)
```

<p dir="rtl" align="justify">
این روش از ترکیب دو فیلتر <code>exclude</code> پیاپی برای یافتن محصولاتی با قیمت دقیقاً برابر 1000 استفاده می‌کند. در مرحله اول، عبارت <code>exclude(price__lt=1000)</code> تمام محصولاتی که قیمت آنها کمتر از 1000 است را از نتایج حذف می‌کند. سپس در مرحله دوم، <code>exclude(price__gt=1000)</code> محصولاتی که قیمت بالاتر از 1000 دارند نیز حذف می‌شوند.
</p>

<p dir="rtl" align="justify">
نتیجه نهایی این دو فیلتر متوالی، مجموعه‌ای از محصولات خواهد بود که قیمت آنها نه کمتر از 1000 است و نه بیشتر از 1000، یعنی دقیقاً برابر با 1000 می‌باشد. این روش برخلاف دو روش قبلی که محصولاتی با قیمت غیر از 1000 را برمی‌گرداندند، دقیقاً محصولاتی را انتخاب می‌کند که قیمتشان برابر 1000 است.
</p>

## <p dir="rtl" align="justify"> فیلتر ترکیبی: شرط موجود بودن و قیمت غیر از 1000</p>

```python
combined = Product.objects.filter(is_available=True).exclude(price=1000)
```

<p dir="rtl" align="justify">
در این روش از ترکیب دو شرط برای فیلتر کردن محصولات استفاده شده است. عبارت <code>combined = Product.objects.filter(is_available=True).exclude(price=1000)</code> ابتدا محصولات را بر اساس وضعیت موجودی فیلتر می‌کند و سپس از بین آنها مواردی که قیمت برابر با <code>1000</code> دارند را حذف می‌نماید.
</p>

<p dir="rtl" align="justify">این کوئری در واقع دو شرط اساسی را اعمال می‌کند:</p>

<p dir="rtl" align="justify">
1. شرط مثبت (فیلتر): فقط محصولاتی که در دسترس هستند و مقدار فیلد <code>is_available</code> آنها <code>True</code> است را انتخاب می‌کند.
</p>

<p dir="rtl" align="justify">
2. شرط منفی (exclude): از بین محصولات موجود، آنهایی که قیمت دقیقاً برابر با <code>1000</code> دارند را از نتایج نهایی حذف می‌کند.
</p>

</details>

### src/config/urls.py
```python
urlpatterns = [
  ...
  path('', include('shop.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### src/shop/urls.py
```python
from django.urls import path
from .views import list_view

urlpatterns = [
    path('', list_view, name='list_view'),
]
```

# 6. templates:

src/templates/_base.html
```
touch src/templates/_base.html
# 
touch templates/_base.html
```

```html
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}Default Title{% endblock %}</title>

</head>
<body>
    {% block content %}

    {% endblock %}
    

</body>
</html>
```


src/shop/templates/list_view.html
```
touch src/shop/templates/list_view.html
#
touch shop/templates/list_view.html
```

```html
{% extends '_base.html' %}

{% block title %}Product List{% endblock %}

{% block content %}
    <h2>Method 1: exclude(price=1000)</h2>
    <ul>
        {% for product in method1 %}
            <li>{{ product.name }} - {{ product.price }} - Available: {{ product.is_available }}</li>
        {% endfor %}
    </ul>
    
    <h2>Method 2: filter(~Q(price=1000))</h2>
    <ul>
        {% for product in method2 %}
            <li>{{ product.name }} - {{ product.price }} - Available: {{ product.is_available }}</li>
        {% endfor %}
    </ul>
    
    <h2>Method 3: exclude(lt).exclude(gt)</h2>
    <ul>
        {% for product in method3 %}
            <li>{{ product.name }} - {{ product.price }} - Available: {{ product.is_available }}</li>
        {% endfor %}
    </ul>
    
    <h2>Combined: Available and price != 1000</h2>
    <ul>
        {% for product in combined %}
            <li>{{ product.name }} - {{ product.price }} - Available: {{ product.is_available }}</li>
        {% endfor %}
    </ul>
{% endblock %}
```

```
python manage.py runserver
```

# 7. test:

src/shop/test.py
```python
import logging

from django.test import TestCase
from django.urls import reverse

from .models import Product


class ListViewTestCase(TestCase):
    fixtures = ['products.json'] 

    def test_list_view_status_code(self):
        response = self.client.get(reverse('list_view'))
        self.assertEqual(response.status_code, 200)

    def test_method1_excludes_price_1000(self):
        response = self.client.get(reverse('list_view'))
        method1_products = response.context['method1']  

        expected_count = Product.objects.exclude(price=1000).count()
        logger = logging.getLogger(__name__)
        logger.info(f"method1-exclude-(Expected number of products): {expected_count}")
        logger.info(f"method1-exclude-(Number of returned products): {method1_products.count()}")
        
        self.assertEqual(method1_products.count(), expected_count)
        self.assertFalse(any(p.price == 1000 for p in method1_products))

    def test_method2_excludes_price_1000(self):
        response = self.client.get(reverse('list_view'))
        method2_products = response.context['method2']

        expected_count = Product.objects.exclude(price=1000).count()
        logger = logging.getLogger(__name__)
        logger.info(f"method2-~Q-(Expected number of products): {expected_count}")
        logger.info(f"method2-~Q-(Number of returned products): {method2_products.count()}")
        
        self.assertEqual(method2_products.count(), expected_count)
        self.assertFalse(any(p.price == 1000 for p in method2_products))

    def test_method3_excludes_price_1000(self):
        response = self.client.get(reverse('list_view'))
        method3_products = response.context['method3']

        expected_count = Product.objects.exclude(price__lt=1000).exclude(price__gt=1000).count()
        logger = logging.getLogger(__name__)
        logger.info(f"method3-lt-gt-(Expected number of products): {expected_count}")
        logger.info(f"method3-lt-gt-(Number of returned products): {method3_products.count()}")
        
        self.assertEqual(method3_products.count(), expected_count)

    def test_combined_filter(self):
        response = self.client.get(reverse('list_view'))
        combined_products = response.context['combined']
        
        self.assertEqual(combined_products.count(), 2)
        self.assertTrue(all(p.is_available and p.price != 1000 for p in combined_products))
```

src/config/settings.py
```python
# Logging settings for tests
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'shop': {  # your app name.
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
```

```
python manage.py test
```

or

src/shop/test.py
```python
from django.test import TestCase, Client
from .models import Product

class ListViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        
        # Create test products
        self.product1 = Product.objects.create(name="Product 1", price=900, is_available=True)
        self.product2 = Product.objects.create(name="Product 2", price=1000, is_available=True)
        self.product3 = Product.objects.create(name="Product 3", price=1100, is_available=False)
        self.product4 = Product.objects.create(name="Product 4", price=1000, is_available=False)
        self.product5 = Product.objects.create(name="Product 5", price=800, is_available=True)

    # Test method1 excludes products with price=1000 using exclude()
    def test_method1_excludes_price_1000(self):
        response = self.client.get('/')
        method1_results = response.context['method1']
        
        self.assertEqual(method1_results.count(), 3)
        self.assertFalse(method1_results.filter(price=1000).exists())
        
        self.assertIn(self.product1, method1_results)
        self.assertIn(self.product5, method1_results)
        self.assertNotIn(self.product2, method1_results)
        self.assertNotIn(self.product4, method1_results)

    # Test method2 excludes products with price=1000 using Q objects
    def test_method2_excludes_price_1000_with_q(self):
        response = self.client.get('/')
        method2_results = response.context['method2']
        
        self.assertEqual(method2_results.count(), 3)
        self.assertFalse(method2_results.filter(price=1000).exists())
        
        method1_results = response.context['method1']
        self.assertEqual(set(method1_results), set(method2_results))

    #  Test method3 gets only products with price=1000 using double exclude
    def test_method3_gets_only_price_1000(self):
        response = self.client.get('/')
        method3_results = response.context['method3']
        
        self.assertEqual(method3_results.count(), 2)
        self.assertTrue(all(p.price == 1000 for p in method3_results))
        
        expected_products = {self.product2, self.product4}
        self.assertEqual(set(method3_results), expected_products)

    # Test combined filter: available=True and price!=1000
    def test_combined_filters_available_and_excludes_price_1000(self):
        response = self.client.get('/')
        combined_results = response.context['combined']
        
        self.assertEqual(combined_results.count(), 2)
        
        self.assertIn(self.product1, combined_results)
        self.assertIn(self.product5, combined_results)
        self.assertNotIn(self.product2, combined_results)
        self.assertNotIn(self.product3, combined_results)
        self.assertNotIn(self.product4, combined_results)
        
        self.assertTrue(all(p.is_available for p in combined_results))
        self.assertTrue(all(p.price != 1000 for p in combined_results))

    # Test that correct template is used
    def test_template_used(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'list_view.html')

    # Test that method1 and method2 produce identical results
    def test_method1_and_method2_consistency(self):
        response = self.client.get('/')
        method1 = set(response.context['method1'])
        method2 = set(response.context['method2'])
        self.assertEqual(method1, method2)
        
        combined = set(response.context['combined'])
        self.assertTrue(combined.issubset(method1))
```

```
python manage.py test
```


<details>

<summary>explanation code:</summary>

# test 1:

## <p dir="rtl" align="justify">کلاس ListViewTestCase</p>

```python
class ListViewTestCase(TestCase):
    fixtures = ['products.json']
```
<p dir="rtl" align="justify">  
ویژگی مهم این کلاس، استفاده از <code>fixtures</code> است که با مقدار <code>['products.json']</code> تعریف شده است. این تنظیم به <code>Django</code> دستور می‌دهد که قبل از اجرای هر یک از متدهای تست در این کلاس، ابتدا داده‌های تست از فایل <code>products.json</code> را در پایگاه داده تست بارگذاری کند. فایل <code>fixture</code> (در اینجا <code>products.json</code>) معمولاً حاوی نمونه داده‌های از پیش تعریف شده است که شرایط مختلفی را برای تست عملکرد <code>view</code> شبیه‌سازی می‌کنند. این رویکرد باعث می‌شود تست‌ها در یک محیط کنترل شده با داده‌های ثابت و شناخته شده اجرا شوند که نتیجه‌ای قابل اطمینان و تکرارپذیر تولید می‌کند.  
</p>
<p dir="rtl" align="justify">
استفاده از <code>fixtures</code> در تست‌های <code>Django</code> چند مزیت مهم دارد: اولاً نیاز به ایجاد دستی داده‌های تست در هر بار اجرا را برطرف می‌کند، ثانیاً تضمین می‌کند که تمام تست‌ها با مجموعه داده‌های یکسانی کار می‌کنند، و ثالثاً امکان اشتراک‌گذاری داده‌های تست بین چندین کلاس تست مختلف را فراهم می‌آورد. در این مورد خاص، کلاس <code>ListViewTestCase</code> از این <code>fixture</code> برای تست عملکردهای مختلف فیلتر کردن محصولات استفاده می‌کند.
</p>

## <p dir="rtl" align="justify">متد test_list_view_status_code</p>

```python
def test_list_view_status_code(self):
    response = self.client.get(reverse('list_view'))
    self.assertEqual(response.status_code, 200)
```

<p dir="rtl" align="justify">
این تابع تست، یکی از اساسی‌ترین بررسی‌ها را در تست‌های <span dir="ltr"><code>Django</code></span> انجام می‌دهد، بررسی صحت عملکرد اولیه یک <span dir="ltr"><code>view</code></span>. تابع <span dir="ltr"><code>test_list_view_status_code</code></span> با استفاده از کلاینت تست <span dir="ltr"><code>Django</code></span> (که از طریق <span dir="ltr"><code>self.client</code></span> در دسترس است)، یک درخواست <span dir="ltr"><code>GET</code></span> به آدرس مربوط به <span dir="ltr"><code>view</code></span> با نام <span dir="ltr"><code>'list_view'</code></span> ارسال می‌کند.
</p>

<p dir="rtl" align="justify">
در اینجا، تابع <span dir="ltr"><code>reverse</code></span> نقش کلیدی ایفا می‌کند؛ این تابع <span dir="ltr"><code>URL</code></span> مربوط به <span dir="ltr"><code>view</code></span> را بر اساس نام آن (که در فایل <span dir="ltr"><code>urls.py</code></span> تعریف شده) تولید می‌کند. این روش هوشمندانه‌ای است که از وابستگی تست به آدرس‌های ثابت (<span dir="ltr"><code>hardcoded URLs</code></span>) جلوگیری می‌کند و انعطاف‌پذیری بیشتری ایجاد می‌نماید.
</p>

<p dir="rtl" align="justify">
پس از ارسال درخواست، تست با استفاده از <span dir="ltr"><code>assertEqual</code></span> بررسی می‌کند که کد وضعیت پاسخ دریافتی برابر با <span dir="ltr"><code>200</code></span> (موفقیت‌آمیز) باشد. این بررسی اولیه و حیاتی، پایه‌ای برای اطمینان از در دسترس بودن و عملکرد صحیح <span dir="ltr"><code>view</code></span> محسوب می‌شود. اگر این تست با شکست مواجه شود، نشان‌دهنده مشکلات اساسی مانند خطاهای <span dir="ltr"><code>routing</code></span>، دسترسی یا اجرای <span dir="ltr"><code>view</code></span> خواهد بود. موفقیت این تست، پیش‌نیاز بررسی‌های دقیق‌تر و تخصصی‌تر در تست‌های بعدی محسوب می‌شود.
</p>

## <p dir="rtl" align="justify">متد test_method1_excludes_price_1000</p>

```python
def test_method1_excludes_price_1000(self):
    response = self.client.get(reverse('list_view'))
    method1_products = response.context['method1']
    
    expected_count = Product.objects.exclude(price=1000).count()
    logger.info(f"method1-exclude-(Expected number of products): {expected_count}")
    logger.info(f"method1-exclude-(Number of returned products): {method1_products.count()}")
    
    self.assertEqual(method1_products.count(), expected_count)
    self.assertFalse(any(p.price == 1000 for p in method1_products))
```

<p dir="rtl" align="justify">
این متد تست، عملکرد فیلتر <span dir="ltr"><code>exclude(price=1000)</code></span> را در سیستم مورد بررسی قرار می‌دهد. تست با ارسال درخواست <span dir="ltr"><code>GET</code></span> به <span dir="ltr"><code>view</code></span> مربوطه آغاز می‌شود و سپس مجموعه محصولات فیلترشده را از <span dir="ltr"><code>context</code></span> پاسخ با کلید <span dir="ltr"><code>method1</code></span> استخراج می‌کند.
</p>

<p dir="rtl" align="justify">
در مرحله بعد، تست با ایجاد یک معیار مقایسه (<span dir="ltr"><code>expected_count</code></span>) از طریق کوئری مستقیم به مدل <span dir="ltr"><code>Product</code></span>، تعداد مورد انتظار محصولاتی که قیمت آنها برابر با <span dir="ltr"><code>1000</code></span> نیست را محاسبه می‌کند. برای افزایش شفافیت تست و کمک به فرآیند دیباگ، از سیستم <span dir="ltr"><code>logging</code></span> استفاده شده و اطلاعات مهم شامل تعداد مورد انتظار و تعداد واقعی محصولات بازگشتی در لاگ ثبت می‌شوند.
</p>

<p dir="rtl" align="justify">
سپس تست دو <span dir="ltr"><code>assertion</code></span> اصلی انجام می‌دهد: اولاً بررسی می‌کند که تعداد محصولات بازگشتی توسط <span dir="ltr"><code>view</code></span> دقیقاً برابر با تعداد مورد انتظار باشد. ثانیاً با استفاده از یک حلقه و تابع <span dir="ltr"><code>any</code></span>، اطمینان حاصل می‌کند که در مجموعه نتایج، حتی یک محصول با قیمت <span dir="ltr"><code>1000</code></span> وجود ندارد. این بررسی دوگانه، هم صحت تعداد و هم صحت منطق فیلتر را تضمین می‌کند و از عملکرد صحیح متد <span dir="ltr"><code>exclude</code></span> در شرایط واقعی اطمینان حاصل می‌نماید.
</p>

## <p dir="rtl" align="justify">متد test_method2_excludes_price_1000</p>

```python
def test_method2_excludes_price_1000(self):
    response = self.client.get(reverse('list_view'))
    method2_products = response.context['method2']

    expected_count = Product.objects.exclude(price=1000).count()
    logger.info(f"method2-~Q-(Expected number of products): {expected_count}")
    logger.info(f"method2-~Q-(Number of returned products): {method2_products.count()}")
    
    self.assertEqual(method2_products.count(), expected_count)
    self.assertFalse(any(p.price == 1000 for p in method2_products))
```

<p dir="rtl" align="justify">
این متد تست، رویکرد جایگزینی برای فیلتر کردن محصولات با استفاده از <span dir="ltr"><code>Q objects</code></span> را مورد بررسی قرار می‌دهد. برخلاف متد قبلی که از <span dir="ltr"><code>exclude()</code></span> ساده استفاده می‌کرد، اینجا از <span dir="ltr"><code>filter(~Q(price=1000))</code></span> بهره گرفته شده که یک روش پیشرفته‌تر و انعطاف‌پذیرتر برای ساخت کوئری‌های پیچیده در <span dir="ltr"><code>Django</code></span> است.
</p>

<p dir="rtl" align="justify">
پس از دریافت پاسخ از <span dir="ltr"><code>view</code></span> و استخراج محصولات از <span dir="ltr"><code>context</code></span> با کلید <span dir="ltr"><code>method2</code></span>، تست دو مرحله اصلی را انجام می‌دهد. ابتدا تعداد مورد انتظار محصولات (با حذف مواردی که قیمتشان <span dir="ltr"><code>1000</code></span> است) محاسبه می‌شود. سپس این مقدار با تعداد واقعی محصولات بازگشتی مقایسه می‌گردد. لاگ‌های ثبت شده شامل اطلاعات مقایسه‌ای، امکان ردیابی و دیباگ آسان‌تر را فراهم می‌کنند.
</p>

<p dir="rtl" align="justify">
نکته جالب توجه اینجاست که این تست نه تنها صحت تعداد نتایج، بلکه درستی منطق فیلتر را نیز با بررسی تک‌تک آیتم‌ها تأیید می‌کند. انتظار می‌رود نتایج این تست دقیقاً با نتایج متد قبلی (که از <span dir="ltr"><code>exclude</code></span> معمولی استفاده می‌کرد) یکسان باشد، که این موضوع همخوانی و سازگاری دو روش مختلف فیلتر کردن در <span dir="ltr"><code>Django</code></span> را نشان می‌دهد. این رویکرد مقایسه‌ای، اطمینان خاطر مضاعفی از صحت عملکرد سیستم در شرایط مختلف فیلتر کردن ایجاد می‌نماید.
</p>

## <p dir="rtl" align="justify">متد test_method3_excludes_price_1000</p>

```python
def test_method3_excludes_price_1000(self):
    response = self.client.get(reverse('list_view'))
    method3_products = response.context['method3']

    expected_count = Product.objects.exclude(price__lt=1000).exclude(price__gt=1000).count()
    logger.info(f"method3-lt-gt-(Expected number of products): {expected_count}")
    logger.info(f"method3-lt-gt-(Number of returned products): {method3_products.count()}")
    
    self.assertEqual(method3_products.count(), expected_count)
```

<p dir="rtl" align="justify">
برخلاف دو روش قبلی که مستقیماً قیمت‌های برابر با <span dir="ltr"><code>1000</code></span> را حذف می‌کردند، اینجا از ترکیب دو شرط <span dir="ltr"><code>exclude(price__lt=1000)</code></span> و <span dir="ltr"><code>exclude(price__gt=1000)</code></span> استفاده شده است که در عمل معادل "قیمت دقیقاً برابر با <span dir="ltr"><code>1000</code></span> نیست" می‌باشد.
</p>

<p dir="rtl" align="justify">
پس از دریافت پاسخ از <span dir="ltr"><code>view</code></span> و استخراج مجموعه محصولات از <span dir="ltr"><code>context</code></span> با کلید <span dir="ltr"><code>method3</code></span>، تست به شیوه‌ای سیستماتیک پیش می‌رود. ابتدا تعداد مورد انتظار محصولات با اجرای همان منطق فیلتر دوگانه بر روی مدل اصلی محاسبه می‌شود. لاگ‌های دقیق و توصیفی که شامل مقادیر مورد انتظار و واقعی هستند، امکان پایش و عیب‌یابی آسان را فراهم می‌کنند.
</p>

<p dir="rtl" align="justify">
نکته قابل تأمل در این تست، بررسی هم‌خوانی نتایج با دو روش قبلی است. اگرچه از نظر منطقی باید نتایج یکسان باشند، اما این تست به‌صورت مستقل صحت پیاده‌سازی این رویکرد خاص را تأیید می‌کند. این روش به‌خصوص زمانی ارزشمند است که نیاز به ترکیب شرایط پیچیده‌تر فیلتر کردن داشته باشیم و انعطاف‌پذیری بیشتری در ساخت کوئری‌ها مورد نیاز باشد. تست تنها تعداد نتایج را مقایسه می‌کند، چرا که منطق حذف موارد با قیمت <span dir="ltr"><code>1000</code></span> قبلاً در تست‌های دیگر به‌صورت جامع بررسی شده است.
</p>

## <p dir="rtl" align="justify">متد test_combined_filter</p>

```python
def test_combined_filter(self):
    response = self.client.get(reverse('list_view'))
    combined_products = response.context['combined']
    
    self.assertEqual(combined_products.count(), 2)
    self.assertTrue(all(p.is_available and p.price != 1000 for p in combined_products))
```

<p dir="rtl" align="justify">
ترکیب چندین شرط فیلتر به صورت همزمان. تست با ارسال درخواست <span dir="ltr"><code>GET</code></span> به <span dir="ltr"><code>view</code></span> مربوطه آغاز شده و مجموعه محصولات ترکیب‌فیلترشده را از <span dir="ltr"><code>context</code></span> پاسخ با کلید <span dir="ltr"><code>'combined'</code></span> استخراج می‌کند.
</p>

<p dir="rtl" align="justify">
در این تست دو بررسی حیاتی انجام می‌شود:<br>
بررسی کمی: با استفاده از <span dir="ltr"><code>assertEqual</code></span> تأیید می‌کند که دقیقاً <span dir="ltr"><code>2</code></span> محصول با شرایط ترکیبی "موجود بودن" (<span dir="ltr"><code>is_available=True</code></span>) و "قیمت غیر از <span dir="ltr"><code>1000</code></span> در سیستم وجود دارند. این عدد ثابت نشان‌دهنده انتظارات دقیق از مجموعه داده‌های تست است.
</p>

<p dir="rtl" align="justify">
بررسی کیفی: با ترکیب هوشمندانه <span dir="ltr"><code>all</code></span> و یک عبارت شرطی، هر محصول در مجموعه نتایج را از دو جنبه بررسی می‌کند:<br>
- وضعیت موجودی (<span dir="ltr"><code>p.is_available</code></span> باید <span dir="ltr"><code>True</code></span> باشد)<br>
- قیمت محصول (<span dir="ltr"><code>p.price</code></span> نباید برابر با <span dir="ltr"><code>1000</code></span> باشد)
</p>

<p dir="rtl" align="justify">
اطمینان جامعی از عملکرد صحیح سیستم ایجاد می‌نماید. موفقیت این تست تضمین می‌کند که کاربران نهایی فقط محصولات موجود با قیمت‌های مشخص (غیر از <span dir="ltr"><code>1000</code></span>) را مشاهده خواهند کرد.
</p>

## <p dir="rtl" align="justify">فایل src/config/settings.py (بخش مربوط به لاگینگ)</p>

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'shop': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
```

<p dir="rtl" align="justify">
این پیکربندی لاگینگ در <span dir="ltr"><code>Django</code></span> یک ساختار منظم و کارآمد برای مدیریت پیام‌های سیستم ایجاد می‌کند. تنظیمات با مشخص کردن <span dir="ltr"><code>version: 1</code></span> نشان می‌دهد که از فرمت استاندارد پیکربندی لاگینگ پایتون استفاده می‌کند. پارامتر <span dir="ltr"><code>disable_existing_loggers: False</code></span> به سیستم دستور می‌دهد که لاگرهای از پیش تعریف شده را غیرفعال نکند، که این امر برای حفظ یکپارچگی با سایر بخش‌های سیستم حیاتی است.
</p>

<p dir="rtl" align="justify">
در بخش <span dir="ltr"><code>handlers</code></span>، تنها یک هندلر از نوع <span dir="ltr"><code>StreamHandler</code></span> تعریف شده که پیام‌های لاگ را به خروجی استاندارد (کنسول) ارسال می‌کند. این تنظیم ساده اما مؤثر برای محیط‌های توسعه و تست بسیار مناسب است. در بخش <span dir="ltr"><code>loggers</code></span>، دو لاگر مجزا پیکربندی شده‌اند: لاگر <span dir="ltr"><code>django</code></span> با سطح <span dir="ltr"><code>INFO</code></span> که پیام‌های عمومی فریمورک را ثبت می‌کند، و لاگر اختصاصی اپلیکیشن (<span dir="ltr"><code>shop</code></span>) با سطح <span dir="ltr"><code>DEBUG</code></span> که تمام پیام‌های ریز و درشت مربوط به اپلیکیشن را ضبط می‌نماید.
</p>

<p dir="rtl" align="justify">
مهم‌ترین نکته در این پیکربندی، مقدار <span dir="ltr"><code>propagate: True</code></span> برای لاگر <span dir="ltr"><code>shop</code></span> است که باعث می‌شود پیام‌های لاگ علاوه بر پردازش توسط این لاگر، به لاگرهای والد در سلسله مراتب لاگینگ نیز ارسال شوند. این ویژگی انعطاف‌پذیری بالایی در مدیریت متمرکز پیام‌های سیستم ایجاد می‌کند و برای محیط‌های پیچیده که نیاز به مدیریت لاگ در سطوح مختلف دارند، ضروری است.
</p>

# test 2:

## <p dir="rtl" align="justify">متد setUp</p>

```python
def setUp(self):
    self.client = Client()
    
    # Create test products
    self.product1 = Product.objects.create(name="Product 1", price=900, is_available=True)
    self.product2 = Product.objects.create(name="Product 2", price=1000, is_available=True)
    self.product3 = Product.objects.create(name="Product 3", price=1100, is_available=False)
    self.product4 = Product.objects.create(name="Product 4", price=1000, is_available=False)
    self.product5 = Product.objects.create(name="Product 5", price=800, is_available=True)
```

<p dir="rtl" align="justify">
این متد با ایجاد داده‌های تستی پایه، شرایط یکسانی برای تمام تست‌ها فراهم می‌کند تا نتایج تست‌ها قابل اعتماد و مستقل از یکدیگر باشند. در این متد:
</p>

<p dir="rtl" align="justify">
1. کلاینت تست ایجاد می‌شود:<br>
شیء <span dir="ltr"><code>self.client</code></span> از کلاس <span dir="ltr"><code>Client</code></span> ساخته می‌شود که امکان شبیه‌سازی درخواست‌های HTTP به viewها را فراهم می‌کند. این کلاینت برای تست endpointها و بررسی پاسخ‌های دریافتی استفاده می‌شود.
</p>

<p dir="rtl" align="justify">
2. داده‌های تستی اولیه ساخته می‌شوند:<br>
پنج محصول (<span dir="ltr"><code>Product</code></span>) با ویژگی‌های متفاوت در دیتابیس تست ایجاد می‌شوند تا سناریوهای مختلف را پوشش دهند.
</p>

## test_method1_excludes_price_1000

```python
def test_method1_excludes_price_1000(self):
    response = self.client.get('/')
    method1_results = response.context['method1']
    
    self.assertEqual(method1_results.count(), 3)
    self.assertFalse(method1_results.filter(price=1000).exists())
    
    self.assertIn(self.product1, method1_results)
    self.assertIn(self.product5, method1_results)
    self.assertNotIn(self.product2, method1_results)
    self.assertNotIn(self.product4, method1_results)
```

<p dir="rtl" align="justify">
این تست با نام <span dir="ltr"><code>test_method1_excludes_price_1000</code></span>، عملکرد متد <span dir="ltr"><code>method1</code></span> را در ویوی لیست محصولات بررسی می‌کند که قرار است محصولات با قیمت ۱۰۰۰ را از نتایج حذف نماید. در این تست، ابتدا با ارسال درخواست <span dir="ltr"><code>GET</code></span> به مسیر اصلی (<span dir="ltr"><code>'/'</code></span>)، پاسخ سرور دریافت می‌شود و نتایج فیلترشده توسط <span dir="ltr"><code>method1</code></span> از طریق <span dir="ltr"><code>response.context['method1']</code></span> استخراج می‌گردد.
</p>

<p dir="rtl" align="justify">
تست سه بخش اصلی را ارزیابی می‌کند:<br>
۱) <strong>تعداد نتایج</strong>: با توجه به اینکه از بین ۵ محصول ایجادشده در <span dir="ltr"><code>setUp</code></span>، دو محصول (<span dir="ltr"><code>product2</code></span> و <span dir="ltr"><code>product4</code></span>) قیمت ۱۰۰۰ دارند و باید حذف شوند، انتظار می‌رود تنها ۳ محصول در نتایج باقی بمانند. این موضوع با <span dir="ltr"><code>assertEqual(method1_results.count(), 3)</code></span> بررسی می‌شود.<br>
۲) <strong>عدم وجود محصولات با قیمت ۱۰۰۰</strong>: با استفاده از <span dir="ltr"><code>assertFalse(method1_results.filter(price=1000).exists())</code></span>، مطمئن می‌شویم هیچ محصولی با قیمت ۱۰۰۰ در نتایج وجود ندارد.<br>
۳) <strong>محتوای نتایج</strong>: با کمک <span dir="ltr"><code>assertIn</code></span> و <span dir="ltr"><code>assertNotIn</code></span>، حضور محصولات صحیح (<span dir="ltr"><code>product1</code></span> و <span dir="ltr"><code>product5</code></span> با قیمت‌های غیر از ۱۰۰۰) و عدم حضور محصولات نادرست (<span dir="ltr"><code>product2</code></span> و <span dir="ltr"><code>product4</code></span> با قیمت ۱۰۰۰) تأیید می‌گردد.
</p>

## test_method2_excludes_price_1000_with_q

```python
def test_method2_excludes_price_1000_with_q(self):
    response = self.client.get('/')
    method2_results = response.context['method2']
    
    self.assertEqual(method2_results.count(), 3)
    self.assertFalse(method2_results.filter(price=1000).exists())
    
    method1_results = response.context['method1']
    self.assertEqual(set(method1_results), set(method2_results))
```

<p dir="rtl" align="justify">
این تست با نام <span dir="ltr"><code>test_method2_excludes_price_1000_with_q</code></span>، عملکرد متد <span dir="ltr"><code>method2</code></span> را ارزیابی می‌کند که همانند <span dir="ltr"><code>method1</code></span> محصولات با قیمت ۱۰۰۰ را از نتایج حذف می‌نماید، اما با این تفاوت که در اینجا از <span dir="ltr"><code>Q objects</code></span> برای فیلتر کردن استفاده شده است. تست با ارسال درخواست <span dir="ltr"><code>GET</code></span> به مسیر اصلی (<span dir="ltr"><code>'/'</code></span>) آغاز می‌شود و نتایج فیلترشده توسط <span dir="ltr"><code>method2</code></span> از طریق <span dir="ltr"><code>response.context['method2']</code></span> استخراج می‌گردد.
</p>

<p dir="rtl" align="justify">
<strong>۱) تعداد نتایج:</strong><br>
با توجه به داده‌های تست (<span dir="ltr"><code>setUp</code></span>)، از ۵ محصول موجود، دو محصول (<span dir="ltr"><code>product2</code></span> و <span dir="ltr"><code>product4</code></span>) قیمت ۱۰۰۰ دارند و باید حذف شوند. بنابراین انتظار می‌رود نتایج شامل ۳ محصول باقیمانده (<span dir="ltr"><code>product1</code></span>، <span dir="ltr"><code>product3</code></span> و <span dir="ltr"><code>product5</code></span>) باشد. این موضوع با <span dir="ltr"><code>assertEqual(method2_results.count(), 3)</code></span> تأیید می‌شود.
</p>

<p dir="rtl" align="justify">
<strong>۲) عدم وجود محصولات با قیمت ۱۰۰۰:</strong><br>
با استفاده از <span dir="ltr"><code>assertFalse(method2_results.filter(price=1000).exists())</code></span>، تست اطمینان حاصل می‌کند که هیچ محصولی با قیمت ۱۰۰۰ در نتایج <span dir="ltr"><code>method2</code></span> وجود ندارد.
</p>

<p dir="rtl" align="justify">
<strong>۳) همخوانی نتایج با method1:</strong><br>
از آنجا که هر دو متد (<span dir="ltr"><code>method1</code></span> و <span dir="ltr"><code>method2</code></span>) هدف یکسانی دارند (حذف محصولات با قیمت ۱۰۰۰)، تست با مقایسه مجموعه نتایج آن‌ها (<span dir="ltr"><code>set(method1_results) == set(method2_results)</code></span>) بررسی می‌کند که آیا خروجی‌های آن‌ها کاملاً یکسان است یا خیر. این مقایسه تضمین می‌کند که استفاده از <span dir="ltr"><code>Q objects</code></span> (در <span dir="ltr"><code>method2</code></span>) و <span dir="ltr"><code>exclude()</code></span> (در <span dir="ltr"><code>method1</code></span>) به نتایج مشابهی منجر می‌شود.
</p>

## test_method3_gets_only_price_1000

```python
def test_method3_gets_only_price_1000(self):
    response = self.client.get('/')
    method3_results = response.context['method3']
    
    self.assertEqual(method3_results.count(), 2)
    self.assertTrue(all(p.price == 1000 for p in method3_results))
    
    expected_products = {self.product2, self.product4}
    self.assertEqual(set(method3_results), expected_products)
```

<p dir="rtl" align="justify">
این تست با نام <span dir="ltr"><code>test_method3_gets_only_price_1000</code></span>، عملکرد متد <span dir="ltr"><code>method3</code></span> را ارزیابی میکند که قرار است فقط محصولات با قیمت دقیقاً ۱۰۰۰ را از بین لیست محصولات موجود فیلتر و بازگرداند. تست با ارسال یک درخواست <span dir="ltr"><code>GET</code></span> به مسیر اصلی (<span dir="ltr"><code>'/'</code></span>) آغاز میشود و نتایج فیلترشده توسط <span dir="ltr"><code>method3</code></span> از طریق <span dir="ltr"><code>response.context['method3']</code></span> استخراج میگردد.
</p>

<p dir="rtl" align="justify">
<strong>۱) تعداد نتایج:</strong><br>
با توجه به داده‌های تست (<span dir="ltr"><code>setUp</code></span>)، تنها دو محصول (<span dir="ltr"><code>product2</code></span> و <span dir="ltr"><code>product4</code></span>) دارای قیمت ۱۰۰۰ هستند. بنابراین، تست با استفاده از <span dir="ltr"><code>assertEqual(method3_results.count(), 2)</code></span> تأیید میکند که دقیقاً دو محصول در نتایج وجود دارد.
</p>

<p dir="rtl" align="justify">
<strong>۲) شرط قیمت محصولات:</strong><br>
با کمک <span dir="ltr"><code>assertTrue(all(p.price == 1000 for p in method3_results))</code></span>، تست اطمینان حاصل میکند که همه محصولات بازگشتی دارای قیمت ۱۰۰۰ هستند. این بخش از تست بررسی میکند که منطق فیلتر کردن به اشتباه محصولات با قیمت‌های دیگر را شامل نشده است.
</p>

<p dir="rtl" align="justify">
<strong>۳) مقایسه با انتظارات:</strong><br>
تست یک مجموعه <span dir="ltr"><code>expected_products</code></span> شامل <span dir="ltr"><code>product2</code></span> و <span dir="ltr"><code>product4</code></span> (تنها محصولات با قیمت ۱۰۰۰) تعریف میکند و با تبدیل نتایج <span dir="ltr"><code>method3</code></span> به مجموعه (<span dir="ltr"><code>set</code></span>)، آن را با مجموعه مورد انتظار مقایسه میکند (<span dir="ltr"><code>assertEqual(set(method3_results), expected_products)</code></span>). این مقایسه تضمین میکند که نتایج دقیقاً شامل همان دو محصول مورد انتظار هستند و هیچ محصول اضافه یا کمتری بازنگردانده شده است.
</p>

## test_combined_filters_available_and_excludes_price_1000

```python
def test_combined_filters_available_and_excludes_price_1000(self):
    response = self.client.get('/')
    combined_results = response.context['combined']
    
    self.assertEqual(combined_results.count(), 2)
    
    self.assertIn(self.product1, combined_results)
    self.assertIn(self.product5, combined_results)
    self.assertNotIn(self.product2, combined_results)
    self.assertNotIn(self.product3, combined_results)
    self.assertNotIn(self.product4, combined_results)
    
    self.assertTrue(all(p.is_available for p in combined_results))
    self.assertTrue(all(p.price != 1000 for p in combined_results))
```

<p dir="rtl" align="justify">
این تست عملکرد فیلتر ترکیبی را در سیستم مورد بررسی قرار می‌دهد. تست با ارسال درخواست <span dir="ltr"><code>GET</code></span> به صفحه اصلی شروع می‌شود و نتایج فیلتر شده را از <span dir="ltr"><code>context</code></span> دریافت می‌کند. فیلتر ترکیبی دو شرط اصلی دارد: محصول باید موجود باشد (<span dir="ltr"><code>is_available=True</code></span>) و قیمت آن نباید برابر با 1000 باشد (<span dir="ltr"><code>price!=1000</code></span>).
</p>

<p dir="rtl" align="justify">
بررسی‌های انجام شده در این تست شامل چند بخش کلیدی است. ابتدا تعداد نتایج فیلتر شده بررسی می‌شود که باید دقیقاً برابر با <span dir="ltr"><code>2</code></span> باشد. سپس وجود محصولات صحیح (<span dir="ltr"><code>product1</code></span> و <span dir="ltr"><code>product5</code></span>) و عدم وجود محصولات نادرست (<span dir="ltr"><code>product2</code></span>, <span dir="ltr"><code>product3</code></span> و <span dir="ltr"><code>product4</code></span>) در نتایج تأیید می‌گردد. در نهایت، تست اطمینان حاصل می‌کند که تمام محصولات موجود در نتایج، هر دو شرط فیلتر (<span dir="ltr"><code>is_available=True</code></span> و <span dir="ltr"><code>price!=1000</code></span>) را دارا هستند.
</p>

## test_template_used

```python
def test_template_used(self):
    response = self.client.get('/')
    self.assertTemplateUsed(response, 'list_view.html')
```

<p dir="rtl" align="justify">
این تست یک بررسی حیاتی برای اطمینان از صحت معماری نرم‌افزار انجام می‌دهد. با اجرای یک درخواست ساده <span dir="ltr"><code>GET</code></span> به صفحه اصلی، تست تأیید می‌کند که ویوی مربوطه از تمپلیت پیش‌بینی شده یعنی <span dir="ltr"><code>'list_view.html'</code></span> برای نمایش محتوا استفاده می‌کند. این بررسی ظاهراً ساده، در واقع چندین جنبه مهم را پوشش می‌دهد:
</p>

<p dir="rtl" align="justify">
<strong>صحت مسیردهی (Routing):</strong> تأیید می‌کند که <span dir="ltr"><code>URL</code></span> اصلی به ویوی صحیح متصل شده است. این بخش اطمینان حاصل می‌کند که درخواست‌های کاربران به مقصد درستی هدایت می‌شوند.
</p>

<p dir="rtl" align="justify">
<strong>یکپارچگی معماری:</strong> اطمینان حاصل می‌کند که الگوی طراحی <span dir="ltr"><code>MVT</code></span> (Model-View-Template) به درستی رعایت شده است. این تست نشان می‌دهد که ارتباط بین مدل‌ها، ویوها و تمپلیت‌ها به شکل صحیح برقرار است.
</p>

<p dir="rtl" align="justify">
<strong>پیشگیری از خطاهای نمایش:</strong> از نمایش نادرست داده‌ها به دلیل استفاده از تمپلیت اشتباه جلوگیری می‌کند. این بخش تضمین می‌کند که کاربران نهایی، اطلاعات را در قالب طراحی شده و مورد انتظار دریافت خواهند کرد.
</p>

## test_method1_and_method2_consistency

```python
def test_method1_and_method2_consistency(self):
    response = self.client.get('/')
    method1 = set(response.context['method1'])
    method2 = set(response.context['method2'])
    self.assertEqual(method1, method2)
    
    combined = set(response.context['combined'])
    self.assertTrue(combined.issubset(method1))
```

<p dir="rtl" align="justify">
این تست دو نکته کلیدی را در سیستم مورد بررسی قرار می‌دهد. ابتدا بررسی می‌کند که دو متد مختلف فیلتر کردن (<span dir="ltr"><code>method1</code></span> و <span dir="ltr"><code>method2</code></span>) که با روش‌های متفاوتی پیاده‌سازی شده‌اند، نتایج یکسانی تولید می‌کنند. این مقایسه با تبدیل نتایج به مجموعه (<span dir="ltr"><code>set</code></span>) و استفاده از <span dir="ltr"><code>assertEqual</code></span> انجام می‌شود که تضمین می‌کند هر دو متد دقیقاً همان محصولات را بازمی‌گردانند، صرف نظر از تفاوت‌های پیاده‌سازی.
</p>

<p dir="rtl" align="justify">
نکته دوم تست، بررسی رابطه بین نتایج فیلتر ترکیبی (<span dir="ltr"><code>combined</code></span>) و نتایج <span dir="ltr"><code>method1</code></span> است. با استفاده از <span dir="ltr"><code>issubset</code></span>، تست تأیید می‌کند که تمام محصولاتی که توسط فیلتر ترکیبی برگردانده می‌شوند، در نتایج <span dir="ltr"><code>method1</code></span> نیز وجود دارند. این بررسی اهمیت ویژه‌ای دارد زیرا:
</p>

<p dir="rtl" align="justify">
<strong>صحت فیلترهای ترکیبی</strong> را تأیید می‌کند<br>
اطمینان حاصل می‌کند که <strong>فیلترهای ساده‌تر</strong> (مثل <span dir="ltr"><code>method1</code></span>) تمام داده‌های مورد نیاز برای فیلترهای پیچیده‌تر را شامل می‌شوند<br>
<strong>یکپارچگی منطق فیلترها</strong> در سطوح مختلف را تضمین می‌نماید
</p>

## what is issubset:

<p dir="rtl" align="justify">issubset در پایتون یک متد برای بررسی رابطه زیرمجموعه‌ای بین دو مجموعه (set) است. </p>

```python
set1 = {1, 2, 3}
set2 = {1, 2}
print(set2.issubset(set1))  # True 
``` 
</details>


### git commit:
```
git status
git add .
git commit -m "Add Product model, fixtures, list view and tests" 
```
```
git checkout develop
git merge feature/shop-app
```
```
git branch -d feature/shop-app
```
