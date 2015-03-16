from django import forms

from django_summernote.widgets import SummernoteWidget


class TopicCreateForm(forms.Form):
    topic = forms.CharField(label="", min_length=3, widget=forms.Textarea(
        attrs={'rows': 1, 'width': '100%', 'placeholder': 'Name of the topic'}))
    message = forms.CharField(label="", min_length=3,
                              widget=SummernoteWidget(
                                  attrs={'height': '490px', 'placeholder': 'Body of the topic'}))


class PostCreateForm(forms.Form):
    message = forms.CharField(label="", min_length=3,
                              widget=SummernoteWidget(
                                  attrs={'height': '490px', 'placeholder': 'Body of the topic'}))


class PostEditForm(forms.Form):
    message = forms.CharField(label="", min_length=3,
                              widget=SummernoteWidget(
                                  attrs={'height': '490px', 'placeholder': 'Body of the topic'}))