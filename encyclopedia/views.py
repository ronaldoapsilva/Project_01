from django.shortcuts import render

from . import util

import re


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def wiki(request, title):
    if title in util.list_entries():
        return render(request, "encyclopedia/wiki.html", {
            "title": re.split(r'\n', util.get_entry(title)),
            "header": title
        })
    else:
        return render(request, "encyclopedia/404.html")
