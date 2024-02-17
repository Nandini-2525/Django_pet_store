from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from useraccount.forms.registration_form import RegistrationForm
from useraccount.forms.login_form import LoginForm
from useraccount.forms.update_form import UpdateForm
from useraccount.models import UserAccount


def landing_page_view(request):
    """
    Return site landing page
    :template:`useraccount/home.html`
    """
    return render(request, "useraccount/home.html")

def registration_view(request):
    """
    Register user.
    **Context**
    ``register_form``
        register form (email, password).
    **Template:**
    :template:`useraccount/register.html`
    """
    context = {}

    if request.POST:
        form = RegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')

            account = authenticate(email=email, username=email, password=raw_password)
            login(request, account)
            return redirect('home')
        else:
            context['registration_form'] = form
            return render(request, "useraccount/register.html", context)
    else: #get request
        context['registration_form'] = RegistrationForm()
        return render(request, "guest/register.html", context)

def login_view(request):
    """
    Log user in.
    **Context**
    ``login_form``
        login form (email, password ).
    **Template:**
    :template:`useraccount/login.html`
    """
    user = request.user
    if user.is_authenticated:
        return redirect("home")

    context = {}

    if request.POST:
        form = LoginForm(request.POST)

        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']

            user = authenticate(email=email, password=password)

            if user:
                login( request, user)
                return redirect('home')
        else:
            context['login_form'] = form
            return render(request, 'guest/home.html', context)
    else:
        context['login_form'] = LoginForm()
        return render(request, 'guest/home.html', context)

def logout_view(request):
    """
    Destroys auth session`.
    Returns redirect to guest page home.html
    """
    logout(request)
    return redirect('home')


def update_user_view(request):
    """
    Update an instance of :model:`useraccount.UserAccount`.
    **Context**
    ``update_form``
        update form with data from user.id:`useraccount.UserAccount`.
    **Template:**
    :template:`useraccount/profile.html`
    """

    if not request.user.is_authenticated:
        return redirect("login")

    context = {}

    if request.POST:
        form = UpdateForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            form = UpdateForm(initial={
                "email": request.user.email,
                "username": request.user.username,
                "first_name": request.user.first_name,
                "last_name": request.user.last_name,
                "phone_number": request.user.phone_number,
            })

        context["update_form"] = form
        return render(request, "useraccount/profile.html", context)
    else:
        form = UpdateForm(initial={
            "email": request.user.email,
            "username": request.user.username,
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
            "phone_number": request.user.phone_number,
        })

        context['update_form'] = form
        return render(request, "useraccount/profile.html", context)


def network_view(request):
    """
    Display list of :model:`useraccount.UserAccount`.
    **Context**
    ``accounts``
        A list of instances:model:`useraccount.UserAccount`.
    **Template:**
    :template:`useraccount/network.html`
    """

    if not request.user.is_authenticated:
        return redirect("login")
    context = {}

    accounts = UserAccount.objects.all()
    context['accounts'] = [
        {
            'first_name': account.first_name,
            'last_name': account.last_name,
            'phone_number': account.phone_number,
            'email': account.email,
            'username': account.username,
            'x': account.address_x,
            'y': account.address_y,
          } for account in accounts]

    return render(request, "useraccount/network.html", context)

def account_view(request, slug):
    """
    Display an individual :model:`useraccount.UserAccount`.
    **Context**
    ``account``
        An instance of :model:`useraccount.UserAccount`.
    **Template:**
    :template:`useraccount/network_account.html`
    """

    if not request.user.is_authenticated:
        return redirect("login")

    context = {}
    account = get_object_or_404(UserAccount, username=slug)
    context['account'] = account

    return render(request, "useraccount/network_account.html", context)






