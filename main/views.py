from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from main.forms import UserRegistrationForm, NewsForm, EventForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login
from main.models import Profile, HighlightedEvents, News, Volunteers, Contact, Ambassador, SpreadWord, JobApplication
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'home/index.html')


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
            prof.organization_slug = slugify(user_form.cleaned_data["organization_name"])
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


def organization_details(request, slug):
    if request.method == 'POST':
        if request.POST.get('form_type') == "spread_word":
            s = SpreadWord()
            s.name = request.POST.get('name')
            s.email = request.POST.get('email')
            s.about = request.POST.get('about')
            s.organization = get_object_or_404(Profile, pk=request.POST.get('organization_id')).organization_user
            s.save()
        elif request.POST.get('form_type') == "ambassador":
            a = Ambassador()
            a.name = request.POST.get('name')
            a.email = request.POST.get('email')
            a.about = request.POST.get('about')
            a.organization = get_object_or_404(Profile, pk=request.POST.get('organization_id')).organization_user
            a.save()
        elif request.POST.get('form_type') == "volunteer":
            v = Volunteers()
            v.name = request.POST.get('name')
            v.email = request.POST.get('email')
            v.about = request.POST.get('about')
            v.organization = get_object_or_404(Profile, pk=request.POST.get('organization_id')).organization_user
            v.save()
        elif request.POST.get('form_type') == "job":
            j = JobApplication()
            j.name = request.POST.get('name')
            j.about = request.POST.get('about')
            j.city = request.POST.get('city')
            j.state = request.POST.get('state')
            j.email = request.POST.get('email')
            j.years_of_experience = request.POST.get('yoe')
            j.organization = get_object_or_404(Profile, pk=request.POST.get('organization_id')).organization_user
            j.save()
        elif request.POST.get('form_type') == "contact":
            c = Contact()
            c.name = request.POST.get('name')
            c.email = request.POST.get('email')
            c.subject = request.POST.get('subject')
            c.message = request.POST.get('message')
            c.organization = get_object_or_404(Profile, pk=request.POST.get('organization_id')).organization_user
            c.save()

    org = get_object_or_404(Profile, organization_slug=slug)
    line1 = org.organization_primary_objective1
    line2 = org.organization_primary_objective2
    line3 = org.organization_primary_objective3
    cnt = 0
    list_of_events = []
    final_events = {}
    final_causes = {}
    list_temp = []
    for i in org.organization_user.events.all():
        if cnt == 1:
            list_temp.append(i)
            list_of_events.append(list_temp)
            cnt = 0
            list_temp = []
        else:
            list_temp.append(i)
            cnt += 1
    if list_temp:
        list_of_events.append(list_temp)
    cnt = 0
    for i in list_of_events:
        final_events[cnt] = i
        cnt += 1
    cnt = 0
    for i in org.organization_user.causes.all():
        final_causes[cnt] = i
        cnt += 1
    context = {
        'about': org.about,
        'id': org.id,
        'news': org.organization_user.news.all(),
        'name': org.name,
        'events': final_events,
        'mission': org.organization_mission,
        'city': org.organization_city,
        'country': org.organization_country,
        'causes': final_causes,
        'contact_email': org.organization_contact_email,
        'line1': line1,
        'line2': line2,
        'line3': line3,
    }
    return render(request,
                  'main/organization.html',
                  context=context)


def organizations(request):

    object_list = Profile.objects.all()
    paginator = Paginator(object_list, 8)  # 8 organizations in each page

    page = request.GET.get('page')
    try:
        organizations_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        organizations_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        organizations_list = paginator.page(paginator.num_pages)

    return render(request,
                  'home/organizations.html',
                  {'page': page,
                   'organizations': organizations_list,
                   })


@login_required
def dashboard(request):
    org = get_object_or_404(Profile, organization_user=request.user)
    org_name = org.name
    context = {
        'org_name': org_name,
        'org': org,
    }
    return render(request, 'admin/dashboard.html', context=context)


