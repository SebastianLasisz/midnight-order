from django import forms


class NewsForm(forms.Form):
    title = forms.CharField(
        widget=forms.TextInput(attrs={'style': 'width:400px'}),
        required=True, max_length=5000)
    description = forms.CharField(
        widget=forms.Textarea(attrs={'style': 'width:400px'}),
        required=True)
    img = forms.CharField(
        widget=forms.TextInput(attrs={'style': 'width:400px'}),
        required=False, max_length=5000)

    def clean(self):
        cleaned_data = self.cleaned_data
        f = cleaned_data.get('description')
        if f == "":
            raise forms.ValidationError("Did you just enter more than 10?")
            return cleaned_data  # Never forget this otherwise you will end up