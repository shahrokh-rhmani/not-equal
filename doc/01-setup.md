<p dir="rtl" align="justify">
این فایل <span dir="ltr"><code>01-setup.md</code></span> مراحل اولیه راه‌اندازی یک پروژه Django با نام <span dir="ltr"><code>not-equal</code></span> را توضیح می‌دهد. ابتدا ساختار پایه پروژه شامل ایجاد فولدرهای اصلی، <span dir="ltr"><code>git init</code></span> و تنظیم branchهای <span dir="ltr"><code>develop</code></span> و <span dir="ltr"><code>feature/base-setup</code></span> شرح داده شده است. سپس تنظیمات اولیه مانند ایجاد <span dir="ltr"><code>.gitignore</code></span> برای فایل‌های غیرضروری، ساخت virtual environment با <span dir="ltr"><code>venv</code></span> و نصب Django با <span dir="ltr"><code>pip</code></span> آمده است. در ادامه، پیکربندی اولیه پروژه شامل تنظیم <span dir="ltr"><code>templates</code></span>، <span dir="ltr"><code>static files</code></span>، <span dir="ltr"><code>media</code></span> و <span dir="ltr"><code>urls.py</code></span> توضیح داده شده و در نهایت، تغییرات با commitهای مناسب در git ذخیره می‌شوند.
</p>

# 1.

project-root:
```
mkdir not-equal
cd not-equal
```
```
git init 
```
```
touch README.md 
```
```
git add README.md
git commit -m "Initial commit"
```

```
git checkout -b develop
```
```
touch .gitignore
```
```
code .
```
.gitignore
```python
# Django #
*.log
*.pot
*.pyc
__pycache__
db.sqlite3
media

# Backup files #
*.bak

# If you are using PyCharm #
# User-specific stuff
.idea/**/workspace.xml
.idea/**/tasks.xml
.idea/**/usage.statistics.xml
.idea/**/dictionaries
.idea/**/shelf

# AWS User-specific
.idea/**/aws.xml

# Generated files
.idea/**/contentModel.xml

# Sensitive or high-churn files
.idea/**/dataSources/
.idea/**/dataSources.ids
.idea/**/dataSources.local.xml
.idea/**/sqlDataSources.xml
.idea/**/dynamic.xml
.idea/**/uiDesigner.xml
.idea/**/dbnavigator.xml

# Gradle
.idea/**/gradle.xml
.idea/**/libraries

# File-based project format
*.iws

# IntelliJ
out/

# JIRA plugin
atlassian-ide-plugin.xml

# Python #
*.py[cod]
*$py.class

# Distribution / packaging
.Python build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.coverage
.coverage.*
.cache
.pytest_cache/
nosetests.xml
coverage.xml
*.cover
.hypothesis/

# Jupyter Notebook
.ipynb_checkpoints

# pyenv
.python-version

# celery
celerybeat-schedule.*

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/
../env/

# mkdocs documentation
/site

# mypy
.mypy_cache/

# Sublime Text #
*.tmlanguage.cache
*.tmPreferences.cache
*.stTheme.cache
*.sublime-workspace
*.sublime-project

# sftp configuration file
sftp-config.json

# Package control specific files Package
Control.last-run
Control.ca-list
Control.ca-bundle
Control.system-ca-bundle
GitHub.sublime-settings

# Visual Studio Code #
.vscode/*
!.vscode/settings.json
!.vscode/tasks.json
!.vscode/launch.json
!.vscode/extensions.json
.history
```

```
git add .gitignore
git commit -m "Add .gitignore file"
```

# 2. 
```
git checkout -b feature/base-setup
```

Create a virtual environment in project root not src/ (windows)
```
python -m venv venv
.\venv\Scripts\activate
```
or

Create a virtual environment in project root not src/ (linux)
```
python3 -m venv venv
source venv/bin/activate
```

```
mkdir src
cd src/
```

```
pip install django==5.2.4
django-admin startproject config .
python manage.py migrate
python manage.py createsuperuser
```

```
python manage.py runserver
```

requirements.txt:
```
touch requirements.txt
pip freeze > requirements.txt
cat requirements.txt
#
pip freeze > ../requirements.txt
cat ../requirements.txt
```

# 3.

src/templates/
```
mkdir src/templates/
mkdir templates/
```

src/config/settings.py
```python
TEMPLATES = [
    {
        ...

        'DIRS': [BASE_DIR / 'templates'],

        ...

]
```

src/static/
```
mkdir src/static/
mkdir static/
```

```python
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / "static",] # development

MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'
```

src/config/urls.py
```python
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
  # path('', include('')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

# 4.

cd .. or terminal 2
```
git status
git add .
git commit -m "base-setup" 
```
```
git checkout develop
git merge feature/base-setup
```

### remove branch:
```
git branch -d feature/base-setup
```
