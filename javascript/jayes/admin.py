from django.contrib import admin

# Register your models here.
from .models import Thing, Fav, Post

admin.site.register(Thing)
admin.site.register(Fav)
admin.site.register(Post)
