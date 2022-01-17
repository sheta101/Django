from turtle import title
from django.db import models
from django.utils import timezone                #use for current time
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager



# Create your models here.


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status = 'published')



class Post(models.Model):                          #create class for POST data
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),)


    title = models.CharField(max_length = 50)            # For the POST title.
    slug = models.SlugField(max_length = 250, unique_for_date = 'publish')
    author = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'blog_posts')  #give foreign key for author's and define Many-to-one relationship
                                                                                                    #CASCADE use for delete dependancy delete related post from the database
    
    body = models.TextField()                           #For the body of the post.
    publish = models.DateTimeField(default = timezone.now)         #This datetime indicates when the post was published.
    created = models.DateTimeField(auto_now_add = True)            #This datetime indicates when the post was created. 
    updated = models.DateTimeField(auto_now = True)                #This datetime indicates the last time the post was updated.
    status = models.CharField(max_length = 10, choices = STATUS_CHOICES, default = 'draft')  #Shows the status of Post.



    objects = models.Manager() # The default manager.
    published = PublishedManager() # Our custom manager.

    tags = TaggableManager()



    def get_absolute_url(self):
        return reverse('blog:post_detail',
                        args=[self.publish.year,
                        self.publish.month,
                        self.publish.day, self.slug])

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name = 'comments')   #associate a comment with asingle post.
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)


    def __str__(self):
        return f'Comment by {self.name} on {self.post}'

