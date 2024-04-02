from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMessage
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView, PasswordChangeView
)
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.utils.translation import gettext_lazy as _

from .forms import (
    LoginForm, SignupForm, ResetPasswordForm, ChangePasswordForm, ProfileForm
)
from .tokens import account_activation_token


class LoginFormView(LoginView):
    form_class = LoginForm
    template_name = 'accounts/login.html'
    extra_context = {'title': 'Login'}


class SignupFormView(CreateView):
    form_class = SignupForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('accounts:login')
    extra_context = {'title': 'Sign Up'}

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        # send account activation email
        mail_subject = 'Activate your account'
        message = render_to_string(
            'accounts/account-activation-email.html',
            {
                'user': user,
                'domain': get_current_site(self.request).domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
                'protocol': 'https' if self.request.is_secure() else 'http',
            }
        )
        email = EmailMessage(
            mail_subject,
            message,
            to=[form.cleaned_data.get('email')]
        )

        if email.send():
            messages.success(
                self.request,
                _('An activation email has been sent to your email address')
            )
        else:
            messages.error(
                self.request,
                _('An error occurred while sending the activation '
                  'email make sure you entered a valid email address ')
            )
        return super(SignupFormView, self).form_valid(form)


class SignUpActivation(View):
    @staticmethod
    def get(request, uidb64, token):
        model = get_user_model()
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = model.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, model.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(
                request,
                _('Your account has been activated. You can login now.')
            )
            return redirect('accounts:login')

        messages.error(
            request,
            _('Invalid activation link please try again')
        )
        return redirect('accounts:login')


class ProfileView(LoginRequiredMixin, DetailView):
    model = get_user_model()
    template_name = 'accounts/profile.html'
    extra_context = {'title': 'Profile'}
    context_object_name = 'user'

    def get_object(self, queryset=None):
        return self.request.user


class LogoutUserView(LoginRequiredMixin, LogoutView):
    success_url = reverse_lazy('accounts:login')
    template_name = 'accounts/logout.html'
    extra_context = {'title': 'Logout'}


class PasswordReset(PasswordResetView):
    template_name = 'accounts/password-reset.html'
    form_class = ResetPasswordForm
    email_template_name = 'accounts/password-reset-email.html'
    extra_context = {'title': 'Reset Password'}
    success_url = reverse_lazy('accounts:password-reset-done')


class PasswordResetDone(PasswordResetDoneView):
    template_name = 'accounts/password-reset-done.html'
    extra_context = {'title': 'Password Reset Request'}


class PasswordResetConfirmation(PasswordResetConfirmView):
    template_name = 'accounts/password-reset-confirmation.html'
    extra_context = {'title': 'Set New Password'}
    success_url = reverse_lazy('accounts:password-reset-complete')


class PasswordResetComplete(PasswordResetCompleteView):
    template_name = 'accounts/password-reset-complete.html'
    extra_context = {'title': 'Password Reset Complete'}


class PasswordChange(LoginRequiredMixin, PasswordChangeView):
    template_name = 'accounts/password-change.html'
    form_class = ChangePasswordForm
    extra_context = {'title': 'Change Password'}

    def get_success_url(self):
        messages.success(self.request, _('Your password has been changed successfully.'))
        return reverse_lazy('accounts:profile')


class ProfileUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'accounts/account-update.html'
    form_class = ProfileForm
    extra_context = {
        'title': 'Update Profile',
        'subtitle': 'Change your personal information',
    }

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        messages.success(self.request, _(f'Dear "{self.request.user}", your profile has been updated'))
        return reverse_lazy('accounts:profile')


class ProfileDelete(LoginRequiredMixin, DeleteView):
    model = get_user_model()
    template_name = 'accounts/account-delete.html'
    success_url = reverse_lazy('accounts:login')
    extra_context = {'title': 'Delete Account'}

    def get_object(self, queryset=None):
        return self.request.user
