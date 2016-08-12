from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import Group, Permission, User
from group.forms import CreateGroupForm, InviteUserToGroupForm
from group.models import GroupExt, Discussion, Invite
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
import datetime


def groups(request):

    all_groups = GroupExt.objects.all()
    invites = Invite.objects.filter(to_user=request.user)

    data = {'all_groups': all_groups, 'invites': invites}
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

    if request.method == 'POST':

        form = InviteUserToGroupForm(request.POST)
        if form.is_valid():
            if form.cleaned_data.get('to_user') != request.user.username:
                u = User.objects.get(username=form.cleaned_data.get('to_user'))
                g = GroupExt.objects.get(id=g_id)

                print('to_user=', form.cleaned_data.get('to_user'), 'req.user=', request.user.username)

                inv = Invite(to_user=u, group=g)
                inv.save()

                return HttpResponseRedirect('/groups/{}'.format(g.id))

    form = InviteUserToGroupForm()

    return render(request, template_name='invite.html', context={'form': form})


def join_to_group(request, g_id, token):

    u = request.user
    g = GroupExt.objects.get(id=g_id)

    if Invite.objects.get(to_user=u, group=g):
        u.groups.add(g)
        u.save()
        Invite.objects.get(to_user=u, group=g).delete()
        return HttpResponseRedirect('/groups/{}'.format(g_id))


