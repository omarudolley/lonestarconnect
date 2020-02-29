from django.contrib.auth import login
from django.shortcuts import render,redirect
from .forms import SignUpForm, Update_profile, Update_image
from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user= form.save()
            login(request,user)
            return redirect('forum-home')
    else:
        form = SignUpForm()
    return render(request, 'users/register.html', {'form':form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = Update_profile(request.POST,instance=request.user)
        i_form = Update_image(request.POST,request.FILES,instance = request.user.profile)
        if u_form.is_valid() and i_form.is_valid():
            u_form.save()
            i_form.save()
            messages.success(request, f"Your Account has been updated")
            return redirect('profile')
    else:
        u_form = Update_profile(instance=request.user)
        i_form = Update_image(instance = request.user.profile)

    context ={
            'u_form': u_form,
            'i_form':i_form
    }
    return render(request,'users/profile.html', context)
