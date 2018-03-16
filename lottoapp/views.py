from django.shortcuts import render
from lottoapp.models import Event
from django.http import HttpResponse
import lottoapp.lib.parse_page as page
import lottoapp.lib.Lottery as lotto
import os, json, facebook

from django.views.generic import TemplateView

# class EventView(TemplateView):
#     template_name = 'lottoapp/create_event.html'
#
#     # def get(self,request):
#     #
#     #
#     # def post(self,request):
page_id_dict = {"輕鬆買": '320583254962571', "604": '1794576900786201'}  # hard-coded at the moment
# 我方提供token for FB graph API
permenant_token = "EAAErN8EuGWQBAKlPFUzuV0mjhl0MhfvVBVnziV8P1QiVDbFNMZBdb3JSONSYMjI3ZCunLgDofk7nL2lm4PZCpLy6Ywc6ZBqEIVBIYguMRrLUrtZAiScZCZAn5QPYrUHtv3ZABdQZALqTI2w41ZCQXQWOTn8thHQZA5Tmg3jhhGT2cUrZCwZDZD"
graph = facebook.GraphAPI(access_token=permenant_token, version=2.7)


# def index(request):  # request parameter is just here to be explicit
#     return render(request, 'lottoapp/home.html')


def create_event(request):
    # 以下兩項從資料庫抓取
    event = Event.objects.create()
    page_id = page_id_dict['輕鬆買']
    lotto_event_no = event.pk  # get the primary key (event_id)
    event_no = page_id + str(lotto_event_no)
    # pass in a dictionary of the variables you want to use in the
    if request.method == 'GET':


        page_overview = page.getAllFeeds(page_id, permenant_token)
        #print("粉專資訊為", page_overview)
        all_feeds_dict = {}
        for entry in page_overview:
            all_feeds_dict[entry[1]] = entry[2]  # key: 貼文id, value: 文章內容

        return render(request, 'lottoapp/create_event.html', {'event_no': event_no, 'all_posts_dict': all_feeds_dict})
    elif request.method == 'POST':
        if request.POST['interaction'] == 'lottery': #選擇開獎
            event_name = request.POST['event_name']
            post_id = request.POST['option']
            token = permenant_token
            #創造lottery物件
            lottery = lotto.Lottery(event_name, event_no, post_id, page_id, token)
            datetime_str = request.POST['deadline_date'] + " " + request.POST['deadline_time']
            lottery.set_deadline(datetime_str)

            #TODO 體驗卷與自動巡航

            print("偵測規則...", request.POST['rules'])

            return render(request, 'lottoapp/event.html')