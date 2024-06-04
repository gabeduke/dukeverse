from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth.models import User
from allauth.account.utils import user_email
from allauth.account.models import EmailAddress

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        # Invoked just after a user successfully authenticates via a social provider,
        # but before the login is actually processed (and before the pre_social_login
        # signal is emitted).
        # We'll use this hook to connect an existing user with a social account.

        # Ignore if user is already logged in
        if request.user.is_authenticated:
            return

        # If a user with this email address already exists, connect the social account
        email = sociallogin.account.extra_data.get('email', '').lower()
        if email:
            try:
                user = User.objects.get(email=email)
                sociallogin.connect(request, user)
            except User.DoesNotExist:
                pass

    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form=form)
        if form:
            user_email(request, user)
            email_address = EmailAddress.objects.get_for_user(user, email=user.email)
            if email_address and not email_address.verified:
                email_address.verified = True
                email_address.save()
        return user
