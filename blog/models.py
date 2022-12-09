from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django_extensions.db.fields import AutoSlugField



class User(AbstractUser):
    
     email = models.EmailField( null=True)
     phone_no =models.CharField(max_length= 10, null=True)
     city = models.CharField(max_length=20, null=True)
     country = models.CharField(max_length=20, null = True)
     image = models.ImageField()

     def __str__(self):
        return self.email

class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='name', unique=True)
    

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reversed("post_detail", kwargs={"slug": self.slug})


class Tag(models.Model):
    name = models.CharField(max_length=32)
    slug = AutoSlugField(populate_from='name', unique=True)
   
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reversed("post_detail", kwargs={"slug": self.slug})



class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='title', max_length=500, unique=True)
    text = models.TextField()
    tag = models.ManyToManyField(Tag)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    image = models.ImageField(upload_to='post/') 

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class Comment(models.Model):
    content=models.TextField(max_length=500)
    post=models.ForeignKey(Post, on_delete=models.CASCADE,related_name='comments')
    parent=models.ForeignKey('self',on_delete=models.CASCADE, null=True, blank=True, related_name='replies' )
    email= models.EmailField(null=True)
    name=models.CharField(max_length=50, null=True)
    active=models.BooleanField(default=False)

    def save(self,*args,**kwargs):
        self.active=True
        super().save(*args,**kwargs)

    def get_comments(self):
        return Comment.objects.filter(parent=self).filter(active=True)     

    def __str__(self):
        return self.name



