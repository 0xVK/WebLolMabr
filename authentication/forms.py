from django.forms import ImageField, CharField, ModelForm, TextInput
from authentication.models import Profile
from django import forms


class ProfileEditForm(ModelForm):

    first_name = forms.CharField()
    last_name = forms.CharField()
    status = forms.CharField()
    email = forms.EmailField()
    photo = forms.ImageField()
    about = forms.Textarea()
    is_extend = forms.BooleanField()

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'status', 'email', 'photo', 'about', 'is_extend']

