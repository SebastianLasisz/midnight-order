from django import forms
from django_summernote.widgets import SummernoteInplaceWidget


class TopicCreateForm(forms.Form):
    topic = forms.CharField(label="", min_length=3, widget=forms.Textarea(
        attrs={'rows': 1, 'width': '100%', 'placeholder': 'Name of the topic'}))
    message = forms.CharField(label="", min_length=3,
                              widget=SummernoteInplaceWidget(
                                  attrs={'width': '10%', 'height': '400px', 'placeholder': 'Body of the topic'}))


class PostCreateForm(forms.Form):
    message = forms.CharField(label="", min_length=3,
                              widget=SummernoteInplaceWidget(
                                  attrs={'width': '10%', 'height': '400px', 'placeholder': 'Body of the topic'}))
