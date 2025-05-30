from django.db import models
from config.models import CityConfiguration

class Product(models.Model):
    url = models.URLField(max_length=255, unique=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    category = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    product_code = models.CharField(max_length=35, blank=True, null=True)
    color = models.CharField(max_length=100, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discount_ratio = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    in_stock = models.BooleanField(default=False)
    images = models.JSONField(default=list)
    timestamp = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50, default="pending")

    def save(self, *args, **kwargs):
        from config.utils import apply_price_configuration
        if self.price:
            self.price = apply_price_configuration(self.price)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.url or "Product"
    
    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        
class ProductSize(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sizes')
    size_name = models.CharField(max_length=50)
    size_id = models.CharField(max_length=50, blank=True, null=True)
    size_general_stock = models.IntegerField(default=0)
    product_option_size_reference = models.CharField(max_length=50, blank=True, null=True)
    barcode_list = models.JSONField(default=list)
    
    def __str__(self):
        return f"{self.product} - {self.size_name}"
    
    class Meta:
        verbose_name = "Product Size"
        verbose_name_plural = "Product Sizes"
        unique_together = ('product', 'size_name')

class City(models.Model):
    city_id = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "City"
        verbose_name_plural = "Cities"

class Store(models.Model):
    store_code = models.CharField(max_length=20, primary_key=True)
    store_name = models.CharField(max_length=200)
    city = models.ForeignKey(CityConfiguration, on_delete=models.CASCADE, related_name='stores')
    store_county = models.CharField(max_length=100, blank=True, null=True)
    store_phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    latitude = models.CharField(max_length=20, blank=True, null=True)
    longitude = models.CharField(max_length=20, blank=True, null=True)
    
    def __str__(self):
        return self.store_name
    
    class Meta:
        verbose_name = "Store"
        verbose_name_plural = "Stores"

class SizeStoreStock(models.Model):
    product_size = models.ForeignKey(ProductSize, on_delete=models.CASCADE, related_name='store_stocks')
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='size_stocks')
    stock = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.product_size} - {self.store}: {self.stock}"
    
    class Meta:
        verbose_name = "Size Store Stock"
        verbose_name_plural = "Size Store Stocks"
        unique_together = ('product_size', 'store')