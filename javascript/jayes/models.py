from django.conf import settings
from django.core.validators import MinLengthValidator
from django.db import models


# Create your models here.

class Thing(models.Model):
    title = models.CharField(max_length=255, validators=[MinLengthValidator(3)])
    text = models.TextField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                              related_name='fav_thing_owner')

    favorites = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                       through="Fav",
                                       related_name="favorite_things")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Fav(models.Model):
    thing = models.ForeignKey(Thing, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name='favs_users')

    class Meta:
        unique_together = ("thing", "user")

    def __str__(self):
        return '%s likes %s' % (self.user.username, self.thing.title[:10])


class Post(models.Model):
    title = models.CharField(max_length=500, validators=[MinLengthValidator(2)])
    text = models.TextField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                              related_name="post_owner")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title
