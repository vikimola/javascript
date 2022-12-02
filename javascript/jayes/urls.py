from django.urls import path, reverse_lazy

from . import views
from .models import Post
from .owner import OwnerCreateView, OwnerUpdateView, OwnerDeleteView

base = "jayes/templates/jayes/"

urlpatterns = [
    path("home", views.home, name="home"),
    path("about", views.about, name="about"),
    path('third', views.third, name='third'),
    path('fourth', views.fourth, name='fourth'),
    path("jquerry", views.jquerry, name="jquerry"),
    path("jsonfun", views.jsonfun, name="jsonfun"),
    path("favs", views.FavsList.as_view(), name="favs"),
    path("log", views.log, name="log"),
    path("log_in", views.log_in, name="log_in"),
    path('thing/<int:pk>/favorite',
         views.AddFavoriteView.as_view(), name='thing_favorite'),
    path('thing/<int:pk>/unfavorite',
         views.DeleteFavoriteView.as_view(), name='thing_unfavorite'),

    path("posts", views.PostList.as_view(), name="posts"),
    path("posts/create",
         OwnerCreateView.as_view(
             model=Post,
             fields=["title", "text"],
             template_name=base + "Post/form.html",
             success_url=reverse_lazy("posts"),
         ), name="pcreate"),
    path("posts/<int:pk>/update",
         OwnerUpdateView.as_view(
             model=Post,
             fields=["title", "text"],
             template_name=base + "Post/form.html",
             success_url=reverse_lazy("posts"),
         ), name="pupdate"),
    path("posts/<int:pk>/delete",
         OwnerDeleteView.as_view(
             model=Post,
             template_name=base + "Post/confirm_delete.html",
             success_url=reverse_lazy("posts"),
         ), name="pdelete"),
]
