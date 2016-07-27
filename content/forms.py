# -*- coding: utf-8 -*-

from django import forms
from .models import Article


class ContactForm(forms.Form):

    subject = forms.CharField(max_length=100, label='Предмет')
    message = forms.CharField(widget=forms.Textarea, label='Повідомлення')
    sender = forms.EmailField(label='Ел. скринька')


class AddForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = ['title', 'text', ]
