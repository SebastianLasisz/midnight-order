from django import forms
from captcha.fields import ReCaptchaField


class RegisterForm(forms.Form):
    irl_name = forms.CharField(
        widget=forms.TextInput(attrs={'style': 'width:400px'}),
        required=True)
    age = forms.IntegerField(widget=forms.NumberInput(attrs={'style': 'width:400px'}), required=True)
    country = forms.CharField(
        widget=forms.TextInput(attrs={'style': 'width:400px'}),
        required=True, max_length=5000)
    about_yourself = forms.CharField(
        widget=forms.Textarea(attrs={'style': 'width:400px'}),
        required=True)
    username = forms.CharField(
        widget=forms.TextInput(attrs={'style': 'width:400px'}),
        required=True)
    class_1 = forms.CharField(
        widget=forms.TextInput(attrs={'style': 'width:400px'}),
        required=True)
    spec = forms.CharField(
        widget=forms.TextInput(attrs={'style': 'width:400px'}),
        required=True)
    wol_logs = forms.CharField(
        widget=forms.TextInput(attrs={'style': 'width:400px'}),
        required=False)
    professions = forms.CharField(
        widget=forms.TextInput(attrs={'style': 'width:400px'}),
        required=True)
    previous_guilds = forms.CharField(
        widget=forms.Textarea(attrs={'style': 'width:400px'}),
        required=False)
    contacs = forms.CharField(
        widget=forms.TextInput(attrs={'style': 'width:400px'}),
        required=False)
    reason = forms.CharField(
        widget=forms.Textarea(attrs={'style': 'width:400px'}),
        required=True)
    questions = forms.CharField(
        widget=forms.TextInput(attrs={'style': 'width:400px'}),
        required=False)
    rules = forms.BooleanField(required=True)
    experience = forms.CharField(
        widget=forms.Textarea(attrs={'style': 'width:400px'}),
        required=True)

    def clean(self):
        cleaned_data = self.cleaned_data
        f = cleaned_data.get('irl_name')
        if f == "":
            raise forms.ValidationError("Did you just enter more than 10?")
            return cleaned_data


class RegisterNewUserForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'style': 'width:400px'}),
        required=True)
    email = forms.CharField(
        widget=forms.EmailInput(attrs={'style': 'width:400px'}),
        required=True)
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'style': 'width:400px'}),
        required=True)
    repeat_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'style': 'width:400px'}),
        required=True)
    captcha = ReCaptchaField(attrs={'theme': 'white'})

    def clean(self):
        cleaned_data = self.cleaned_data
        f = cleaned_data.get('captcha')
        if f == "":
            raise forms.ValidationError("Username cannot be empty")
            return cleaned_data


class UserProfileForm(forms.Form):
    avatar = forms.ImageField(required=False)
    signature = forms.CharField(
        widget=forms.TextInput(attrs={'style': 'width:200px'}),
        required=False)
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'style': 'width:100px'}),
        required=False)
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'style': 'width:100px'}),
        required=False)
    repeat_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'style': 'width:100px'}),
        required=False)

    def clean(self):
        cleaned_data = self.cleaned_data
        f = cleaned_data.get('avatar')
        if f == "":
            raise forms.ValidationError("Username cannot be empty")
            return cleaned_data
