from django import forms
from django.contrib.auth.models import User
from main.models import News, HighlightedEvents
import re
from django.core.validators import RegexValidator


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat Password',
                                widget=forms.PasswordInput)
    organization_name = forms.CharField(label="Organization name",
                                        widget=forms.TextInput,
                                        required=True)
    ein_number = forms.CharField(label="EIN Number",
                                 validators=[
                                     RegexValidator(
                                         regex='^[1-9]\d?-\d{7}$',
                                         message="Please enter valid EIN Number",
                                     ),
                                 ],
                                 required=True)
    about = forms.CharField(label="About your organization",
                            widget=forms.Textarea,
                            required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ('title', 'status', 'news_details', 'tags')
