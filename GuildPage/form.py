from django import forms


class ContactForm(forms.Form):
    subject = forms.CharField(label='Email subject',
                              widget=forms.TextInput(attrs={'placeholder': 'subject', 'style': 'width:400px'}),
                              required=True)
    message = forms.CharField(label='Your message',
                              widget=forms.TextInput(attrs={'placeholder': 'message', 'style': 'width:400px'}),
                              required=True)
    sender = forms.EmailField(label='Your email address',
                              widget=forms.TextInput(attrs={'placeholder': 'email', 'style': 'width:400px'}),
                              required=True)
    cc_myself = forms.BooleanField(label='Carbon copy yourself?', required=False)