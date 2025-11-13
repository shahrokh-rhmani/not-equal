<p dir="rtl" align="justify">مراحل پیاده‌سازی یک <span dir="ltr"><code>list-view</code></span> برای محصولات با ایجاد یک <span dir="ltr"><code>branch</code></span> جدید به نام <span dir="ltr"><code>feature/list-view</code></span>. در فایل <span dir="ltr"><code>views.py</code></span>، فیلترهای مختلفی مانند <span dir="ltr"><code>search</code></span>، <span dir="ltr"><code>min_price</code></span>، <span dir="ltr"><code>max_price</code></span> و <span dir="ltr"><code>availability</code></span> برای محصولات اضافه خواهد شد.</p>

<p dir="rtl" align="justify">سپس، چندین فایل <span dir="ltr"><code>template</code></span> و <span dir="ltr"><code>static</code></span> ایجاد می شود تا ظاهر صفحه را شکل دهند. این شامل یک <span dir="ltr"><code>filter-card</code></span> با قابلیت <span dir="ltr"><code>collapse</code></span> است که کاربر می‌تواند فیلترهای قیمت، وضعیت موجودی و جستجو را اعمال کند. همچنین، یک <span dir="ltr"><code>price-range-slider</code></span> با استفاده از کتابخانه <span dir="ltr"><code>noUiSlider</code></span> اضافه می شود تا کاربر بتواند محدوده قیمت را با کشیدن اسلایدر انتخاب کند.</p>

<p dir="rtl" align="justify">در مرحله نهایی، یک <span dir="ltr"><code>ProductFilterForm</code></span> تعریف می شود تا فرآیند <span dir="ltr"><code>validation</code></span> و مدیریت فیلدهای فرم را ساده‌تر کند. در پایان، تمام تغییرات به <span dir="ltr"><code>develop</code></span> <span dir="ltr"><code>merge</code></span> خواهد شد و <span dir="ltr"><code>branch</code></span> مربوطه حذف می گردد.</p>




# 1.

git branch
```
source venv/bin/activate
```
```
git checkout -b feature/list-view
```
```
cd src
```


# 2.

src/shop/views.py
```python
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
```
<details>

<summary>explanation code: (src/shop/views.py)</summary>

## <p dir="rtl" align="justify">دریافت پارامترهای فیلتر از URL</p>

```python
    search_query = request.GET.get('search', '')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    availability = request.GET.get('availability')
```

<p dir="rtl" align="justify">
در این بخش از کد، پارامترهای مختلفی از <span dir="ltr"><code>URL</code></span> دریافت می‌شوند که به عنوان معیارهای فیلتر برای نمایش محصولات استفاده خواهند شد. این پارامترها از طریق متد <span dir="ltr"><code>GET</code></span> در <span dir="ltr"><code>URL</code></span> ارسال شده‌اند و با استفاده از <span dir="ltr"><code>request.GET.get()</code></span> قابل دسترسی هستند.
</p>

<p dir="rtl" align="justify">
پارامتر اول <span dir="ltr"><code>search</code></span> است که برای جستجوی محصولات بر اساس نام آنها به کار می‌رود. اگر کاربر عبارتی را در فیلد جستجو وارد کند، این مقدار در پارامتر <span dir="ltr"><code>search</code></span> ذخیره می‌شود. مقدار پیش‌فرض برای این پارامتر یک رشته خالی (<span dir="ltr"><code>''</code></span>) در نظر گرفته شده است تا در صورت عدم ارسال این پارامتر، خطایی رخ ندهد.
</p>

<p dir="rtl" align="justify">
دو پارامتر بعدی <span dir="ltr"><code>min_price</code></span> و <span dir="ltr"><code>max_price</code></span> مربوط به محدوده قیمت محصولات هستند. این پارامترها به ترتیب حداقل و حداکثر قیمت مورد نظر کاربر برای فیلتر کردن محصولات را مشخص می‌کنند. این مقادیر می‌توانند به صورت اعداد اعشاری یا صحیح ارسال شوند.
</p>

<p dir="rtl" align="justify">
پارامتر نهایی <span dir="ltr"><code>availability</code></span> وضعیت موجودی محصول را مشخص می‌کند که می‌تواند دو مقدار <span dir="ltr"><code>'available'</code></span> (برای محصولات موجود) یا <span dir="ltr"><code>'unavailable'</code></span> (برای محصولات ناموجود) داشته باشد. این پارامتر به سیستم اجازه می‌دهد تا بر اساس وضعیت انبار محصولات را فیلتر کند. تمام این پارامترها اختیاری هستند و در صورتی که کاربر آنها را مشخص نکرده باشد، مقدار <span dir="ltr"><code>None</code></span> برای آنها در نظر گرفته می‌شود.
</p>


## <p dir="rtl" align="justify">دریافت تمام محصولات</p>

```python
  products = Product.objects.all()
```

<p dir="rtl" align="justify">
در این خط از کد، تمامی محصولات موجود در پایگاه داده با استفاده از متد <span dir="ltr"><code>all()</code></span> از مدل <span dir="ltr"><code>Product</code></span> دریافت می‌شوند. این دستور یک <span dir="ltr"><code>QuerySet</code></span> شامل تمام رکوردهای جدول محصولات در دیتابیس برمی‌گرداند. در واقع، این خط پایه و اساس کار را تشکیل می‌دهد و تمام محصولات بدون هیچ گونه فیلتر یا محدودیتی از دیتابیس فراخوانی می‌شوند.
</p>

<p dir="rtl" align="justify">
در مراحل بعدی و با توجه به پارامترهای دریافتی از کاربر (مانند جستجو، محدوده قیمت و وضعیت موجودی)، این <span dir="ltr"><code>QuerySet</code></span> اولیه فیلتر شده و محدود می‌شود تا فقط محصولات مطابق با معیارهای کاربر نمایش داده شوند. استفاده از این روش (دریافت تمام داده‌ها در ابتدا و سپس اعمال فیلترها) یک الگوی رایج در جنگو محسوب می‌شود که هم از نظر عملکرد بهینه است و هم انعطاف‌پذیری لازم برای اعمال شرایط مختلف فیلتر را فراهم می‌کند.
</p>

<p dir="rtl" align="justify">
نکته مهم این است که در این مرحله هنوز هیچ کوئری به دیتابیس ارسال نشده است، چرا که <span dir="ltr"><code>QuerySet</code></span>های جنگو به صورت تنبل (<span dir="ltr"><code>lazy</code></span>) ارزیابی می‌شوند و تنها زمانی که واقعاً به داده‌ها نیاز باشد (مثلاً هنگام رندر کردن تمپلیت یا فراخوانی متدهای خاص)، کوئری به دیتابیس ارسال خواهد شد. این ویژگی به بهینه‌سازی عملکرد برنامه کمک شایانی می‌کند.
</p>

