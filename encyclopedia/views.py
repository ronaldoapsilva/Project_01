from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
import markdown2
from . import util

import re


class NewPageForm(forms.Form):
    title = forms.CharField(label="Entry title", widget=forms.TextInput(
        attrs={'class': 'form-control col-md-8 col-lg-8'}))
    content = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control col-md-8 col-lg-8', 'rows': 10}))
    edit = forms.BooleanField(
        initial=False, widget=forms.HiddenInput(), required=False)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def wiki(request, title):
    content = util.get_entry(title)
    if content is None:
        return render(request, "encyclopedia/404.html")
    else:
        return render(request, "encyclopedia/wiki.html", {
            "title": title,
            "content": markdown2.markdown(content)
        })


def search(request):
    value = request.GET.get('q', '')
    if(util.get_entry(value) is not None):
        return HttpResponseRedirect(reverse("wiki", kwargs={'title': value}))
    else:
        subStringEntries = []
        for entry in util.list_entries():
            if value.upper() in entry.upper():
                subStringEntries.append(entry)

        return render(request, "encyclopedia/index.html", {
            "entries": subStringEntries,
            "search": True,
            "value": value
        })


def new_page(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if util.get_entry(title) is None:
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("wiki", kwargs={'title': title}))
            else:
                return render(request, "encyclopedia/New_Page.html", {
                    "existing": True,
                    "title": title
                })
    else:
        return render(request, "encyclopedia/New_Page.html", {
            "form": NewPageForm()
        })
