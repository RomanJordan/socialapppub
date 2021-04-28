from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, HttpResponseRedirect, request
from .models import User, Profile
from django.views.generic import CreateView, FormView, RedirectView, ListView, DetailView, UpdateView
from .forms import CustomUserCreationForm, ProfileEditForm
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import SingleObjectMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from rest_framework import viewsets
from .serializers import UserSerializer, ProfileSerializer

def index(request):
    return render(request, 'core/index.html')

class RegisterView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'core/register.html'
    success_url = reverse_lazy('login')
    
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        return super().dispatch(self.request, *args, **kwargs)

    def get_success_url(self):
        return self.success_url

    def post(self, request, *args, **kwargs):
        if User.objects.filter(email__iexact=request.POST['email']).exists() or User.objects.filter(username__iexact=request.POST['username']).exists():
            messages.error(request, 'This email or username is already taken')
            return redirect('register')

        user_form = CustomUserCreationForm(data=request.POST)

        if user_form.is_valid():
            user = user_form.save(commit=False)
            password = user_form.cleaned_data.get("password1")
            user.set_password(password)
            user.save()
            messages.success(request, 'Account created')
            return redirect('login')
        else:
            print(user_form.errors)
            return render(request, 'core/register.html', {'form': user_form})

class CanEditMixin(object):
    def get_context_data(self, **kwargs):
        """
        The method populates Context with can_edit var
        """
        # Call the base implementation first to get a context
        context = super(CanEditMixin, self).get_context_data(**kwargs)
        #Update Context with the can_edit
        #Your logic goes here (something like that)
        if self.request.user.slug == self.kwargs['username']:
            context['can_edit']=True
        else:
            context['can_edit']=False
        return context

class ProfileView(DetailView):
    model = Profile
    template_name = 'core/profile.html'
    slug_field = 'user__username'
    slug_url_kwarg = 'username'

    # def self_profile(self):
    #     if request.user.is_authenticated:
    #         return User.objects.filter(username = self.kwargs['username'])
    
    def get_queryset(self):
        return Profile.objects.filter(user__username=self.kwargs['username'])


@login_required
def ProfileEdit(request):
    model = request.user.profile 
   
    if request.method == 'POST':
        edit_form = ProfileEditForm(request.POST, request.FILES, instance=request.user.profile)
        # extras = CustomLinkFormSet(request.POST, instance=request.user)
        # edit_form.fields['facebook_link'].initial = "Test"
        if edit_form.is_valid():
            # m = User.profile.objects.get(request)
            edit_form.save()
            messages.success(request, 'Saved')
            img_obj = edit_form.instance
            return HttpResponseRedirect(reverse('index'))
    else:
        edit_form = ProfileEditForm(instance=User, initial={"facebook_link":request.user.profile.facebook_link, 
                                                            "instagram_link":request.user.profile.instagram_link, 
                                                            "twitter_link":request.user.profile.twitter_link,
                                                            "youtube_link":request.user.profile.youtube_link,
                                                            "patreon_link":request.user.profile.patreon_link,
                                                            "twitch_link":request.user.profile.twitch_link,
                                                            "profile_image":request.user.profile.profile_image})
        # extras = CustomLinkFormSet()
        return render(request, 'core/edit_profile.html', {'form': edit_form})

#
def get_user_profile(request, queryset=None):
    model = User
    template_name = 'core/profile.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    # def self_profile(self):
    #     if request.user.is_authenticated:
    #         return User.objects.filter(username = self.kwargs['username'])

    def get_queryset(self):
        return self.request.user.profile


# Not really working.. might delete this
class UpdateProfile(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileEditForm
    success_url = reverse_lazy('selfprofile')
    template_name = 'core/edit_profile.html'

    # if form_class.is_valid():
    #     form_class.save()

    def get_object(self):
        return self.request.user

def logout_view(request):
    logout(request)
    messages.success(request, 'Logged Out')
    return redirect('index')
    # Redirect to a success page.

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint 
    """
    queryset = User.objects.all().order_by('username')
    serializer_class = UserSerializer

class ProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint 
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

