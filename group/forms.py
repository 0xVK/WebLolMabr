from django.forms import ModelForm, ChoiceField, FileField
from group.models import GroupExt, Invite


class CreateGroupForm(ModelForm):

    avatar = FileField(required=False)

    class Meta:
        model = GroupExt
        fields = ['name', 'description', 'avatar', ]


class InviteUserToGroupForm(ModelForm):

    class Meta:
        model = Invite
        fields = ('to_user', )
