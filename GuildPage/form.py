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