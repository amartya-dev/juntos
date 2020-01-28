from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, HttpResponse
from main.forms import UserRegistrationForm, NewsForm
from django.contrib.auth import authenticate, login
from main.models import Profile
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            prof = Profile()
            prof.organization_user = new_user
            prof.name = user_form.cleaned_data["organization_name"]
            prof.ein_number = user_form.cleaned_data["ein_number"]
            prof.about = user_form.cleaned_data["about"]
            prof.save()
            return HttpResponse("Registration Done")
    else:
        user_form = UserRegistrationForm()
    context = {
        'user_form': user_form
    }
    return render(request,
                  'main/register.html',
                  context=context
                  )


@login_required
def add_news(request):
    if request.method == 'POST':
        news_form = NewsForm(request.POST)
        if news_form.is_valid():
            new_news = news_form.save(commit=False)
            new_news.organization = request.user
            new_news.slug = slugify(news_form.cleaned_data['title'])
            new_news.news_details = news_form.cleaned_data['news_details']
            new_news.save()
            return HttpResponse("News Item Saved")
    else:
        news_form = NewsForm()
    context = {
        'news_form': news_form
    }
    return render(request,
                  'main/add_news.html',
                  context=context
                  )

def base_check(request):
    return render(request,'main/organization.html')