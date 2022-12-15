from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from distutils.command.upload import upload
from itertools import product
from pyexpat import model
from unicodedata import category
from venv import create
from django.db import models
from django.contrib.auth.models import User

class User(AbstractUser):
    profile_pic = models.ImageField(upload_to='profile_pic/')
    bio = models.TextField(max_length=160, blank=True, null=True)
    cover = models.ImageField(upload_to='covers/', blank=True)

    def __str__(self):
        return self.username

    def serialize(self):
        return {
            'id': self.id,
            "username": self.username,
            "profile_pic": self.profile_pic.url,
            "first_name": self.first_name,
            "last_name": self.last_name
        }


class page(models.Model):
    creater = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    username=models.CharField(max_length=255,null=True)
    pagename=models.CharField(max_length=255,null=True)
    website=models.CharField(max_length=255,null=True)
    category=models.CharField(max_length=255,null=True)
    
    emial=models.CharField(max_length=255,null=True)
    image=models.ImageField(upload_to='posts/', blank=True)          

class Post(models.Model):
    creater = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    page_name=models.CharField(max_length=255,null=True)
    page_id=models.ForeignKey(page, on_delete=models.CASCADE,null=True)
    date_created = models.DateTimeField(default=timezone.now)
    content_text = models.TextField(max_length=140, blank=True)
    status=models.CharField(max_length=255,null=True)

    Product_Price = models.IntegerField(null=True,blank=True)
    content_image = models.ImageField(upload_to='posts/', blank=True)
    likers = models.ManyToManyField(User,blank=True , related_name='likes')
    savers = models.ManyToManyField(User,blank=True , related_name='saved')
    comment_count = models.IntegerField(default=0)
    posts_type = models.CharField(max_length=255,null=True)


    def __str__(self):
        return f"Post ID: {self.id} (creater: {self.creater})"

    def img_url(self):
        return self.content_image.url

    def append(self, name, value):
        self.name = value

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commenters')
    comment_content = models.TextField(max_length=90)
    comment_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Post: {self.post} | Commenter: {self.commenter}"

    def serialize(self):
        return {
            "id": self.id,
            "commenter": self.commenter.serialize(),
            "body": self.comment_content,
            "timestamp": self.comment_time.strftime("%b %d %Y, %I:%M %p")
        }
    
class Follower(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    followers = models.ManyToManyField(User, blank=True, related_name='following')

    def __str__(self):
        return f"User: {self.user}"
    


class sell(models.Model):
    creater = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    picture=models.ImageField(upload_to='posts/', blank=True)
    Title=models.CharField(max_length=255,null=True)
    price=models.IntegerField()
    category=models.CharField(max_length=255,null=True)
    description=models.CharField(max_length=255,null=True)
    date_created = models.DateTimeField(default=timezone.now)

class pageposts(models.Model):
    creater = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pageposts')
    date_created = models.DateTimeField(default=timezone.now)
    content_text = models.TextField(max_length=140, blank=True)
    content_image = models.ImageField(upload_to='posts/', blank=True)
    likers = models.ManyToManyField(User,blank=True , related_name='pagelikes')
    savers = models.ManyToManyField(User,blank=True , related_name='pagesaved')
    comment_count = models.IntegerField(default=0)



# Create your models here.



class Category(models.Model):
    Category_Name = models.CharField(max_length=255)

    def __str__(self):
        return self.Category_Name




    

class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)  
    product =  models.ForeignKey(Post,on_delete=models.CASCADE)
    product_qty = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.first_name



class Shipping_address(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)  
    Full_name = models.CharField(max_length=255)
    Phone = models.CharField(max_length=12)
    House  = models.CharField(max_length=255)
    Area = models.CharField(max_length=60)
    Landmark = models.CharField(max_length=60)
    Town =  models.CharField(max_length=60)
    State =  models.CharField(max_length=60)
    Zip = models.IntegerField()
    
    def __str__(self):
        return self.Full_name


class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE) 
    shipping_address = models.ForeignKey(Shipping_address,on_delete=models.CASCADE) 
    total_price = models.FloatField(null=False)
    payment_mode = models.CharField(max_length=255,null=False)
   
    Order_statuses = (
        ('Pending','Pending'),
        ('Out For Shipping','Out For Shipping'),
        ('Completed','Completed'),

    )
    
    status =models.CharField(max_length=150,choices=Order_statuses,default='Pending')
    tracking_no = models.CharField(max_length=150,null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now_add=True)

    

  
class Order_Item(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)  
    order = models.ForeignKey(Order,on_delete=models.CASCADE) 
    product = models.ForeignKey(Post,on_delete=models.CASCADE)
    price = models.IntegerField(null=False)
    quanty = models.IntegerField(null=False)   




RATE_CHOICES = [
    (1,'1 - Bad'),
    (2, '2 -OK'),
    (3, '3 -Good'),
    (4, '4 -Very Good'),
    (5, '5 -Perfect')

]


class review(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    post=models.ForeignKey(Post,on_delete=models.CASCADE,null=True)
    body=models.TextField()
    date_added=models.DateField()
    rating=models.PositiveIntegerField(choices=RATE_CHOICES,null=True)




RATING = [
    (1,'1 - Bad'),
    (2, '2 -OK'),
    (3, '3 -Good'),
    (4, '4 -Very Good'),
    (5, '5 -Perfect')
]

class Rating(models.Model):
    rate = models.PositiveIntegerField(choices=RATING,null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE,null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)    

    


class Friendrequest(models.Model):
    from_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="from_user",null=True)
    to_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="to_user",null=True)     




class share(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    post=models.ForeignKey(Post,on_delete=models.CASCADE,null=True)
    date=models.DateField(null=True)
    discription=models.CharField(max_length=255,null=True)
