"""
Forms for the profiles...
"""
from django.contrib.auth.models import User
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.localflavor.us.forms import USZipCodeField, USPhoneNumberField, USStateField, USStateSelect

from swarm.apps.profiles.models import OrganizationProfile

# I put this on all required fields, because it's easier to pick up
# on them with CSS or JavaScript if they have a class of "required"
# in the HTML. Your mileage may vary. If/when Django ticket #3515
# lands in trunk, this will no longer be necessary.
attrs_dict = { 'class': 'am_required' }

class NewOrganizationProfileForm(forms.Form):
    """
    Form for business profiles.
    """
    name = forms.CharField(widget=forms.TextInput(attrs=dict(attrs_dict)),label=_('Name'))
    location_address = forms.CharField(widget=forms.TextInput(attrs=dict(attrs_dict)),label=_('Address'))
    location_city = forms.CharField(widget=forms.TextInput(attrs=dict(attrs_dict)),label=_('City'))
    location_state = USStateField(widget=USStateSelect(attrs=dict(attrs_dict)),label=_('State'))
    location_zip = USZipCodeField(widget=forms.TextInput(attrs=dict(attrs_dict)),label=_('Zip'))
    telephone = USPhoneNumberField(widget=forms.TextInput(attrs=dict(attrs_dict)),label=_('Telephone'))
    website = forms.URLField(widget=forms.TextInput(),label=_('Website'))
    user = forms.CharField()
    
    def clean_user(self):
        try:
            self.cleaned_data['user'] = User.objects.get(id=self.cleaned_data['user'])
        except:
            raise forms.ValidationError(_(u'This user does not exist in our system.'))
        
        return self.cleaned_data['user']

    def save(self):
        new_profile = OrganizationProfile.objects.create_business_profile(name=self.cleaned_data['name'],
                                                                      address=self.cleaned_data['location_address'],
                                                                      city=self.cleaned_data['location_city'],
                                                                      state=self.cleaned_data['location_state'],
                                                                      zip=self.cleaned_data['location_zip'],
                                                                      telephone=self.cleaned_data['telephone'],
                                                                      user=self.cleaned_data['user'],
                                                                      website=self.cleaned_data['website'])
        return new_profile
        
class UpdateOrganizationProfileForm(forms.ModelForm):
    """
    This is built atop the model for the business profile.
    """
    class Meta:
        model = OrganizationProfile
        exclude = ['user','name','type']