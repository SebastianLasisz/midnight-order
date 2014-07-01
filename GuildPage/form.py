from django import forms


class ContactForm(forms.Form):
    subject = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'subject'}),
        required=True)
    message = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'message'}),
        required=True)
    sender = forms.EmailField(
        widget=forms.TextInput(attrs={'placeholder': 'email'}),
        required=True)
    cc_myself = forms.BooleanField(required=False)

    def clean(self):
        cleaned_data = self.cleaned_data
        f = cleaned_data.get('subject')
        if f == "":
            raise forms.ValidationError("Did you just enter more than 10?")
            return cleaned_data # Never forget this otherwise you will end up