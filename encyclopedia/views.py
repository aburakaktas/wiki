from django.shortcuts import render
from django.http import HttpResponse
import markdown2
import re
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def article(request, article_name):
    article = util.get_entry(article_name)
    if article:
        article_title = re.findall("^# (.*)", article)
        # print("title:", article_title[0])
        # print(article)
        return render(request, "encyclopedia/article.html",
                      {"article": markdown2.markdown(article),
                      "article_title": article_title[0],
                      })
    else:
        return HttpResponse("404 not found")
