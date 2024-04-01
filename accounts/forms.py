from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.translation import gettext_lazy as _
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Invisible, ReCaptchaV2Checkbox


class LoginForm(AuthenticationForm):
    # captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())
    captcha = ReCaptchaField(widget=ReCaptchaV2Invisible())

    class Meta:
        fields = ('email', 'password', 'captcha')
        model = get_user_model()


class SignupForm(UserCreationForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Invisible())

    class Meta:
        fields = ('email', 'phone', 'password1', 'password2', 'captcha')
        model = get_user_model()

    def clean_email(self):
        if get_user_model().objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError(_('A user with that email already exists.'))
        return self.cleaned_data['email']
