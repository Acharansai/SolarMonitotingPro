from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from .forms import LoginForm


def login_view(request):

    if request.user.is_authenticated:
        return redirect("monitoring:dashboard")


    form = LoginForm()


    if request.method == "POST":

        form = LoginForm(request.POST)


        if form.is_valid():

            username = form.cleaned_data["username"]

            password = form.cleaned_data["password"]


            user = authenticate(
                request,
                username=username,
                password=password
            )


            if user is not None:

                login(request, user)

                return redirect(
                    "monitoring:dashboard"
                )


            messages.error(
                request,
                "Invalid username or password."
            )


    return render(
        request,
        "accounts/login.html",
        {
            "form": form
        }
    )


def logout_view(request):

    logout(request)

    return redirect(
        "accounts:login"
    )