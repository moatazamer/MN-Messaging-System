from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class SignUpForm(UserCreationForm):

    email = forms.EmailField(max_length=254, help_text='Required. Enter a Valid Email Address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )

class MessageForm(forms.Form):
    receiver = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "To: (Username)"
        }),
        error_messages = {'Invalid':'Invalid Username'}
    )
    content = forms.CharField(widget=forms.Textarea(
        attrs={
            "class": "form-control",
            "placeholder": "Enter your Message!"
        })
    )

    def clean_receiver(self):
        receiver = self.cleaned_data.get('receiver')
        receiver_qs = User.objects.filter(username=receiver)
        if not receiver_qs.exists():
            raise ValidationError(self.fields['receiver'].error_messages['Invalid'])
        return receiver
