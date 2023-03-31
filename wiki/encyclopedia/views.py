from django.shortcuts import render
from . import util
from django import forms
import random
import markdown2

class newArticleForm(forms.Form):
    title = forms.CharField(label="Title of new article")
    content = forms.CharField(
        label="Content (in markdown)",
        widget=forms.Textarea(attrs={'rows': 5, 'cols': 40}),
    )


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def view_article(request, article):

    if article not in util.list_entries():
        return render(request, "encyclopedia/error.html")

    return render(request, "encyclopedia/article.html", {
        "article_title": article,
        "article_content": markdown2.markdown(util.get_entry(article))
    })

def search(request):
    all_entries = util.list_entries()
    search = request.GET.get("q")

    if search in all_entries:
        return view_article(request, search)

    search_results = []
    for entry in all_entries:
        if search.lower() in entry.lower():
            search_results.append(entry)

    return render(request, "encyclopedia/search.html", {
        "search_results": search_results,
    })

def new(request):

    if request.method == "GET":
        return render(request, "encyclopedia/new.html", {
            "form": newArticleForm()
        })

    form = newArticleForm(request.POST)
    if form.is_valid():
        title = form.cleaned_data["title"]
        content = form.cleaned_data["content"]

        # TODO: Check if article already exists!
        if title in util.list_entries():
            return render(request, "encyclopedia/alreadyexists.html")

        util.save_entry(title, content)
        return view_article(request, title)

def edit(request):

    if request.method == "GET":

        initial_data = {
            "title": request.GET.get("article_title"),
            "content": util.get_entry(request.GET.get("article_title"))
        }

        pre_populated_form = newArticleForm(initial_data)
        pre_populated_form.fields['title'].widget.attrs['readonly'] = True

        return render(request, "encyclopedia/edit.html", {
            "form": pre_populated_form
        })

    form = newArticleForm(request.POST)
    if form.is_valid():
        title = form.cleaned_data["title"]
        content = form.cleaned_data["content"]

        util.save_entry(title, content)
        return view_article(request, title)

def random_article(request):
    random_article = random.choice(util.list_entries())
    return view_article(request, random_article)