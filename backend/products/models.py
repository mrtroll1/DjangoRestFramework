from django.db import models

# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=99.99)

    @property
    def sale_price(self):
        return "%.2f" %(float(self.price) * 0.8)
    
    def get_discount(self):
        return 'Some discount string'

    def __str__(self):
        return f'{self.title}'
