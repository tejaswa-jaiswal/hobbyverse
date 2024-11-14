# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True)  # Ensure email is unique
    userid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    interests = models.TextField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    profile_img = models.ImageField(upload_to='static/profile/', blank=True, null=True)

    REQUIRED_FIELDS = ['username']  # Add 'username' as a required field for superuser creation
    USERNAME_FIELD = 'email'        # Set 'email' as the unique identifier for authentication

    def __str__(self):
        return self.username

class Community(models.Model):
    community_ID= models.AutoField(primary_key=True )
    community_type= models.CharField(max_length=255)
    category = models.CharField(unique=True, max_length=255 )
    community_image=   models.ImageField(upload_to='static/community/', blank=True, null=True)
    def __str__(self) :
        return self.category
class Channel(models.Model):
    channel_ID = models.AutoField(primary_key=True)
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name="channels")  # Link to Community
    channel_name = models.CharField(max_length=255)
    channel_admin = models.ForeignKey(User, on_delete=models.CASCADE, blank=True , null=True)
    description = models.TextField(blank=True, null=True)
    channel_image=   models.ImageField(upload_to='static/channel/', blank=True, null=True)
    def __str__(self):
        return self.channel_name

class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, null= True, blank=False)
    chat_id = models.AutoField(primary_key=True)
    chats = models.TextField()  # Storing chat messages
    chat_date = models.DateField(auto_now_add=True)
    chat_time = models.TimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Chat {self.chat_id} by {self.user.username}"

class Content(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog_id = models.AutoField(primary_key=True)
    blog_img = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    texts = models.TextField()
    interests = models.TextField(blank=True, null=True)  # Store interests related to the blog
    blog_date = models.DateField(auto_now_add=True)
    blog_time = models.TimeField(auto_now_add=True)
    family_friendly = models.BooleanField(default=True)  # True if family-friendly
    no_of_likes = models.IntegerField(default=0)

    def __str__(self):
        return f"Blog {self.blog_id} by {self.user.username}"

class BlogComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='comments')
    comment_text = models.TextField()

    def __str__(self):
        return f"Comment by {self.user.username} on Blog {self.content.blog_id}"
