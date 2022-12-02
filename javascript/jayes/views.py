import time
from sqlite3 import IntegrityError

from Tools.scripts.make_ctype import method
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from .models import Fav, Thing, Post

base = "jayes/templates/jayes/"


# Create your views here.
def home(request):
    return render(request, base + "home.html")


def about(request):
    return render(request, base + "about.html")


def third(request):
    return render(request, base + "third.html")


def fourth(request):
    return render(request, base + "fourth.html")


def jquerry(request):
    return render(request, base + "jquerry.html")


def jsonfun(request):
    time.sleep(2)
    stuff = {
        'first': 'first thing',
        'second': 'second thing'
    }
    return JsonResponse(stuff)


def log(request):
    return render(request, base + "log_in.html")


def log_in(request):
    if request.method == "POST":
        name = request.POST["name"]
        password = request.POST["password"]

        user = authenticate(request, username=name, password=password)

        if user is not None:
            login(request, user)
            # return redirect(reverse("main"))
            return redirect(reverse("home"))
        else:
            messages.add_message(request, messages.INFO, 'Invalid credentials.')
            return redirect(reverse("home"))


class FavsList(View):
    template_name = base + "fav_list.html"

    def get(self, request):
        thing_list = Thing.objects.all()
        favorites = []

        if request.user.is_authenticated:
            rows = request.user.favorite_things.values("id")
            favorites = [row["id"] for row in rows]

        ctx = {"thing_list": thing_list, "favorites": favorites}

        return render(request, self.template_name, ctx)


@method_decorator(csrf_exempt, name="dispatch")
class AddFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        # print("AAAAAAadd pk", pk)
        t = get_object_or_404(Thing, id=pk)
        fav = Fav(user=request.user, thing=t)
        try:
            fav.save()
        except IntegrityError as e:
            pass
        return HttpResponse()


@method_decorator(csrf_exempt, name="dispatch")
class DeleteFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        # print("Delete PK",pk)
        t = get_object_or_404(Thing, id=pk)
        try:
            fav = Fav.objects.get(user=request.user, thing=t).delete()
        except Fav.DoesNotExist as e:
            pass
        return HttpResponse()


class PostList(View):
    template_name = base + "Post/post_list.html"

    def get(self, request):  # get(key, default=None)
        strval = request.GET.get("search", False)

        if strval:
            # Simple title-only search
            # objects = Post.objects.filter(title__contains=strval).select_related().order_by('-updated_at')[:10]

            # Multi-field search
            # __icontains for case-insensitive search
            query = Q(title__icontains=strval)
            query.add(Q(text__icontains=strval), Q.OR)
            post_list = Post.objects.filter(query).select_related().order_by('-updated_at')[:10]

        else:
            post_list = Post.objects.all().order_by('-updated_at')[:10]

        # Augument the post post_list
        # for obj in post_list:
        #     obj.natural_updated = naturaltime(obj.updated_at)

        # post_list = Post.objects.all()
        ctx = {"post_list": post_list, "search": strval}
        return render(request, self.template_name, ctx)
