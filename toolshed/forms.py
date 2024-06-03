from django import forms
from django.contrib.auth.models import User

from toolshed.models import Tool


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm password')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class CSVUploadForm(forms.Form):
    csv_file = forms.FileField(label='Select a CSV file')

class UserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm password')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

class UserAssociationForm(forms.Form):
    def __init__(self, *args, **kwargs):
        new_users = kwargs.pop('new_users', [])
        super().__init__(*args, **kwargs)
        for username in new_users:
            self.fields[f'user_{username}'] = forms.ChoiceField(
                choices=[('', '---')] + [(user.id, user.username) for user in User.objects.all()] + [('create_new', 'Create New')],
                label=f'Associate or create user for {username}',
                required=True
            )

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Tool
        fields = []


class AssignForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all(), required=True, label='Assign to User')

    def __init__(self, *args, **kwargs):
        # Pass the request user through kwargs to filter out inappropriate choices.
        super(AssignForm, self).__init__(*args, **kwargs)
        # Define queryset to filter users based on specific criteria (e.g., exclude inactive users).
        self.fields['user'].queryset = User.objects.filter(is_active=True)