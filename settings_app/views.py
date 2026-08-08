from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import redirect, render


@login_required
def settings_page(request):

    password_form = PasswordChangeForm(
        user=request.user
    )

    if request.method == "POST":

        password_form = PasswordChangeForm(
            request.user,
            request.POST
        )

        if password_form.is_valid():

            user = password_form.save()

            # Keep the user logged in after changing password
            update_session_auth_hash(
                request,
                user
            )

            messages.success(
                request,
                "Password changed successfully."
            )

            return redirect(
                "settings_app:settings"
            )

    return render(
        request,
        "settings/settings.html",
        {
            "user": request.user,
            "password_form": password_form,
        }
    )