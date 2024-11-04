from django.db import models
from django.conf import settings
from django.db.models import Q

from .validators import validate_title

User = settings.AUTH_USER_MODEL

class ProductQuerySet(models.QuerySet):
    def is_public(self):
        return self.filter(public=True)
    
    def search(self, query, user):
        lookup = Q(title_icontains=query) | Q(content_icontains=query)
        qs = self.is_public().filter(lookup)
        if user is not None: # add private data to qs that matches the query
            qs2 = qs.filter(user=user).filter(lookup)
            qs = (qs | qs2).distinct()
        return qs

class ProductManager(models.Manager): # default Manager for each model is .objects ...
    def get_queryset(self, *args, **kwargs):
        return ProductQuerySet(self.model, using=self._db)

    def search(self, user=None):
        return self.get_queryset().search(user)

class Product(models.Model):
    user = models.ForeignKey(User, default=1, null=True, on_delete=models. SET_NULL)
    title = models.CharField(max_length=30, validators=[validate_title])
    content = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=99.99)
    public = models.BooleanField(default=True)

    objects = ProductManager()

    @property
    def sale_price(self):
        return "%.2f" %(float(self.price) * 0.8)
    
    def get_discount(self):
        return 'Some discount string'

    def __str__(self):
        return f'{self.title}'
