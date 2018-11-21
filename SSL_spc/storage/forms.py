from django import forms

class PostForm(forms.Form):
    key1 = forms.CharField()
    key2 = forms.CharField()
    schema = forms.CharField()