## <p dir="rtl" align="justify">ایجاد فیلترها با Q objects</p>

```python
    filters = Q()
```

<p dir="rtl" align="justify">
در این خط از کد، یک شیء <span dir="ltr"><code>Q</code></span> خالی ایجاد می‌شود که نقش اصلی را در ساخت شرط‌های پویا و ترکیبی برای فیلتر کردن محصولات ایفا می‌کند. شیء <span dir="ltr"><code>Q</code></span> در جنگو یک ابزار قدرتمند برای ساخت کوئری‌های پیچیده است که امکان ترکیب چندین شرط با استفاده از عملگرهای منطقی مانند AND (<span dir="ltr"><code>&</code></span>) و OR (<span dir="ltr"><code>|</code></span>) را فراهم می‌آورد.
</p>

<p dir="rtl" align="justify">
با ایجاد این شیء خالی، در واقع یک بوم نقاشی آماده می‌کنیم که در مراحل بعدی و بر اساس پارامترهای دریافتی از کاربر، شرط‌های مختلف به آن اضافه خواهد شد. این رویکرد بسیار انعطاف‌پذیر است زیرا به ما اجازه می‌دهد به صورت پویا و فقط برای پارامترهایی که کاربر مشخص کرده است، شرط‌های فیلتر را ایجاد کنیم. به عبارت دیگر، اگر کاربر برخی از فیلترها را اعمال نکرده باشد، شرط مربوط به آن فیلتر نیز به این شیء اضافه نخواهد شد.
</p>

<p dir="rtl" align="justify">
خاصیت مهم این روش این است که تمام شرط‌ها در نهایت با هم ترکیب شده و به صورت یکپارچه به کوئری اصلی اضافه می‌شوند، که منجر به تولید یک کوئری بهینه و کارآمد برای دیتابیس می‌گردد. این شیوه از نوشتن کد، هم خوانایی بالایی دارد و هم از نظر عملکرد بسیار کارآمد است.
</p>

## <p dir="rtl" align="justify">اعمال فیلتر جستجو</p>

```python
    if search_query:
        filters &= Q(name__icontains=search_query)
```

<p dir="rtl" align="justify">
در این بخش از کد، شرطی برای اعمال فیلتر جستجو بر اساس نام محصولات بررسی می‌شود. اگر کاربر عبارتی را در فیلد جستجو وارد کرده باشد (یعنی پارامتر <span dir="ltr"><code>search</code></span> در <span dir="ltr"><code>URL</code></span> وجود داشته باشد و خالی نباشد)، یک شرط جدید به فیلترهای موجود اضافه می‌شود. 
</p>

<p dir="rtl" align="justify">
شرط ایجاد شده با استفاده از <span dir="ltr"><code>Q(name__icontains=search_query)</code></span> بیان می‌کند که نام محصول باید شامل عبارت جستجو شده باشد. نکته کلیدی در اینجا استفاده از <span dir="ltr"><code>icontains</code></span> است که دو ویژگی مهم دارد: اولاً به بزرگی و کوچکی حروف حساس نیست (case-insensitive)، یعنی جستجوی عبارت "laptop" و "Laptop" نتایج یکسانی خواهد داشت. ثانیاً این عملگر بررسی می‌کند که عبارت جستجو به صورت بخشی از نام محصول وجود داشته باشد، نه necessarily به عنوان کل نام محصول.
</p>

<p dir="rtl" align="justify">
عملگر <span dir="ltr"><code>&=</code></span> که برای ترکیب این شرط با فیلترهای موجود استفاده شده است، به این معنی است که این شرط جدید باید به صورت <span dir="ltr"><code>AND</code></span> با سایر شرط‌هایی که قبلاً اضافه شده‌اند ترکیب شود. این رویکرد باعث می‌شود نتایج جستجو دقیقاً مطابق با تمام معیارهای تعیین شده توسط کاربر فیلتر شوند. به عبارت دیگر، فقط محصولاتی نمایش داده خواهند شد که هم نامشان شامل عبارت جستجو باشد و هم سایر شرایط فیلتر (مانند محدوده قیمت و وضعیت موجودی) را دارا باشند.
</p>

## <p dir="rtl" align="justify">اعمال فیلتر حداقل قیمت</p>

```python
    if min_price:
        filters &= Q(price__gte=min_price)
```

<p dir="rtl" align="justify">
در این بخش از کد، سیستم بررسی می‌کند آیا کاربر حداقل قیمت (<span dir="ltr"><code>min_price</code></span>) را برای فیلتر کردن محصولات مشخص کرده است یا خیر. اگر این پارامتر وجود داشته باشد، یک شرط جدید به فیلترهای موجود اضافه می‌شود که فقط محصولاتی را نمایش دهد که قیمت آنها بزرگتر یا مساوی مقدار تعیین شده توسط کاربر است.
</p>

<p dir="rtl" align="justify">
عملکرد این بخش به این صورت است:
<br>
- ابتدا بررسی می‌شود آیا پارامتر <span dir="ltr"><code>min_price</code></span> در درخواست کاربر وجود دارد (<span dir="ltr"><code>if min_price:</code></span>)
<br>
- در صورت وجود، از عملگر <span dir="ltr"><code>&=</code></span> برای ترکیب این شرط جدید با فیلترهای قبلی استفاده می‌شود
<br>
- <span dir="ltr"><code>gte</code></span> که مخفف <span dir="ltr"><code>"greater than or equal"</code></span> است به معنای "بزرگتر یا مساوی" می‌باشد.
<br>    
- شرط قیمت با استفاده از <span dir="ltr"><code>Q(price__gte=min_price)</code></span> ایجاد می‌شود:
</p>

<p dir="rtl" align="justify">
این فیلتر به صورت هوشمندانه فقط زمانی اعمال می‌شود که کاربر واقعاً مقدار <span dir="ltr"><code>min_price</code></span> را مشخص کرده باشد. اگر کاربر این فیلتر را اعمال نکرده باشد، این بخش از کد هیچ تاثیری در نتایج نخواهد داشت. همچنین، با استفاده از عملگر <span dir="ltr"><code>&=</code></span>، این شرط به صورت <span dir="ltr"><code>AND</code></span> با سایر فیلترهای موجود (مانند جستجو، حداکثر قیمت و وضعیت موجودی) ترکیب می‌شود تا نتایج دقیقاً مطابق با تمام معیارهای کاربر نمایش داده شوند.
</p>

## <p dir="rtl" align="justify">اعمال فیلتر حداکثر قیمت</p>

