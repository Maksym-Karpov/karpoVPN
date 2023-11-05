from django.contrib.auth import (
    authenticate,
    login,
    get_user_model
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views.generic import (
    CreateView,
    DetailView,
    UpdateView,
    RedirectView
)

from .forms import (
    CustomUserCreationForm, UserChangeForm
)
from .mixin import (
    SuccessUrlMixin,
    IsUserAbleEditProfileTestMixin,
    IsUserAbleEditProfileMixin
)


class UserSignUpView(SuccessUrlMixin, CreateView):
    form_class = CustomUserCreationForm
    template_name = 'accounts/registration.html'

    def form_valid(self, form):
        form.save()
        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1']
        )
        login(self.request, user)
        return HttpResponseRedirect(self.get_success_url())


class ProfileDetailView(IsUserAbleEditProfileMixin, DetailView):
    model = get_user_model()
    template_name = 'accounts/profile.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['is_user_able_edit_profile'] = (
            self.is_user_able_edit_profile()
        )
        return context_data


class ProfileEditView(
    LoginRequiredMixin,
    IsUserAbleEditProfileTestMixin,
    UpdateView
):
    template_name = 'accounts/profile_edit.html'
    form_class = UserChangeForm
    model = get_user_model()

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(pk=self.request.user.pk)


class LoginRedirectView(LoginRequiredMixin, SuccessUrlMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        redirect_url = self.get_success_url()
        return redirect_url
