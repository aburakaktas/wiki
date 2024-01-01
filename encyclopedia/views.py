from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import markdown2
import random
import re
from . import util
from django import forms


class SearchInput(forms.Form):
    search_query = forms.CharField(label="Search:")


class NewPageInput(forms.Form):
    title = forms.CharField(label="Title:")
    body = forms.CharField(widget=forms.Textarea(attrs={'rows': 10, 'cols': 40, 'width':"100%",}))

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
                return HttpResponseRedirect(f"/wiki/{search_query}")

            # if entry cannot be found, list entries that match as a substring and redirect to search results page
            else:
                all_entries = util.list_entries()

                # list all matched entries
                matched_entries = []
                for entry in all_entries:
                    if search_query in entry.lower():
                        matched_entries.append(entry)
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
        print("article:", article)
        
        print("article title:", article_name)
        return render(request, "encyclopedia/article.html",
                      {"article": markdown2.markdown(article),
                       "article_title": article_name,
                        "form": searchInput,
                       })
    else:
        return HttpResponse("404 not found")


def new_page(request):
    newPageInput = NewPageInput()
    
    if request.method == "POST":
        form = NewPageInput(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            body = form.cleaned_data["body"]

            if (util.get_entry(title)):
                error = "Article already exists, try a different title."
                return render(request, "encyclopedia/newpage.html",
                    {
                        "form": searchInput,
                        "new_page_input": newPageInput,
                        "error": error,
                    })
            util.save_entry(title, body)
            return HttpResponseRedirect(f"/wiki/{title}")
            
    else:
        return render(request, "encyclopedia/newpage.html",
                    {
                        "form": searchInput,
                        "new_page_input": newPageInput
                    })


def edit_article(request, article_name):
    
    if request.method == "POST":
        form = NewPageInput(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            body = form.cleaned_data["body"]
            util.save_entry(title, body)
            return HttpResponseRedirect(f"/wiki/{title}")

    
    else:
        article = util.get_entry(article_name)
        if article:
            edit_data = {'title': article_name, 'body': article}
            edit_form = NewPageInput(initial=edit_data)
            return render(request, 'encyclopedia/edit_page.html', {
                "form": searchInput,
                'edit_form': edit_form,
                'article_title': article_name,
            })
        
def random_page(request):
    all_entries = util.list_entries()
    random_entry_name = random.choice(all_entries)
    random_entry = util.get_entry(random_entry_name)
    return render(request, "encyclopedia/article.html",
                  {"article": markdown2.markdown(random_entry),
                   "article_title": random_entry_name,
                    "form": searchInput,
                   })
