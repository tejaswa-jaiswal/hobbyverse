from django.contrib import admin
from .models import User
from .models import Content
from .models import Chat
from .models import BlogComment
# Register your models here.
from .models import Community
from .models import Channel
admin.site.register(User)

admin.site.register(Content)
admin.site.register(Channel)
admin.site.register(Chat)
admin.site.register(BlogComment)
admin.site.register(Community)