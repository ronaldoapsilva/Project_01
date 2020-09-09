from django import forms
from django.shortcuts import render

from . import util

import re


class SearchForm(forms.Form):
    search = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Search Encyclopedia'}))


def index(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            search = form.cleaned_data["search"]
            return wiki(request, search)
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(),
            "form": SearchForm()
        })
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": SearchForm()
    })


def wiki(request, title):
    try:
        return render(request, "encyclopedia/wiki.html", {
            "title": re.split(r'\n', util.get_entry(title)),
            "header": title,
            "form": SearchForm()
        })
    except:
        return render(request, "encyclopedia/404.html")
