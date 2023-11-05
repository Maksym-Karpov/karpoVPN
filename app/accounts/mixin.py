from django.contrib.auth.mixins import UserPassesTestMixin


class IsUserAbleEditProfileMixin:
    def is_user_able_edit_profile(self):
        return self.request.user.pk == self.kwargs['pk']


class IsUserAbleEditProfileTestMixin(
    IsUserAbleEditProfileMixin,
    UserPassesTestMixin
):
    def test_func(self):
        return self.is_user_able_edit_profile()


class SuccessUrlMixin:
    def get_success_url(self):
        from django.urls import reverse_lazy
        return reverse_lazy('profile', args=(str(self.request.user.pk),))
