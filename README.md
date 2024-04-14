ShopyThing

Django ecommerce project, where users can add products, message about the products and add reviews.
The project is using MySQL 

You can visit the live page here:

https://testdjango.nikthe.tech/
<br>

How to run the project:

Clone the repo:
git clone https://github.com/nikthe883/dev.git

Install the requirements:
pip install -r requirements.txt

Connect MySQL Database
In settings.py:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'db_name',
        'USER': 'db_username',
        'PASSWORD': 'db_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

python manage.py makemigrations
python manage.py migrate

python manage.py runserver

Two users are initialized - super_admin , staff_admin 
Both users use the same password: nikola12A

If you with to populate the webpage with fake products, categories and reviews you can use

python manage.py populate_products
