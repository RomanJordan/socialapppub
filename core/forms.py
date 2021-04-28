from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, Profile
from django.contrib.auth import get_user_model, authenticate
from django.forms import inlineformset_factory

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Enter Username'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Enter Email'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Enter password'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Repeat your password'})

    class Meta(UserCreationForm):
        model = User
        fields = ('email', 'username', 'gender', 'country', 'password1', 'password2')

    def clean_username(self):
        username = self.cleaned_data['username']
        print(username)
        if ' ' in username:
            raise forms.ValidationError("Username may not contain spaces.")
        if '@' in username or '*' in username or '+' in username or '=' in username or '-' in username \
        or '^' in username or '$' in username or '!' in username or '%' in username:
            raise forms.ValidationError("Username may not contain special characters.")
        return username

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class UserLoginForm(forms.Form):
    email = forms.EmailField(label="Email", widget=forms.TextInput(attrs={'class' : 'input'}))
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'input'}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None
        self.fields['email'].widget.attrs.update({'placeholder': 'Enter Email'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Enter Password'})

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email and password:
            self.user = authenticate(email=email, password=password)

            if self.user is None:
                raise forms.ValidationError("User Does Not Exist.")
            if not self.user.check_password(password):
                raise forms.ValidationError("Passwords do not match.")
            if not self.user.is_active:
                raise forms.ValidationError("User is not Active.")

        # return self.cleaned_data
        return super(UserLoginForm, self).clean(*args, **kwargs)

    def get_user(self):
        return self.user

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'username', 'gender', 'country')

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['facebook_link', 'instagram_link', 'twitter_link', 
                'youtube_link','patreon_link', 'twitch_link', 
                'profile_image',]
        
# CustomLinkFormSet = inlineformset_factory(User, CustomLink, fields=('title','link'),form=ProfileEditForm)       

# class CustomLinkEditForm(forms.ModelForm):
#     class Meta:
#         model = CustomLink
#         fields = ['title', 'link']