@login_required
def events_list(request):
    if request.method == 'POST':
        ev_id = request.POST.get('event_id')
        ev = get_object_or_404(HighlightedEvents, pk=ev_id)
        ev.delete()
        return redirect('main:events_list')

    events = request.user.events.all()
    context = {
        'events': events,
    }
    return render(request, 'admin/events_list.html', context=context)


@login_required
def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            new_event = form.save(commit=False)
            new_event.organization = request.user
            new_event.event_name = request.POST.get('event_name')
            new_event.event_link = request.POST.get('event_link')
            new_event.event_start_date = request.POST.get('event_start_date')
            new_event.event_end_date = request.POST.get('event_end_date')
            new_event.event_start_time = request.POST.get('event_start_time')
            new_event.event_end_time = request.POST.get('event_end_time')
            new_event.slug = slugify(request.POST.get('event_name'))
            new_event.save()
            return redirect('main:events_list')
    else:
        form = EventForm()
    context = {
        'form': form,
    }
    return render(request, 'admin/add_events.html', context=context)


@login_required
def news_list(request):
    if request.method == "POST":
        ev_id = request.POST.get('news_id')
        ev = get_object_or_404(News, pk=ev_id)
        ev.delete()
        return redirect('main:news_list')
    news = request.user.news.all()
    context = {
        'news_list': news,
    }
    return render(request, 'admin/news_list.html', context=context)


@login_required
def add_news(request):
    if request.method == 'POST':
        news_form = NewsForm(request.POST)
        if news_form.is_valid():
            new_news = news_form.save(commit=False)
            new_news.organization = request.user
            new_news.title = request.POST.get('title')
            new_news.slug = slugify(request.POST.get('title'))
            new_news.tags = request.POST.get('tags')
            new_news.news_image = request.FILES['image']
            new_news.save()
            return redirect('main:news_list')
    else:
        news_form = NewsForm()
    context = {
        'news_form': news_form
    }
    return render(request,
                  'admin/add_news.html',
                  context=context
                  )


@login_required
def volunteers_list(request):
    if request.method == 'POST':
        ev_id = request.POST.get('volunteer_id')
        ev = get_object_or_404(Volunteers, pk=ev_id)
        ev.delete()
        return redirect('main:volunteers_list')

    volunteers = request.user.volunteers.all()
    context = {
        'volunteers': volunteers,
    }
    return render(request, 'admin/volunteers.html', context=context)


@login_required
def contact(request):
    if request.method == "POST":
        ev_id = request.POST.get('contact_id')
        ev = get_object_or_404(Contact, pk=ev_id)
        ev.delete()
        return redirect('main:contact')

    contacts = request.user.contact.all()
    print(contacts)
    context = {
        'contacts': contacts,
    }
    return render(request, 'admin/contact.html', context=context)


@login_required
def ambassador(request):
    if request.method == 'POST':
        ev_id = request.POST.get('ambassador_id')
        ev = get_object_or_404(Ambassador, pk=ev_id)
        ev.delete()
        return redirect('main:ambassador')

    ambassadors = request.user.ambassador.all()
    context = {
        'ambassadors': ambassadors,
    }
    return render(request, 'admin/ambassador.html', context=context)


@login_required
def spreads(request):
    if request.method == 'POST':
        ev_id = request.POST.get('spread_id')
        ev = get_object_or_404(SpreadWord, pk=ev_id)
        ev.delete()
        return redirect('main:spread')

    spread = request.user.spreadword.all()
    context = {
        'spreads': spread,
    }
    return render(request, 'admin/spread.html', context=context)


@login_required
def jobs(request):
    if request.method == 'POST':
        ev_id = request.POST.get('job_id')
        ev = get_object_or_404(JobApplication, pk=ev_id)
        ev.delete()
        return redirect('main:job')

    job = request.user.careers.all()
    context = {
        'jobs': job,
    }
    return render(request, 'admin/job.html', context=context)
