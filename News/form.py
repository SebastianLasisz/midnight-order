from django import forms

from django_summernote.widgets import SummernoteInplaceWidget,SummernoteWidget


class NewsForm(forms.Form):
    title = forms.CharField(label="", min_length=3, widget=forms.Textarea(
        attrs={'rows': 1, 'width': '100%', 'placeholder': 'Name of the topic'}))
    description = forms.CharField(label="", min_length=3,
                                  widget=SummernoteInplaceWidget(
                                      attrs={'width': '10%', 'height': '400px', 'placeholder': 'Body of the topic'}))

    def clean(self):
        cleaned_data = self.cleaned_data
        f = cleaned_data.get('description')
        if f == "":
            raise forms.ValidationError("Did you just enter more than 10?")
            return cleaned_data  # Never forget this otherwise you will end up