```python
    if max_price:
        filters &= Q(price__lte=max_price)
```

<p dir="rtl" align="justify">
ابتدا بررسی می‌شود آیا پارامتر <span dir="ltr"><code>max_price</code></span> در درخواست کاربر وجود دارد یا خیر. اگر کاربر این فیلتر را مشخص نکرده باشد، این بخش از کد کاملاً نادیده گرفته می‌شود.
</p>

<p dir="rtl" align="justify">
در صورت وجود مقدار <span dir="ltr"><code>max_price</code></span>، یک شرط جدید به فیلترهای موجود اضافه می‌شود که با استفاده از عملگر <span dir="ltr"><code>&=</code></span> به صورت <span dir="ltr"><code>AND</code></span> با سایر فیلترها ترکیب می‌شود.
</p>

<p dir="rtl" align="justify">
شرط ایجاد شده <span dir="ltr"><code>Q(price__lte=max_price)</code></span> از سه بخش تشکیل شده:
<br>
- <span dir="ltr"><code>price</code></span>: اشاره به فیلد قیمت در مدل <span dir="ltr"><code>Product</code></span> دارد
<br>
- <span dir="ltr"><code>lte</code></span>: که مخفف "less than or equal" به معنای "کمتر یا مساوی" است
<br>
- <span dir="ltr"><code>max_price</code></span>: مقدار دریافتی از کاربر که به عنوان سقف قیمت تعیین شده
</p>

<p dir="rtl" align="justify">
نکته مهم این است که این فیلتر به صورت پویا فقط زمانی اعمال می‌شود که کاربر واقعاً مقدار <span dir="ltr"><code>max_price</code></span> را مشخص کرده باشد. این رویکرد انعطاف‌پذیری بالایی ایجاد می‌کند و به کاربران اجازه می‌دهد فقط فیلترهای مورد نیاز خود را اعمال کنند. همچنین ترکیب این فیلتر با سایر فیلترها (مانند حداقل قیمت، جستجو و وضعیت موجودی) باعث می‌شود نتایج نمایش داده شده دقیقاً مطابق با تمام معیارهای درخواستی کاربر باشند.
</p>

## <p dir="rtl" align="justify">اعمال فیلتر وضعیت موجودی</p>

```python
    if availability == 'available':
        filters &= Q(is_available=True)
    elif availability == 'unavailable':
        filters &= Q(is_available=False)
```

<p dir="rtl" align="justify">
در این بخش از کد، فیلتر کردن محصولات بر اساس وضعیت موجودی آنها با استفاده از پارامتر <span dir="ltr"><code>availability</code></span> انجام می‌شود. این کد به صورت هوشمندانه و انعطاف‌پذیر عمل می‌کند:
</p>

<p dir="rtl" align="justify">
سیستم ابتدا مقدار پارامتر <span dir="ltr"><code>availability</code></span> را بررسی می‌کند که می‌تواند یکی از سه حالت زیر باشد:
<br>
- رشته <span dir="ltr"><code>'available'</code></span> (برای محصولات موجود)
<br>
- رشته <span dir="ltr"><code>'unavailable'</code></span> (برای محصولات ناموجود)
<br>
- مقدار <span dir="ltr"><code>None</code></span> (وقتی کاربر هیچ انتخابی نکرده باشد)
</p>

<p dir="rtl" align="justify">
رفتار سیستم در هر حالت:
<br>
اگر <span dir="ltr"><code>availability == 'available'</code></span>:
<br>
- شرط <span dir="ltr"><code>Q(is_available=True)</code></span> به فیلترها اضافه می‌شود
<br>
- فقط محصولات با وضعیت "موجود" نمایش داده می‌شوند
<br><br>
اگر <span dir="ltr"><code>availability == 'unavailable'</code></span>:
<br>
- شرط <span dir="ltr"><code>Q(is_available=False)</code></span> به فیلترها اضافه می‌شود
<br>
- فقط محصولات با وضعیت "ناموجود" نمایش داده می‌شوند
</p>

<p dir="rtl" align="justify">
حالت خاص - وقتی <span dir="ltr"><code>availability</code></span> برابر <span dir="ltr"><code>None</code></span> است:
<br>
- این حالت زمانی رخ می‌دهد که کاربر اصلاً پارامتر <span dir="ltr"><code>availability</code></span> را ارسال نکرده باشد یا مقدار نامعتبری ارسال کرده باشد
<br>
- در این حالت هیچ شرطی به فیلترها اضافه نمی‌شود
<br>
- وضعیت موجودی در فیلترها تاثیری ندارد
<br>
- تمام محصولات بدون توجه به وضعیت موجودی نمایش داده می‌شوند
</p>


## <p dir="rtl" align="justify">اعمال فیلترها روی محصولات</p>

```python
    products = products.filter(filters)
```

<p dir="rtl" align="justify">
در این خط کد، تمام فیلترهایی که تا این مرحله به صورت پویا و بر اساس پارامترهای دریافتی از کاربر ساخته شده‌اند، بر روی مجموعه اولیه محصولات اعمال می‌شوند. این مرحله، نقطه اوج و نتیجه‌گیری تمام مراحل فیلترسازی است که به صورت هوشمندانه و بهینه انجام می‌شود.
</p>

<p dir="rtl" align="justify">
مجموعه اولیه محصولات (که با <span dir="ltr"><code>Product.objects.all()</code></span> دریافت شده بود) اکنون با متد <span dir="ltr"><code>filter()</code></span> و با استفاده از شیء <span dir="ltr"><code>filters</code></span> که حاوی تمام شرایط است، فیلتر می‌شود.
</p>

<p dir="rtl" align="justify">
شیء <span dir="ltr"><code>filters</code></span> که از نوع <span dir="ltr"><code>Q</code></span> است، می‌تواند شامل ترکیبی از چندین شرط باشد:
<br>
- شرط جستجو (در صورت وجود)
<br>
- شرط حداقل قیمت (در صورت وجود)
<br>
- شرط حداکثر قیمت (در صورت وجود)
<br>
- شرط وضعیت موجودی (در صورت وجود)
</p>

<p dir="rtl" align="justify">
نتیجه نهایی در متغیر <span dir="ltr"><code>products</code></span> ذخیره می‌شود که:
<br>
- یک <span dir="ltr"><code>QuerySet</code></span> فیلتر شده است
<br>
- فقط شامل محصولاتی است که با تمام معیارهای کاربر مطابقت دارند
<br>
- هنوز به صورت (<span dir="ltr"><code>lazy</code></span>) ارزیابی می‌شود و تا زمان نیاز واقعی، کوئری به دیتابیس ارسال نمی‌کند، (هنگام تکرار (Iteration)،وقتی در تمپلیت از حلقه <span dir="ltr"><code>{% for product in products %}</code></span> استفاده می‌کنید)
</p>


