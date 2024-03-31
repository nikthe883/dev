from django.db import models
from django.db.models import Avg
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    """
    Model representing a category for products.
    """
    name = models.CharField(max_length=250, db_index=True)
    slug = models.SlugField(max_length=250, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='sub_categories')
    
    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('list-category', args=[self.slug])


    
    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('list-category', args=[self.slug])
    


class Product(models.Model):
    """
    Model representing a product.
    """

    category = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=250)
    brand = models.CharField(max_length=250, default='un-branded')
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=255)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    user = models.ForeignKey(User, max_length=10, on_delete=models.CASCADE, null=True)

    @property
    def average_rating(self):
        """
        Property to calculate the average rating of the product.
        """
        return self.reviews.aggregate(Avg('rating'))['rating__avg'] or 0

    @staticmethod
    def best_product():
        best_product = Product.objects.annotate(avg_rating=Avg('reviews__rating')).order_by('-avg_rating').first()
        return best_product
    

    def save(self, *args, **kwargs):
        """
        Custom save method to generate slug if not provided.
        """

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
    """
    Model representing images associated with a product.
    """

    product = models.ForeignKey(Product, default=None,on_delete=models.CASCADE,  related_name='images')
    image = models.ImageField(upload_to='images')




class ProductReview(models.Model):
    """
    Model representing a review for a product.
    """

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0, null=True)
    content = models.TextField(blank=True, max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)