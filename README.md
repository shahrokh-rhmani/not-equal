# <p dir="rtl" align="justify">پروژه نمایش فیلترهای NOT EQUAL در Django:</p>

این پروژه بر اساس سوال <span dir="ltr"><code>[StackOverflow](https://stackoverflow.com/questions/687295/how-do-i-do-a-not-equal-in-django-queryset-filtering)</code></span> درباره نحوه انجام فیلتر "not equal" در Django QuerySet ایجاد شده است.

# <p dir="rtl" align="justify">توضیحات پروژه:</p>

<p dir="rtl" align="justify">
این پروژه یک اپلیکیشن ساده فروشگاه (<span dir="ltr"><code>shop</code></span>) ایجاد می‌کند که روش‌های مختلف فیلتر کردن محصولاتی که قیمت آنها برابر با <span dir="ltr"><code>1000</code></span> نیست را نمایش می‌دهد.
</p>

<p dir="rtl" align="justify">روش های پیاده سازی شده:</p>

<p dir="rtl" align="justify">1. استفاده از <span dir="ltr"><code>exclude()</code></span>:</p>

```python
Product.objects.exclude(price=1000)
```

<p dir="rtl" align="justify">  
2. استفاده از <span dir="ltr"><code>Q objects</code></span> با <span dir="ltr"><code>~</code></span>:
</p>


```python
Product.objects.filter(~Q(price=1000))
```

<p dir="rtl" align="justify">3. استفاده از دو <span dir="ltr"><code>exclude</code></span> برای محدوده قیمت:</p>

```python
Product.objects.exclude(price__lt=1000).exclude(price__gt=1000)
```

<p dir="rtl" align="justify">4. ترکیب فیلترها:</p>

```python
Product.objects.filter(is_available=True).exclude(price=1000)
```


# <p dir="rtl" align="justify">نحوه اجرا:</p>

### 1. Create a virtual environment in project root not src/ (windows)
```
python -m venv venv
.\venv\Scripts\activate
```
### or
### Create a virtual environment in project root not src/ (linux)
```
python3 -m venv venv
source venv/bin/activate
```

### 2. Installing Requirements:
```
pip install -r requirements.txt
```

### 3. Running Migrations:
```
cd src/
```
```
python manage.py migrate
```
```
python manage.py createsuperuser
```

### 4. Fixtures:
tip: Tip: Copy product images from `not-equal/doc/01-img/` to `media/products/`
```
mkdir -p media/products
```

Loading Fixtures:
```
python manage.py loaddata products
```

### 5. Running the Server:
```
python manage.py runserver
```

### 6. Running Tests:
```
python manage.py test
```

