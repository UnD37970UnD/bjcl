from django import forms

class Searchform(forms.Form):
    search = forms.CharField(required=True)
