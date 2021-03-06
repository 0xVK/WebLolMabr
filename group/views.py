from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth.models import Group, Permission, User
from group.forms import CreateGroupForm, InviteUserToGroupForm
from group.models import GroupExt, Discussion, Invite
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404
from django.core.exceptions import MultipleObjectsReturned
from guardian.shortcuts import assign_perm
import datetime


@login_required()
def groups(request):

    u = request.user
    p = u.get_all_permissions()


    all_groups = GroupExt.objects.all()
    user_groups = request.user.groups.all()
    # print(user_groups)
    invites = Invite.objects.filter(to_user=request.user)

    data = {'all_groups': all_groups, 'user_groups': user_groups, 'invites': invites}
    return render(request, template_name='groups.html', context=data)


@login_required()
@permission_required('auth.add_group', login_url='/groups/')
def create_group(request):

    if request.method == 'POST':
        print(request.FILES)
        form = CreateGroupForm(request.POST, request.FILES)
        if form.is_valid():
            group_name = form.cleaned_data.get('name')
            group_desc = form.cleaned_data.get('description')
            group_avatar = request.FILES.get('avatar')
            GroupExt(name=group_name, description=group_desc, owner=request.user, avatar=group_avatar).save()

            u = User.objects.get(id=request.user.id)
            gr = GroupExt.objects.get(name=group_name)
            u.groups.add(gr)
            assign_perm('group.group_admin', u, gr)
            assign_perm('group.group_member', u, gr)
            u.save()

            return HttpResponseRedirect ('/groups/{}'.format(gr.id))
    else:

        form = CreateGroupForm()

    return render(request, template_name='create.html', context={'form': form})


def group(request, g_id):

    g = get_object_or_404(GroupExt, id=g_id)
    topics = Discussion.objects.filter(group=g)
    is_admin = request.user == g.owner

    if not request.user.has_perm('group.group_admin', g) or not request.user.has_perm('group.group_member', g):
        return HttpResponseForbidden('no!')

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

    inv_inform = ''

    if request.method == 'POST':

        form = InviteUserToGroupForm(request.POST)
        if form.is_valid():
            to_user = User.objects.get(username=form.cleaned_data.get('to_user'))
            g = GroupExt.objects.get(id=g_id)
            g_members = User.objects.filter(groups=g)

            if to_user.username == request.user.username:  # сам себе
                inv_inform += 'Нононо, себе ти не пригласиш!'
                return render(request, template_name='invite.html', context={'form': form, 'inv_inf': inv_inform})

            if to_user in g_members:  # братіша вже в групі
                inv_inform += 'Нононо, братіша вже в групі!'
                return render(request, template_name='invite.html', context={'form': form, 'inv_inf': inv_inform})

            try:  # вже скинуто
                inv = Invite.objects.get(to_user=to_user, group=g)
                inv_inform += 'Нононо, хватить. Раз скинув і всьо!'
                return render(request, template_name='invite.html', context={'form': form, 'inv_inf': inv_inform})
            except MultipleObjectsReturned:
                inv_inform += 'Нононо, вже в чергі дофіга. Потерпи!'
                return render(request, template_name='invite.html', context={'form': form, 'inv_inf': inv_inform})

            except Invite.DoesNotExist:
                inv = Invite.objects.create(to_user=to_user, group=g)
                inv.save()
                inv_inform += 'Найс, відправлено!!'
                return render(request, template_name='invite.html', context={'form': form, 'inv_inf': inv_inform})

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

    g = GroupExt.objects.get(id=g_id)
    if not g.owner == request.user:
        request.user.groups.remove(g_id)
    return HttpResponseRedirect('/groups/')


