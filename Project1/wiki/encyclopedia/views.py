import re
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django import forms
import secrets

from . import util

import markdown

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title", widget=forms.TextInput(attrs={'class': 'form-control col-md-6 col-lg-6'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control col-md-6 col-lg-6', 'rows': 10}))
    edit_page = forms.BooleanField(initial=False, widget=forms.HiddenInput(), required=False)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    entry_page = util.get_entry(entry)
    if entry_page is None:
        return render(request, "encyclopedia/errorEntry.html", {
            "title_entry": entry.capitalize()
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "entry": markdown.markdown(entry_page),
            "title_entry": entry
        })

def search(request):
    if request.method == 'GET':
        search_entry = request.GET.get('q')
        entries = util.list_entries()

        if(util.get_entry(search_entry) is not None):
            entry_page = util.get_entry(search_entry)
            return HttpResponseRedirect(reverse("entry", kwargs={'entry': search_entry}))
        
        else:
            substringSearch = []
            for entry in util.list_entries():
                if search_entry.upper() in entry.upper():
                    substringSearch.append(entry)

            return render(request, "encyclopedia/index.html", {
                "entries": substringSearch,
                "search": True,
                "search_entry": search_entry
            })

def new_entry(request):
    if request.method == 'POST':
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]

            if(util.get_entry(title) is None or form.cleaned_data["edit_page"] is True):
                util.save_entry(title,description)
                return HttpResponseRedirect(reverse("entry", kwargs={'entry': title}))

            else:
                return render(request, "encyclopedia/new_entry.html", {
                    "form": form,
                    "exists": True,
                    "entry": title
                })
        
        else:
            return render(request, "encyclopedia/new_entry.html", {
                "form": form,
                "exists": False
            })

    else:
        return render(request, "encyclopedia/new_entry.html", {
           "form": NewEntryForm(),
           "exists": False
        })

def edit(request, entry):
    entry_page = util.get_entry(entry)
    if entry_page is None:
        return render(request, "encyclopedia/errorEntry.html", {
            "title_entry": entry.capitalize()
        })
    else:
        form = NewEntryForm()
        form.fields["title"].initial = entry
        form.fields["title"].widget = forms.HiddenInput()
        form.fields["description"].initial = entry_page
        form.fields["edit_page"].initial = True
        return render(request, "encyclopedia/new_entry.html", {
            "form": form,
            "edit_page": form.fields["edit_page"].initial,
            "entry": form.fields["title"].initial
        })

def random(request):
    entries = util.list_entries()
    randomWiki = secrets.choice(entries)
    return HttpResponseRedirect(reverse("entry", kwargs={'entry': randomWiki}))