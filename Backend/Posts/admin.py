from django.contrib import admin

# Register your models here.
from .models import Post,SavedPost
admin.site.register(Post)
admin.site.register(SavedPost)