</details>




src/static/css/main.css
```
mkdir src/static/css
touch src/static/css/main.css
# 
mkdir static/css
touch static/css/main.css
```
```css
:root {
  --primary-color: #4e73df;
  --secondary-color: #f8f9fc;
}

/* Layout Styles */
html, body {
  height: 100%;
}

body {
  font-family: Vazirmatn, sans-serif;
  background-color: var(--secondary-color);
  text-align: right !important;
  direction: rtl;
  display: flex;
  flex-direction: column;
}

main {
  flex: 1 0 auto;
  padding-bottom: 60px; /* Extra space for footer*/
}

footer {
  flex-shrink: 0;
  background-color: #343a40;
  color: white;
  padding: 1rem 0;
}

/* Navbar Styles */
.navbar-brand {
  font-weight: 600;
}

/* Card Styles */
.card {
  border-radius: 0.5rem;
  box-shadow: 0 0.15rem 0.5rem rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.card:hover {
  transform: translateY(-5px);
}

.card-header {
  background-color: var(--primary-color);
  color: white;
  border-radius: 0.5rem 0.5rem 0 0 !important;
}

/* Form Styles */
.form-control, 
.input-group-text, 
.form-select {
  direction: rtl;
}

.input-group-text {
  border-left: none;
  border-right: 1px solid #ced4da;
}

.form-control {
  border-right: none;
  border-left: 1px solid #ced4da;
}

/* Product Styles */
.product-img {
  height: 180px;
  object-fit: contain;
  padding: 10px;
}

/* Button Styles */
.filter-btn {
  width: 100%;
}

/* Empty State Styles */
.empty-state {
  text-align: center;
  padding: 2rem;
}

.empty-state i {
  font-size: 3rem;
  color: #6c757d;
}
```

src/templates/_product_filter.html
```
touch src/templates/_product_filter.html
# 
touch templates/_product_filter.html
```

_product_filter.html
```html
    <!-- Filter Card -->
    <div class="card shadow mb-4">
        <div class="card-header py-3 d-flex justify-content-between align-items-center">
            <h6 class="m-0 font-weight-bold text-white"><i class="bi bi-funnel"></i> فیلتر محصولات</h6>
            <button class="btn btn-sm btn-light" type="button" data-bs-toggle="collapse" data-bs-target="#filterCollapse">
                <i class="bi bi-chevron-down"></i>
            </button>
        </div>
        <div class="card-body collapse show" id="filterCollapse">
            <form method="get" class="row g-3">
                <div class="col-md-4">
                    <label for="search" class="form-label text-end">جستجو</label>
                    <div class="input-group">
                        <input type="text" class="form-control text-end" id="search" name="search" 
                               value="{{ search_query }}" placeholder="نام محصول...">
                        <span class="input-group-text"><i class="bi bi-search"></i></span>
                    </div>
                </div>
                <div class="col-md-2">
                    <label for="min_price" class="form-label text-end">حداقل قیمت</label>
                    <div class="input-group">
                        <input type="number" class="form-control text-end" id="min_price" name="min_price" 
                               value="{{ filters.min_price }}" placeholder="حداقل">
                        <span class="input-group-text"><i class="bi bi-currency-dollar"></i></span>
                    </div>
                </div>
                <div class="col-md-2">
                    <label for="max_price" class="form-label text-end">حداکثر قیمت</label>
                    <div class="input-group">
                        <input type="number" class="form-control text-end" id="max_price" name="max_price" 
                               value="{{ filters.max_price }}" placeholder="حداکثر">
                        <span class="input-group-text"><i class="bi bi-currency-dollar"></i></span>
                    </div>
                </div>
                <div class="col-md-2">
                    <label for="availability" class="form-label text-end">وضعیت موجودی</label>
                    <select class="form-select text-end" id="availability" name="availability">
                        <option value="">همه</option>
                        <option value="available" {% if filters.availability == 'available' %}selected{% endif %}>موجود</option>
                        <option value="unavailable" {% if filters.availability == 'unavailable' %}selected{% endif %}>ناموجود</option>
                    </select>
                </div>
                <div class="col-md-2 d-flex align-items-end">
                    <button type="submit" class="btn btn-primary filter-btn w-100">
                        <i class="bi bi-filter"></i> اعمال فیلتر
                    </button>
                </div>
            </form>
        </div>
    </div>
```

src/templates/_base.html
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
    <!-- Custom styles-->
    <link rel="stylesheet" href="{% static 'css/main.css' %}">
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
                        <a class="nav-link active" href="#"><i class="bi bi-house"></i> خانه</a>
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
</body>
</html>
```

src/shop/templates/list_view.html
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
                        <button class="btn btn-outline-primary btn-sm">
                            <i class="bi bi-eye"></i> مشاهده جزئیات
                        </button>
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
```
src/shop/models.py:
```python
    @property
    def image_url(self):
        if self.image:
            return self.image.url
        return None
```

### tip: add images.

git commit (cd .. or terminal 2)
```
cd ..
```
```
git status
git add .
git commit -m "Add advanced product filtering with search, price range, and availability"
```
```
cd src/
```

