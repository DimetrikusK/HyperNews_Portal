from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from django.conf import settings
import datetime
import json
import random
import itertools
import copy


news_file = "news.json"
with open(settings.NEWS_JSON_PATH) as json_file:
    news = json.load(json_file)


def index(request):
    return redirect('/news/')


class ListView(View):
    def get(self, request, title=None, *args, **kwargs):
        return render(request, 'news/news_list.html', context={'news': news})


class DetailView(View):
    def get(self, request, id=0, *args, **kwargs):
        news_list = list()
        q = request.GET.get('q')
        if id != 0:
            context = {'news': news, 'id': id}
            return render(request, 'news/detail.html', context=context)
        elif q:
            for news_items in news:
                if q in news_items['title']:
                    news_list.append(news_items)
            return render(request, 'news/index.html', context={'news': news_list})
        else:
            return render(request, 'news/news_list.html', context={'news': news})


class CreateView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'news/create_form.html')

    def post(self, request, *args, **kwargs):
        while True:
            num_int = random.randint(1, 999999)
            for elem in news:
                if elem['link'] == num_int:
                    break
            else:
                break

        add_news = {'created': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'title': request.POST.get('title'),
                'text': request.POST.get('text'),
                'link': num_int}
        news.append(add_news)

        with open(news_file, "w") as json_file:
            json.dump(news, json_file)

        return redirect('/news/')