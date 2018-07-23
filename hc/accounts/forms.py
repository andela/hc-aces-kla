from django import forms


class LowercaseEmailField(forms.EmailField):

    def clean(self, value):
        value = super(LowercaseEmailField, self).clean(value)
        return value.lower()


class EmailPasswordForm(forms.Form):
    email = LowercaseEmailField()
    password = forms.CharField(required=False)


class ReportSettingsForm(forms.Form):
    reports_allowed = forms.BooleanField(required=False)
    report_frequency = forms.CharField(required=False)


class SetPasswordForm(forms.Form):
    password = forms.CharField()


class InviteTeamMemberForm(forms.Form):
    email = LowercaseEmailField()


class RemoveTeamMemberForm(forms.Form):
    email = LowercaseEmailField()


class AssignChecksForm(forms.Form):
    email = LowercaseEmailField()
    check_code = forms.UUIDField(required=False)
    priority = forms.IntegerField(min_value=0, max_value=5)


class UnAssignChecksForm(forms.Form):
    email = LowercaseEmailField()
    check_code = forms.UUIDField(required=False)


class TeamNameForm(forms.Form):
    team_name = forms.CharField(max_length=200, required=True)
