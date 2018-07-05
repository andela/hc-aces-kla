from django import forms
from hc.api.models import Channel


class NameTagsForm(forms.Form):
    name = forms.CharField(max_length=100, required=False)
    tags = forms.CharField(max_length=500, required=False)

    def clean_tags(self):
        list_a = []

        for part in self.cleaned_data["tags"].split(" "):
            part = part.strip()
            if part != "":
                list_a.append(part)

        return " ".join(list_a)


class TimeoutForm(forms.Form):
    timeout = forms.IntegerField(min_value=60, max_value=2592000)
    grace = forms.IntegerField(min_value=60, max_value=2592000)

class ShopifyForm(forms.Form):
    name = forms.CharField(max_length=100, required=False)
    api_key = forms.CharField(max_length=100, required=False)
    password = forms.CharField(max_length=100, required=False)
    event = forms.CharField(max_length=100, required=False)
    shop_name = forms.CharField(max_length=100, required=False)

class NagIntervalForm(forms.Form):
    nag_interval = forms.IntegerField(min_value=60, max_value=2592000)


class AddChannelForm(forms.ModelForm):

    class Meta:
        model = Channel
        fields = ['kind', 'value']

    def clean_value(self):
        value = self.cleaned_data["value"]
        return value.strip()


class AddWebhookForm(forms.Form):
    error_css_class = "has-error"

    value_down = forms.URLField(max_length=1000, required=False)
    value_up = forms.URLField(max_length=1000, required=False)

    def get_value(self):
        return "{value_down}\n{value_up}".format(**self.cleaned_data)


class PriorityForm(forms.Form):
    priority = forms.CharField(max_length=20, required=True)
