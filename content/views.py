# -*- coding: utf-8 -*-

from django.shortcuts import render, resolve_url, redirect
from django.views.generic import DetailView, ListView, FormView, CreateView
from .models import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect, HttpResponse
from content.forms import ContactForm, AddForm

def log_out(request):

    logout(request)
    return HttpResponseRedirect('/')


class LoginFormView(FormView):

    form_class = AuthenticationForm
    template_name = "login.html"
    success_url = "/"

    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)


def detail_art_view(request, a_id=1):

    article = Article.objects.get(id=a_id)
    comments = Comment.objects.filter(article=a_id)

    is_author = article.author == request.user

    context = {'Article': article, 'com_list': comments, 'is_author': is_author}

    if request.POST.get('comment'):
        new_comment_text = request.POST.get('comment')
        new_comment = Comment(text=new_comment_text, author=request.user, article=article)
        new_comment.save()
    return render(request, 'detail.html', context)


def about_page(request):

    return render(request, template_name='about.html')


class IndexPage(ListView):

    template_name = 'index.html'
    model = Article
    latest = Article.objects.order_by('-pub_date')[:10]
    context_object_name = 'Article'

    def dispatch(self, request, *args, **kwargs):

        self.sort_field = request.GET.get('sort_by')
        return super(IndexPage, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):

        if self.sort_field:
            q = Article.objects.all().order_by(self.sort_field)
            return q[0:10]

        return Article.objects.all()[0:10]


def contact_page(request):

    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            return HttpResponseRedirect('/thanks/')

    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})


def thanks_page(request):

    return HttpResponse("Відправлено! <br> <a href = '/'>На головну</a>")


def add_post(request):

    if request.method == 'POST':
        form = AddForm(request.POST)

        if form.is_valid():
            article_title = form.cleaned_data.get('title')
            article_text = form.cleaned_data.get('text')
            article_author = request.user
            article_rating = 0

            a = Article.objects.create(title=article_title, text=article_text, author=article_author, rating=article_rating)
            a.save()

            return redirect('/post/%d' % a.id)

    else:
        form = AddForm()

    return render(request, template_name='add.html', context={'form': form})


def del_post(request, a_id):

    article = Article.objects.get(id=a_id)
    if request.user == article.author:
        article.delete()

        return redirect('/')

    else:
        return HttpResponse('Nonono!')


def like_post(request, a_id):

    if request.user.is_authenticated:
        article = Article.objects.get(id=a_id)
        article.rating += 1
        article.save()
        return redirect('/post/{}/'.format(a_id))


