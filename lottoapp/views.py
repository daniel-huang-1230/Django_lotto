from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def index(request):  #request parameter is just here to be explicit
    return render(request, 'lottoapp/home.html')


def event(request):
    #pass in a dictionary of the variables you want to use in the
    # todo 以下兩項從資料庫抓取
    page_id = 'facebook_fanpage_id'
    lotto_event_no = '0001'
    event_no = page_id + lotto_event_no
    all_feeds_list = ["第一篇", "第二篇", "第三篇"]  # todo 用getAllFeeds抓取
    return render(request, 'lottoapp/event.html', {'event_no':event_no, 'all_posts': all_feeds_list })