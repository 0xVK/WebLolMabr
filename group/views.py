from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import Group, Permission, User
from group.forms import CreateGroupForm, InviteUserToGroupForm
from group.models import GroupExt, Discussion, Invite
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.core.exceptions import MultipleObjectsReturned
import datetime


def groups(request):

    all_groups = GroupExt.objects.all()
    user_groups = request.user.groups.all()
    # print(user_groups)
    invites = Invite.objects.filter(to_user=request.user)

    data = {'all_groups': all_groups, 'user_groups': user_groups, 'invites': invites}
    return render(request, template_name='groups.html', context=data)


@login_required()
def create_group(request):

    if request.method == 'POST':
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            desc = form.cleaned_data.get('description')
            g = GroupExt(name=name, description=desc, owner=request.user)
            g.save()
            gr = GroupExt.objects.get(name=name)
            u = User.objects.get(id=request.user.id)
            u.groups.add(gr)
            u.save()

            return HttpResponseRedirect ('/groups/{}'.format(gr.id))
    else:

        form = CreateGroupForm()

    return render(request, template_name='create.html', context={'form': form})


def group(request, g_id):

    g = get_object_or_404(GroupExt, id=g_id)
    topics = Discussion.objects.filter(group=g)
    is_admin = request.user == g.owner

    data = {'g': g, 'dis': topics, 'is_admin': is_admin}
    return render(request, template_name='group.html', context=data)


def new_topic(request, g_id):

    if request.method == 'POST':
        g = GroupExt.objects.get(id=g_id)
        topic = Discussion()
        topic.title = request.POST.get('title')
        topic.text = request.POST.get('text')
        topic.author = request.user
        topic.group = g
        topic.save()

        return HttpResponseRedirect('/groups/{}/{}'.format(g_id, topic.slug))

    else:

        return render(request, template_name='new_discussion.html')


def topic(request, g_id, slug):

    g = GroupExt.objects.get(id=g_id)
    t = Discussion.objects.get(group=g, slug=slug)

    return render(request, template_name='topic.html', context={'topic': t})


def members(request, g_id):

    g = GroupExt.objects.get(id=g_id)
    mem = User.objects.filter(groups=g)

    return render(request, template_name='members.html', context={'members': mem})


def del_group(request, g_id):

    g = GroupExt.objects.get(id=g_id)
    if request.user == g.owner:
        g.delete()
        return HttpResponseRedirect('/groups')
    else:
        return HttpResponseRedirect('/groups/{}'.format(g_id))


@login_required()
def invite_to_group(request, g_id):

    inv_inf = ''

    if request.method == 'POST':

        form = InviteUserToGroupForm(request.POST)
        if form.is_valid():
            to_user = User.objects.get(username=form.cleaned_data.get('to_user'))
            g = GroupExt.objects.get(id=g_id)
            mems = User.objects.filter(groups=g)

            if to_user.username == request.user.username:  # сам себе
                inv_inf += 'Нононо, себе ти не пригласиш!'
                return render(request, template_name='invite.html', context={'form': form, 'inv_inf': inv_inf})

            if to_user in mems:  # братіша вже в групі
                inv_inf += 'Нононо, братіша вже в групі!'
                return render(request, template_name='invite.html', context={'form': form, 'inv_inf': inv_inf})

            try:  # вже скинуто
                inv = Invite.objects.get(to_user=to_user, group=g)
                inv_inf += 'Нононо, хватить. Раз скинув і всьо!'
                return render(request, template_name='invite.html', context={'form': form, 'inv_inf': inv_inf})
            except MultipleObjectsReturned:
                inv_inf += 'Нононо, вже в чергі дофіга. Потерпи!'
                return render(request, template_name='invite.html', context={'form': form, 'inv_inf': inv_inf})

            except Invite.DoesNotExist:
                inv = Invite.objects.create(to_user=to_user, group=g)
                inv.save()
                inv_inf += 'Найс, відправлено!!'
                return render(request, template_name='invite.html', context={'form': form, 'inv_inf': inv_inf})

    form = InviteUserToGroupForm()

    return render(request, template_name='invite.html', context={'form': form})


def join_to_group(request, g_id, token):

    u = request.user
    g = GroupExt.objects.get(id=g_id)
    inv = get_object_or_404(Invite, to_user=u, group=g, token=token)

    u.groups.add(g)
    u.save()
    inv.delete()
    return HttpResponseRedirect('/groups/{}'.format(g_id))


def leave_group(request, g_id):
    request.user.groups.remove(g_id)
    return HttpResponseRedirect('/groups/')