# 3. price-range

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
            <form method="get" class="row g-3">
                <!-- search -->
                <div class="col-md-3">
                    <label for="search" class="form-label text-end">جستجو</label>
                    <div class="input-group">
                        <input type="text" class="form-control text-end" id="search" name="search"
                            value="{{ search_query }}" placeholder="نام محصول...">
                        <span class="input-group-text"><i class="bi bi-search"></i></span>
                    </div>
                </div>

                <!-- Inventory status -->
                <div class="col-md-2">
                    <label for="availability" class="form-label text-end">وضعیت موجودی</label>
                    <select class="form-select text-end" id="availability" name="availability">
                        <option value="">همه</option>
                        <option value="available" {% if filters.availability == 'available' %}selected{% endif %}>موجود
                        </option>
                        <option value="unavailable" {% if filters.availability == 'unavailable' %}selected{% endif %}>
                            ناموجود</option>
                    </select>
                </div>

                <!-- Price range -->
                <div class="col-md-4">
                    <label for="price-range" class="form-label text-end">محدوده قیمت</label>
                    <div class="d-flex justify-content-between mb-2">
                        <div class="input-group" style="width: 48%;">
                            <span class="input-group-text"><i class="bi bi-currency-dollar"></i></span>
                            <input type="number" class="form-control text-end" id="min_price" name="min_price"
                                value="{{ filters.min_price|default:0 }}" placeholder="حداقل" min="0">
                        </div>
                        <div class="input-group" style="width: 48%;">
                            <span class="input-group-text"><i class="bi bi-currency-dollar"></i></span>
                            <input type="number" class="form-control text-end" id="max_price" name="max_price"
                                value="{{ filters.max_price|default:1000000 }}" placeholder="حداکثر" min="0">
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
git diff
```

```
mkdir src/static/js
touch src/static/js/price-range-slider.js
#
mkdir static/js
touch static/js/price-range-slider.js
```

src/static/js/price-range-slider.js:
```js
document.addEventListener('DOMContentLoaded', function () {
    const priceRange = document.getElementById('price-range');
    const minPriceInput = document.getElementById('min_price');
    const maxPriceInput = document.getElementById('max_price');

    // Initialize with current values or defaults
    const minPrice = parseInt(minPriceInput.value) || 0;
    const maxPrice = parseInt(maxPriceInput.value) || 1000000;

    // Create slider
    noUiSlider.create(priceRange, {
        start: [minPrice, maxPrice],
        connect: true,
        direction: 'rtl',
        range: {
            'min': 0,
            'max': 1000000
        },
        step: 1,
        tooltips: [true, true],
        format: wNumb({
            decimals: 0,
            thousand: ',',
            suffix: ' تومان'
        })
    });

    // Update input fields when slider changes
    priceRange.noUiSlider.on('update', function (values, handle) {
        const value = values[handle];
        if (handle) {
            maxPriceInput.value = value.replace(/[^0-9]/g, '');
        } else {
            minPriceInput.value = value.replace(/[^0-9]/g, '');
        }
    });

    // Update slider when input fields change
    function updateSliderFromInputs() {
        let minValue = parseInt(minPriceInput.value) || 0;
        let maxValue = parseInt(maxPriceInput.value) || 1000000;

        // Validate values
        if (minValue < 0) minValue = 0;
        if (maxValue > 1000000) maxValue = 1000000;
        if (minValue > maxValue) {
            // If the minimum value becomes greater than the maximum, set the minimum value equal to the maximum
            minValue = maxValue;
            minPriceInput.value = minValue;
        }

        // Update slider
        priceRange.noUiSlider.set([minValue, maxValue]);
    }

    // Add event listeners for input changes
    minPriceInput.addEventListener('change', updateSliderFromInputs);
    maxPriceInput.addEventListener('change', updateSliderFromInputs);

    // Also update on input (real-time) with debounce
    let timeout;
    function debounceUpdate() {
        clearTimeout(timeout);
        timeout = setTimeout(updateSliderFromInputs, 500);
    }

    minPriceInput.addEventListener('input', debounceUpdate);
    maxPriceInput.addEventListener('input', debounceUpdate);
});
```

<details>

<summary>explanation code: (src/static/js/price-range-slider.js)</summary>

## <p dir="rtl" align="justify">1. رویداد DOMContentLoaded</p>

```js
document.addEventListener('DOMContentLoaded', function () {
```

<p dir="rtl" align="justify">
کد داخل یک رویداد <span dir="ltr"><code>DOMContentLoaded</code></span> قرار دارد که تضمین می‌کند کد فقط پس از بارگذاری کامل <span dir="ltr"><code>DOM</code></span> اجرا شود.
</p>

## <p dir="rtl" align="justify">2. انتخاب عناصر</p>

```js
const priceRange = document.getElementById('price-range');
const minPriceInput = document.getElementById('min_price');
const maxPriceInput = document.getElementById('max_price');
```

<p dir="rtl" align="justify">
در این بخش از کد، ما سه عنصر مهم از صفحه وب را انتخاب می‌کنیم که برای ایجاد و کنترل اسلایدر محدوده قیمت ضروری هستند:
</p>

<p dir="rtl" align="justify">
<strong>عنصر priceRange:</strong><br>
این خط کد <span dir="ltr"><code>const priceRange = document.getElementById('price-range')</code></span> یک عنصر <span dir="ltr"><code>div</code></span> را از صفحه انتخاب می‌کند که به عنوان ظرفیت اصلی برای نمایش اسلایدر عمل خواهد کرد. و کتابخانه <span dir="ltr"><code>noUiSlider</code></span> از این عنصر برای رندر کردن اسلایدر استفاده می‌کند.
</p>

<p dir="rtl" align="justify">
<strong>عناصر minPriceInput و maxPriceInput:</strong><br>
دو خط بعدی <span dir="ltr"><code>const minPriceInput = document.getElementById('min_price')</code></span> و <span dir="ltr"><code>const maxPriceInput = document.getElementById('max_price')</code></span> دو فیلد ورودی را از صفحه انتخاب می‌کنند که به ترتیب برای نمایش و ویرایش مقادیر حداقل و حداکثر قیمت استفاده می‌شوند.
</p>

<p dir="rtl" align="justify">
این سه عنصر به صورت هماهنگ کار می‌کنند:
<ul dir="rtl">
<li>کاربر می‌تواند هم با حرکت دادن دستگیره‌های اسلایدر درون <span dir="ltr"><code>priceRange</code></span>، مقادیر قیمت را تغییر دهد</li>
<li>و هم می‌تواند مقادیر را مستقیماً در فیلدهای <span dir="ltr"><code>minPriceInput</code></span> و <span dir="ltr"><code>maxPriceInput</code></span> وارد کند</li>
<li>تغییرات در هر یک از این عناصر به صورت خودکار به عناصر دیگر منتقل می‌شود</li>
</ul>
</p>


## <p dir="rtl" align="justify">3. مقداردهی اولیه</p>

```js
const minPrice = parseInt(minPriceInput.value) || 0;
const maxPrice = parseInt(maxPriceInput.value) || 1000000;
```

<p dir="rtl" align="justify">
این بخش از کد مسئول تعیین مقادیر اولیه برای اسلایدر محدوده قیمت است.
</p>

<p dir="rtl" align="justify">
کد با استفاده از <span dir="ltr"><code>parseInt(minPriceInput.value)</code></span> و <span dir="ltr"><code>parseInt(maxPriceInput.value)</code></span> سعی می‌کند مقادیر عددی را از فیلدهای ورودی استخراج کند. تابع <span dir="ltr"><code>parseInt</code></span> مقدار رشته‌ای فیلد را به عدد صحیح تبدیل می‌کند که برای محاسبات و تنظیمات اسلایدر ضروری است.
</p>

<p dir="rtl" align="justify">
عملگر منطقی <span dir="ltr"><code>OR (||)</code></span> در اینجا به عنوان یک fallback عمل می‌کند. اگر مقدار فیلد ورودی:
<ul dir="rtl">
<li>خالی باشد</li>
<li>شامل عدد معتبر نباشد</li>
<li>یا نتیجه <span dir="ltr"><code>parseInt</code></span> برابر <span dir="ltr"><code>NaN</code></span> شود</li>
</ul>
<p dir="rtl" align="justify">در این صورت مقدار پس از عملگر <span dir="ltr"><code>OR</code></span> استفاده می‌شود:</p>


<ul dir="rtl">
<li>برای حداقل قیمت: <span dir="ltr"><code>0</code></span> تومان</li>
<li>برای حداکثر قیمت: <span dir="ltr"><code>1,000,000</code></span> تومان</li>
</ul>
</p>

## <p dir="rtl" align="justify">4. ایجاد اسلایدر با noUiSlider</p>

```js
noUiSlider.create(priceRange, {
    start: [minPrice, maxPrice],
    connect: true, 
    direction: 'rtl', 
    range: {
        'min': 0, 
        'max': 1000000  
    },
    step: 1, // 
    tooltips: [true, true], 
    format: wNumb({ 
        decimals: 0, 
        thousand: ',', 
        suffix: 'تومان' 
    })
});
```

<p dir="rtl" align="justify">
این بخش از کد، هسته اصلی عملکرد اسلایدر محدوده قیمت را تشکیل می‌دهد. در اینجا با استفاده از تابع <span dir="ltr"><code>noUiSlider.create</code></span>، یک اسلایدر حرفه‌ای و قابل تنظیم ایجاد می‌شود که دارای ویژگی‌های زیر است:
</p>

<p dir="rtl" align="justify">
<strong>تنظیمات اولیه و مقداردهی:</strong><br>
اسلایدر با پارامتر <span dir="ltr"><code>start</code></span> مقداردهی می‌شود که آرایه‌ای از دو مقدار حداقل و حداکثر قیمت را دریافت می‌کند. این مقادیر از بخش قبلی کد که فیلدهای ورودی را بررسی می‌کرد، به دست آمده‌اند.
</p>

<p dir="rtl" align="justify">
<strong>ویژگی‌های ظاهری و عملکردی:</strong>
<ul dir="rtl">
<li><span dir="ltr"><code>connect: true</code></span>: یک نوار رنگی بین دو دستگیره ایجاد می‌کند</li>
<li><span dir="ltr"><code>direction: 'rtl'</code></span>: اسلایدر را از راست به چپ تنظیم می‌کند</li>
<li><span dir="ltr"><code>range</code></span>: محدوده 0 تا 1,000,000 تومان را تعیین می‌کند</li>
<li><span dir="ltr"><code>step: 1</code></span>: اسلایدر با گام‌های 1 واحدی تغییر می‌کند</li>
</ul>
</p>

<p dir="rtl" align="justify">
<strong>نمایش اطلاعات:</strong>
<ul dir="rtl">
<li><span dir="ltr"><code>tooltips: [true, true]</code></span>: نمایش مقدار کنار دستگیره‌ها</li>
<li><span dir="ltr"><code>format</code></span>: با استفاده از کتابخانه <span dir="ltr"><code>wNumb</code></span> اعداد را فرمت‌بندی می‌کند:
<ul>
<li>بدون رقم اعشار (<span dir="ltr"><code>decimals: 0</code></span>)</li>
<li>جداکننده هزارگان (<span dir="ltr"><code>thousand: ','</code></span>)</li>
<li>واحد تومان (<span dir="ltr"><code>suffix: ' تومان'</code></span>)</li>
</ul>
</li>
</ul>
</p>

## <p dir="rtl" align="justify">5. به‌روزرسانی فیلدهای ورودی هنگام تغییر اسلایدر</p>

```js
priceRange.noUiSlider.on('update', function (values, handle) {
    const value = values[handle];
    if (handle) {
        maxPriceInput.value = value.replace(/[^0-9]/g, '');
    } else {
        minPriceInput.value = value.replace(/[^0-9]/g, '');
    }
});
```

<p dir="rtl" align="justify">
این بخش از کد مسئول همگام‌سازی مقادیر فیلدهای ورودی با تغییراتی است که کاربر روی اسلایدر اعمال می‌کند. 
</p>

<p dir="rtl" align="justify">
<strong>ثبت رویداد Update:</strong><br>
کد با استفاده از <span dir="ltr"><code>priceRange.noUiSlider.on('update', ...)</code></span> (listener) برای رویداد update اسلایدر تنظیم می‌کند. این رویداد در موارد زیر فعال می‌شود:
<ul dir="rtl">
<li>هنگامی که کاربر دستگیره‌های اسلایدر را جابجا می‌کند</li>
<li>وقتی مقدار اسلایدر به صورت برنامه‌ای تغییر می‌کند</li>
<li>در هنگام اولین بارگذاری اسلایدر</li>
</ul>
</p>

<p dir="rtl" align="justify">
<strong>پردازش مقادیر:</strong><br>
تابع callback دو پارامتر دریافت می‌کند:
<ul dir="rtl">
<li><span dir="ltr"><code>values</code></span>: آرایه‌ای شامل مقادیر فعلی دو دستگیره اسلایدر</li>
<li><span dir="ltr"><code>handle</code></span>: اندیسی که مشخص می‌کند کدام دستگیره تغییر کرده (0 برای دستگیره حداقل، 1 برای دستگیره حداکثر)</li>
</ul>
</p>

<p dir="rtl" align="justify">
<strong>به‌روزرسانی فیلدهای ورودی:</strong><br>
سیستم به این صورت عمل می‌کند:
<ul dir="rtl">
<li>اگر <span dir="ltr"><code>handle</code></span> برابر 1 باشد (دستگیره حداکثر قیمت)، مقدار به <span dir="ltr"><code>maxPriceInput</code></span> اختصاص می‌یابد</li>
<li>اگر <span dir="ltr"><code>handle</code></span> برابر 0 باشد (دستگیره حداقل قیمت)، مقدار به <span dir="ltr"><code>minPriceInput</code></span> اختصاص می‌یابد</li>
</ul>
</p>

<p dir="rtl" align="justify">
<strong>پاکسازی مقادیر:</strong><br>
متد <span dir="ltr"><code>replace(/[^0-9]/g, '')</code></span> تمام کاراکترهای غیرعددی را از مقدار حذف می‌کند. این کار به دلایل زیر انجام می‌شود:
<ul dir="rtl">
<li>حذف جداکننده‌های هزارگان (کاما) که در نمایش اسلایدر وجود دارند</li>
<li>حذف واحد "تومان" که در tooltip نمایش داده می‌شود</li>
<li>اطمینان از اینکه فقط اعداد خام در فیلدهای ورودی ذخیره می‌شوند</li>
</ul>
</p>

<p dir="rtl" align="justify">
این مکانیزم تضمین می‌کند که فیلدهای ورودی همیشه با موقعیت فعلی دستگیره‌های اسلایدر همگام باشند و کاربر بتواند هم از طریق اسلایدر و هم از طریق تایپ مستقیم، محدوده قیمت را تنظیم کند.
</p>

## <p dir="rtl" align="justify">6. به‌روزرسانی اسلایدر هنگام تغییر فیلدهای ورودی</p>

```js
function updateSliderFromInputs() {
    let minValue = parseInt(minPriceInput.value) || 0;
    let maxValue = parseInt(maxPriceInput.value) || 1000000;

    if (minValue < 0) minValue = 0;
    if (maxValue > 1000000) maxValue = 1000000;
    if (minValue > maxValue) {
        minValue = maxValue;
        minPriceInput.value = minValue;
    }

    priceRange.noUiSlider.set([minValue, maxValue]);
}
```

<p dir="rtl" align="justify">
این تابع، ارتباط معکوس بین فیلدهای ورودی و اسلایدر را مدیریت می‌کند و یک حلقه بازخورد کامل ایجاد می‌نماید. 
</p>

<p dir="rtl" align="justify">
<strong>مرحله اول: خواندن و پیش‌پردازش مقادیر</strong><br>
تابع ابتدا مقادیر فیلدهای ورودی را با استفاده از <span dir="ltr"><code>parseInt</code></span> به عدد تبدیل می‌کند. در این تبدیل دو سناریو پیش‌بینی شده است:
<ul dir="rtl">
<li>اگر فیلد خالی باشد یا مقدار نامعتبر داشته باشد، از مقادیر پیش‌فرض استفاده می‌شود (<span dir="ltr"><code>0</code></span> برای حداقل و <span dir="ltr"><code>1,000,000</code></span> برای حداکثر)</li>
<li>این رویکرد از خرابی سیستم در مواجهه با ورودی‌های نادرست جلوگیری می‌کند</li>
</ul>
</p>

<p dir="rtl" align="justify">
<strong>مرحله دوم: اعتبارسنجی هوشمند</strong><br>
سیستم چندین بررسی امنیتی انجام می‌دهد:
<ul dir="rtl">
<li>حداقل مجاز: اگر مقدار وارد شده کمتر از <span dir="ltr"><code>0</code></span> باشد، به طور خودکار به <span dir="ltr"><code>0</code></span> اصلاح می‌شود</li>
<li>حداکثر مجاز: مقادیر بالاتر از <span dir="ltr"><code>1,000,000</code></span> به این مقدار محدود می‌شوند</li>
<li>تناقض منطقی: اگر حداقل قیمت از حداکثر بیشتر شود، به طور خودکار با مقدار حداکثر برابر می‌شود و فیلد ورودی نیز اصلاح می‌گردد</li>
</ul>
</p>

<p dir="rtl" align="justify">
<strong>مرحله نهایی: همگام‌سازی اسلایدر</strong><br>
پس از اطمینان از معتبر بودن مقادیر، تابع از <span dir="ltr"><code>priceRange.noUiSlider.set</code></span> برای:
<ul dir="rtl">
<li>به‌روزرسانی موقعیت دستگیره‌های اسلایدر</li>
<li>تغییر نوار رنگی بین دو دستگیره</li>
<li>به‌روزرسانی <span dir="ltr"><code>tooltip</code></span>‌ها</li>
</ul>

</p>

## <p dir="rtl" align="justify">7.رویدادهای تغییر و ورود</p>

```js
minPriceInput.addEventListener('change', updateSliderFromInputs);
maxPriceInput.addEventListener('change', updateSliderFromInputs);

let timeout;
function debounceUpdate() {
    clearTimeout(timeout);
    timeout = setTimeout(updateSliderFromInputs, 500);
}

minPriceInput.addEventListener('input', debounceUpdate);
maxPriceInput.addEventListener('input', debounceUpdate);
```

<p dir="rtl" align="justify">
این بخش از کد، دو مکانیسم مختلف برای نظارت بر تغییرات در فیلدهای ورودی پیاده‌سازی کرده است که در کنار هم تجربه کاربری بهینه‌ای ایجاد می‌کنند:
</p>

<p dir="rtl" align="justify">
<strong>۱. رویداد Change برای تعاملات قطعی</strong><br>
این بخش با استفاده از <span dir="ltr"><code>addEventListener('change',...)</code></span> رویدادی را ثبت می‌کند که:
<ul dir="rtl">
<li>فقط هنگامی فعال می‌شود که کاربر پس از ویرایش فیلد، focus را از آن خارج کند</li>
<li>برای تغییرات نهایی و قطعی مناسب است</li>
<li>بلافاصله تابع <span dir="ltr"><code>updateSliderFromInputs</code></span> را فراخوانی می‌کند</li>
<li>مناسب برای مواردی که کاربر مقدار نهایی خود را وارد کرده و می‌خواهد نتیجه را ببیند</li>
</ul>
</p>

<p dir="rtl" align="justify">
<strong>۲. رویداد Input با تکنیک Debounce برای تعاملات بلادرنگ</strong><br>
این مکانیسم پیشرفته‌تر عمل می‌کند:
<ul dir="rtl">
<li>با <span dir="ltr"><code>addEventListener('input',...)</code></span> به هر تغییر حین تایپ واکنش نشان می‌دهد</li>
<li>از تکنیک <span dir="ltr"><code>debounce</code></span> با تاخیر 500 میلی‌ثانیه استفاده می‌کند</li>
</ul>
</p>

<p dir="rtl" align="justify">
<strong>مزایای این روش:</strong>
<ul dir="rtl">
<li>از عملکرد بیش از حد (over-processing) جلوگیری می‌کند</li>
<li>هنگام تایپ سریع کاربر، درخواست‌های مکرر ایجاد نمی‌کند</li>
<li>فقط پس از توقف تایپ کاربر (500ms) اسلایدر را به‌روز می‌کند</li>
<li>تعادل مناسبی بین پاسخگویی و عملکرد ایجاد می‌کند</li>
</ul>
</p>

<p dir="rtl" align="justify">
<strong>همکاری این دو مکانیسم</strong><br>
این دو روش به صورت مکمل کار می‌کنند:
<ul dir="rtl">
<li>رویداد <span dir="ltr"><code>input</code></span> برای تعاملات پویا و حین تایپ</li>
<li>رویداد <span dir="ltr"><code>change</code></span> برای ثبت نهایی مقادیر</li>
<li>تضمین می‌کنند سیستم هم به تغییرات بلادرنگ واکنش نشان دهد و هم از بار پردازشی اضافی جلوگیری کند</li>
</ul>
</p>

# <p dir="rtl" align="justify">مفهوم پایه‌ای Debounce</p>

<p dir="rtl" align="justify">
<span dir="ltr"><code>Debounce</code></span> یک تکنیک برنامه‌نویسی است که مکرر بودن اجرای یک تابع را کنترل می‌کند. این تکنیک مخصوصاً برای رویدادهایی که به سرعت و پشت سر هم اتفاق می‌افتند (مثل تایپ کردن در فیلد ورودی یا اسکرول صفحه) بسیار مفید است.
</p>

<p dir="rtl" align="justify">
<strong>نحوه کارکرد:</strong>
<ul dir="rtl">
<li>وقتی رویدادی مکرراً اتفاق می‌افتد (مثلاً کاربر در حال تایپ کردن است)</li>
<li>به جای اجرای تابع برای هر بار تغییر، یک تایمر تنظیم می‌شود</li>
<li>اگر قبل از اتمام تایمر، رویداد جدیدی اتفاق بیفتد، تایمر از اول شروع می‌شود</li>
<li>فقط وقتی تایمر کامل شود (یعنی مدتی از آخرین رویداد گذشته باشد)، تابع اصلی اجرا می‌شود</li>
</ul>
</p>

<p dir="rtl" align="justify">
این تکنیک با استفاده از <span dir="ltr"><code>setTimeout</code></span> و <span dir="ltr"><code>clearTimeout</code></span> پیاده‌سازی می‌شود و بهینه‌سازی قابل توجهی در عملکرد برنامه‌های تحت وب ایجاد می‌کند.
</p>



</details>




_base.html:
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
                        <a class="nav-link active" href="#"><i class="bi bi-house"></i> خانه</a>
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
</body>
</html>
```
```
git diff src/templates/_base.html
```

src/static/css/main.css
```css
:root {
  --primary-color: #4e73df;
  --secondary-color: #f8f9fc;
}

/* Layout Styles */
html, body {
  height: 100%;
}

body {
  font-family: Vazirmatn, sans-serif;
  background-color: var(--secondary-color);
  text-align: right !important;
  direction: rtl;
  display: flex;
  flex-direction: column;
}

main {
  flex: 1 0 auto;
  padding-bottom: 60px; /* Extra space for footer*/
}

footer {
  flex-shrink: 0;
  background-color: #343a40;
  color: white;
  padding: 1rem 0;
}

/* Navbar Styles */
.navbar-brand {
  font-weight: 600;
}

/* Card Styles */
.card {
  border-radius: 0.5rem;
  box-shadow: 0 0.15rem 0.5rem rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.card:hover {
  transform: translateY(-5px);
}

.card-header {
  background-color: var(--primary-color);
  color: white;
  border-radius: 0.5rem 0.5rem 0 0 !important;
}

/* Form Styles */
.form-control, 
.input-group-text, 
.form-select {
  direction: rtl;
}

.input-group-text {
  border-left: none;
  border-right: 1px solid #ced4da;
}

.form-control {
  border-right: none;
  border-left: 1px solid #ced4da;
}

/* Product Styles */
.product-img {
  height: 180px;
  object-fit: contain;
  padding: 10px;
}

/* Button Styles */
.filter-btn {
  width: 100%;
}

/* Empty State Styles */
.empty-state {
  text-align: center;
  padding: 2rem;
}

.empty-state i {
  font-size: 3rem;
  color: #6c757d;
}

/* Filter Button Container Styles */
.filter-btn-container {
    padding-top: 1.9rem;
}

/* list_view */
.noUi-connect {
    background: #4e73df;
}

.noUi-target {
    margin-top: 10px;
    margin-bottom: 20px;
    direction: ltr;
    height: 8px;
    background: #f5f5f5;
    border-radius: 4px;
    border: 1px solid #ddd;
}

.noUi-handle {
    border-radius: 50%;
    width: 20px;
    height: 20px;
    top: -7px;
    right: -10px;
    background: #4e73df;
    border: 2px solid #fff;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    cursor: pointer;
}

.noUi-handle:before,
.noUi-handle:after {
    display: none;
}

.noUi-tooltip {
    font-family: Vazirmatn, sans-serif;
    direction: rtl;
    background: #4e73df;
    color: white;
    border: none;
    padding: 2px 6px;
    border-radius: 3px;
    font-size: 12px;
    bottom: 120%;
}

.noUi-horizontal .noUi-tooltip {
    bottom: 120%;
}
```
```
git diff src/static/css/main.css
```

cd .. or terminal 2
```
cd ..
```
```
git status
git add .
git commit -m "Add price range slider with nouislider" 
```
```
cd src/
```

### test:
###  max price
```
max price: 1000
output: three product
```
### min price
```
min price: 1500
output: two product
```

# 4. add form

create src/shop/forms.py
```
touch src/shop/forms.py
#
touch shop/forms.py
```

src/shop/forms.py
```python
from django import forms

class ProductFilterForm(forms.Form):
    search = forms.CharField(
        required=False,
        label="جستجو",
        widget=forms.TextInput(attrs={
            "placeholder": "نام محصول...",
            "class": "form-control text-end ",
            "id": "search"
        })
    )
    min_price = forms.IntegerField(
        required=False,
        label="حداقل قیمت",
        widget=forms.NumberInput(attrs={
            "placeholder": "حداقل",
            "class": "form-control text-end",
            "id": "min_price"
        })
    )
    max_price = forms.IntegerField(
        required=False,
        label="حداکثر قیمت",
        widget=forms.NumberInput(attrs={
            "placeholder": "حداکثر",
            "class": "form-control text-end",
            "id": "max_price"
        })
    )
    availability = forms.ChoiceField(
        required=False,
        label="وضعیت موجودی",
        choices=[
            ("", "همه"),
            ("available", "موجود"),
            ("unavailable", "ناموجود")
        ],
        widget=forms.Select(attrs={
            "class": "form-select text-end",
            "id": "availability"
        })
    )
```

update src/shop/views.py
```python
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
```
```
git diff src/shop/views.py
```

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
            <form method="get" class="row g-3">
                <!-- search -->
                <div class="col-md-3">
                    {{ form.search.label_tag }}
                    {{ form.search }}
                </div>

                <!-- Inventory status -->
                <div class="col-md-2">
                    {{ form.availability.label_tag }}
                    {{ form.availability }}
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

cd .. or terminal 2

```
cd ..
```
```
git status
git add .
git commit -m "Add ProductFilterForm with search, price range, and availability filters" 
```
```
cd src/
```

```
git checkout develop
git merge feature/list-view
```

remove branch:
```
git branch -d feature/list-view
```


