from django.db import models


from django.urls import reverse
from django.template.defaultfilters import slugify

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator



class Category(models.Model):

    name = models.CharField(max_length=250, db_index=True)
    slug = models.SlugField(max_length=250, unique=True)
    
    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('list-category', args=[self.slug])


class Product(models.Model):

    category = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=250)
    brand = models.CharField(max_length=250, default='un-branded')
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=255)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    user = models.ForeignKey(User, max_length=10, on_delete=models.CASCADE, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Product, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'products'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product-info', args=[self.slug])


class Images(models.Model):
    product = models.ForeignKey(Product, default=None,on_delete=models.CASCADE,  related_name='images')
    image = models.ImageField(upload_to='images')



class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0, null=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)