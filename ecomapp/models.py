from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator
# Create your models here.

STATE_CHOICES = (
("Bahawalpur","Bahawalpur"),
( "Bahawalnagar","Bahawalnagar"),
("Rahim Yar Khan","Rahim Yar Khan"),
 ("Gujranwala","Gujranwala"),
("Gujrat","Gujrat"),
 ("Sargodha","Sargodha"),
("Khushab","Khushab"),
 ("Mianwali","Mianwali"),
("Bhakkar","Bhakkar"),
 ("Sahiwal","Sahiwal"),
("Pakpattan","Pakpattan"),
 ('Okara','Okara'),
)

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField( max_length=250)
    locality = models.CharField( max_length=250)
    city = models.CharField( max_length=250)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES, max_length=250)
    def __str__(self):
        return str(self.id )   

CATEGORY_CHOICES = (
    ('M','Mobile'),
    ('L','LAptop'),
    ('S','Shoes'),
    ('J','Jeans'),
    ('ST','Shirts'),

)

class Product(models.Model):
    title = models.CharField( max_length=150)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    brand = models.CharField( max_length=50)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=50)
    product_image = models.ImageField(upload_to='productimg')

    def __str__(self):
        return str(self.id)    

class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)    
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price   

STATUS_CHOICES = (
    ('Accepted','Accepted'),
    ('packed','packed'),
    ('on the way','on the way'),
    ('delivered','delivered'),
    ('cancel','cancel'),
)    
    
class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    order_date = models.DateTimeField( auto_now_add=True)
    status = models.CharField( max_length=150 , choices=STATUS_CHOICES,default='pending')

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price   


class Image(models.Model):
    file = models.ImageField(upload_to='productimg')
    uploaded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pk)
    