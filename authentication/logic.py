import hashlib

from django.contrib import messages
from django.shortcuts import redirect
import re
from authentication.models import UserDetails


# storing the data
def set_session_data(request, key, value):
    request.session[key] = value


# retreiving the data
def get_session_data(request, key):
    value=request.session.get(key,None)
    return key,value
    # return request.session.get(key, False)


# deleting the data
def delete_session_data(request, key):
    return request.session.pop(key, None)


def profile_is_empty(user):
    return not bool(
        user.name and user.email and user.password
    )


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def is_valid_password(password):
    # Password should be at least 8 characters and contain at least one special character and one uppercase letter
    return len(password) >= 8 and re.search(r'[!@#$%^&*(),.?":{}|<>]', password) and any(char.isupper() for char in password)



def auth(by_pass_route=False):
    def outer_function(func):
        def inner_function(request, *args, **kwargs):
            user = None

            if email := request.session.get("login_token", None):
                user = UserDetails.objects.get(email=email)

            if not user:
                messages.error(request, "Please login to continue...")
                return redirect("/login/")

            request.user = user

            if by_pass_route:
                return func(request, *args, **kwargs)

            # if profile_is_empty(user):
            #     return redirect("/user/update")

            return func(request, *args, **kwargs)

        return inner_function

    return outer_function
