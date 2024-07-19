from django.forms import ModelForm, TextInput, HiddenInput, Textarea
from django.forms import inlineformset_factory
from .models.basic import VendTable, VendAddress, VendContact
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


class VendAddressForm(ModelForm):
    class Meta:
        model = VendAddress
        fields = ['vendtable',"name",'is_primary',"addresstype","address",'zipcode','city','state','countryregion']

    def clean_is_primary(self):
        vendtable_id = self.cleaned_data["vendtable"]
        is_primary = self.cleaned_data["is_primary"]

        if is_primary:
            if VendAddress.objects.filter(vendtable=vendtable_id,is_primary=True).count():
                raise ValidationError(_("Only one primary address is allowed per address book record."))

        # Always return a value to use as the new cleaned data, even if
        # this method didn't change it.
        return is_primary


class VendContactForm(ModelForm):
    class Meta:
        model = VendContact
        fields = ['vendtable',"name",'is_primary',"telephone","telephoneext",'teleFax','mobilephone','email']

    def clean_is_primary(self):
        vendtable_id = self.cleaned_data["vendtable"]
        is_primary = self.cleaned_data["is_primary"]

        if is_primary:
            if VendContact.objects.filter(vendtable=vendtable_id,is_primary=True).count():
                raise ValidationError(_("Only one primary contact is allowed per contact."))

        # Always return a value to use as the new cleaned data, even if
        # this method didn't change it.
        return is_primary
