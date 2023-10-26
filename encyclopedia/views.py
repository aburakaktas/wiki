from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import markdown2
import re
from . import util
from django import forms


class SearchInput(forms.Form):
    search_query = forms.CharField(label="Search:")


class NewPageInput(forms.Form):
    title = forms.CharField(label="Title:")
    body = forms.CharField(widget=forms.Textarea)

searchInput = SearchInput()

def index(request):
    
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": searchInput,
    })


def search(request):
    if request.method == "GET":
        searchInput = SearchInput(request.GET)
        if searchInput.is_valid():
            search_query = searchInput.cleaned_data["search_query"]

            # check if search query matches an existing entry. if yes redirect to that page
            if util.get_entry(search_query):
                print(search_query, "found")
                return HttpResponseRedirect(f"/wiki/{search_query}")

            # if entry cannot be found, list entries that match as a substring and redirect to search results page
            else:
                print(search_query, "not found")
                all_entries = util.list_entries()
                print(all_entries)

                # list all matched entries
                matched_entries = []
                for entry in all_entries:
                    if search_query in entry.lower():
                        matched_entries.append(entry)

                print("matched entries:", matched_entries)
                
                return render(request, "encyclopedia/results.html", {
                    "form": searchInput,
                    "matched_entries": matched_entries,
                    "search_query": search_query
                })

    return HttpResponseRedirect(reverse("wiki:index"))


def results(request):
    return render(request, "encyclopedia/results.html", {

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


def new_page(request):
    newPageInput = NewPageInput()
    return render(request, "encyclopedia/newpage.html",
                  {
                      "form": searchInput,
                      "new_page_input": newPageInput
                  })