from django import forms

from captcha.fields import ReCaptchaField


class RegisterForm(forms.Form):
    irl_name = forms.CharField(
        label='What is your real name?',
        widget=forms.TextInput(attrs={'style': 'width:400px'}),
        required=True)
    age = forms.IntegerField(
        label='How old are you?',
        widget=forms.NumberInput(attrs={'style': 'width:400px'}),
        required=True)
    country = forms.CharField(
        label='Where are you from?',
        widget=forms.TextInput(attrs={'style': 'width:400px'}),
        required=True, max_length=5000)
    about_yourself = forms.CharField(
        label='Tell us something about yourself',
        widget=forms.Textarea(attrs={'style': 'width:400px'}),
        required=True)
    username = forms.CharField(
        label='What is your character name?',
        widget=forms.TextInput(attrs={'style': 'width:400px'}),
        required=True)
    class_1 = forms.CharField(
        label='Which class you are playing?',
        widget=forms.TextInput(attrs={'style': 'width:400px'}),
        required=True)
    spec = forms.CharField(
        label='What is your specialisation?',
        widget=forms.TextInput(attrs={'style': 'width:400px'}),
        required=True)
    wol_logs = forms.CharField(
        label='Link to logs (Warcraft Logs / World of Logs)',
        widget=forms.TextInput(attrs={'style': 'width:400px'}),
        required=False)
    professions = forms.CharField(
        label='What are your professions?',
        widget=forms.TextInput(attrs={'style': 'width:400px'}),
        required=True)
    previous_guilds = forms.CharField(
        label='Previous guilds and why you left',
        widget=forms.Textarea(attrs={'style': 'width:400px'}),
        required=False)
    contacs = forms.CharField(
        label='Do you know anyone inside guild?',
        widget=forms.TextInput(attrs={'style': 'width:400px'}),
        required=False)
    reason = forms.CharField(
        label='Why would you like to join us?',
        widget=forms.Textarea(attrs={'style': 'width:400px'}),
        required=True)
    questions = forms.CharField(
        label='Do you have any questions to us?',
        widget=forms.Textarea(attrs={'style': 'width:400px'}),
        required=False)
    rules = forms.BooleanField(
        label='Do you accept guild rules?',
        required=True)
    experience = forms.CharField(
        label='What is your raiding experience?',
        widget=forms.Textarea(attrs={'style': 'width:400px'}),
        required=True)


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


class UserProfileForm(forms.Form):
    avatar = forms.ImageField(required=False)
    signature = forms.CharField(
        widget=forms.Textarea(attrs={'style': 'width:400px; height:100px'}),
        required=False)
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'style': 'width:400px'}),
        required=False)
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'style': 'width:400px'}),
        required=False)
    repeat_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'style': 'width:400px'}),
        required=False)
    style = forms.ChoiceField(
        choices=[(1, "Default"), (2, "Midnight Order")],
        widget=forms.Select(attrs={'style':'width:400px'}))