from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.forms import UserCreationForm
from .forms import UserCreateForm


# Create your views here.
def register(request):
  if request.method == 'POST':
    form = UserCreateForm(request.POST)
    form.fields['username'].widget.attrs.update({
            'placeholder': 'Username'
        })
    form.fields['first_name'].widget.attrs.update({
            'placeholder': 'First Name'
        })
    form.fields['last_name'].widget.attrs.update({
            'placeholder': 'Last Name'
        })
    form.fields['email'].widget.attrs.update({
            'placeholder': 'Email'
        })
    form.fields['password1'].widget.attrs.update({
            'placeholder': 'Password'
        })
    form.fields['password2'].widget.attrs.update({
            'placeholder': 'Confirm Password'
        })
    if form.is_valid():
      form.save()
      username = form.cleaned_data.get('username')
      messages.success(request,f"Welcome {username}, Please login to continue!")
      return redirect("login")
      # return redirect("practice:index")
    # else:
      # messages.error(request,'Something went wrong!')
      # return redirect("register")
  else:
    form = UserCreateForm()
    form.fields['username'].widget.attrs.update({
            'placeholder': 'Username'
        })
    form.fields['first_name'].widget.attrs.update({
            'placeholder': 'First Name'
        })
    form.fields['last_name'].widget.attrs.update({
            'placeholder': 'Last Name'
        })
    form.fields['email'].widget.attrs.update({
            'placeholder': 'Email'
        })
    form.fields['password1'].widget.attrs.update({
            'placeholder': 'Password'
        })
    form.fields['password2'].widget.attrs.update({
            'placeholder': 'Confirm Password'
        })
  return render(request,'account/register.html',{'form':form})


@login_required
def userProfile(request):
  return render(request,'account/profile.html')

