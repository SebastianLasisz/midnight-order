from django import forms

from django_summernote.widgets import SummernoteWidget


class NewsForm(forms.Form):
    title = forms.CharField(label="", min_length=3, widget=forms.Textarea(
        attrs={'rows': 1, 'width': '100%', 'placeholder': 'Name of the news'}))
    description = forms.CharField(label="", min_length=3,
                                  widget=SummernoteWidget(
                                      attrs={'width': '300%','height': '490px', 'placeholder': 'Body of the topic'}))