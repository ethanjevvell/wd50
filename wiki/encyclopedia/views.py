from django.shortcuts import render
from . import util
from django import forms

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
        "article_content": util.get_entry(article)
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
        util.save_entry(title, content)
        return view_article(request, title)

