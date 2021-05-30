# models
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# creating model manager
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,self).get_queryset().filter(status='published')

# post model
class Post(models.Model):
    STATUS_CHOICES = (
    ('draft', 'Draft'),
    ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)  
    status = models.CharField(max_length=10,choices=STATUS_CHOICES,default='draft')

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title
    
    objects = models.Manager()
    published = PublishedManager()
    def get_absolute_url(self):
        return reverse('post_detail',args=[self.slug])

    def get_comments(self):
        return self.comments.filter(parent=None).filter(active=True)

# comment model    
class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=50)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('created',)
    
    def __str__(self):
        return self.body

    def get_comments(self):
        return self.objects.filter(parent=self).filter(active=True)