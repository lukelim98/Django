from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse

monthly_challanges = {
    'january': 'Eat no meat for the entire month',
    'february': 'Walk for at least 20 minutes every day!',
    'march': 'Learn Django for at least 20 mintues every day!',
    'april': 'Go practice golf swing once a week.',
    'may': 'Go to gym atleast 4 times a week.',
    'june': 'Solve atleast one baekjoon question a day.',
    'july': 'Read book every day.',
    'august': 'Play summoners war.',
    'september': 'Get a good ld 5 that I need.',
    'october': 'Play RTA in summoners war.',
    'november': 'Study Linux.',
    'december': None,

}

# Create your views here.x


def index(request):
    list_items = ""
    months = list(monthly_challanges.keys())
    month_path_list = []
    for month in months:
        month_path_list.append((month, reverse('month-challanges', args=[month])))
    return render(request, 'challanges/index.html', {
        'month_path_list': month_path_list
    })

def monthly_challange_by_number(request, month):
    months = list(monthly_challanges.keys())
    if month > len(months):
        return HttpResponseNotFound('Invalid Month')
    redirect_month = months[month-1]
    redirect_path = reverse("month-challanges", args=[redirect_month])
    return HttpResponseRedirect(redirect_path)


def monthly_challange(request, month):
    if month in monthly_challanges:
        challange_text = monthly_challanges[month]
        return render(request, 'challanges/challange.html', {
            'text': challange_text,
            'month_name': month
        })
    else:
        return HttpResponseNotFound("<h1>This month is not supported</h1>")
