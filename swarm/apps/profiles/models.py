import re

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from swarm.apps.base.storage import S3Storage
from swarm.apps.registration.signals import user_registered
from swarm.apps.registration.models import RegistrationProfile

class UserProfile(models.Model):
    """
    This user profile for settings and things specific to user meta.
    """
    TYPE_CHOICES = (
        ('ind','Individual or Household'),
        ('org','Organization'),
    )
    user = models.ForeignKey(User,verbose_name=_('you'),unique=True)
    vanity_name = models.CharField(_('vanity name'),max_length=50,blank=True,null=True,unique=True,help_text=_("First name and last name."))
    user_type = models.CharField(_("i'm joining as"),max_length=10,choices=TYPE_CHOICES,blank=True,null=True,help_text=_("Your role in our community."))
    
    def __unicode__(self):
        return unicode(self.user.first_name)
    
    def get_listings_count(self):
        from swarm.apps.classifieds.models import Listing
        return Listing.objects.filter(company__user__id=self.user.id,status__exact="OPEN").count()
    
    def create_vanity_name(self):
        my_vanity = "%s%s" % (self.user.first_name.lower(), self.user.last_name.lower())
        if not my_vanity:
            my_vanity = "bumblebee"
        my_vanity = re.sub(r'\.|\s|\-|\W','',my_vanity)
        up = UserProfile.objects.filter(vanity_name__startswith=my_vanity).order_by('-id')
        if len(up) != 0 and up[0].id is not self.id:
            match = re.search(r'\d+$',up[0].vanity_name)
            if match and match.group(0):
                old_number = int(match.group(0))
                new_number = old_number + 1
                my_vanity = re.sub(r'\d+$',str(new_number),up[0].vanity_name)
            else:
                new_number = '1'
                my_vanity = my_vanity + new_number
        self.vanity_name = "%s" % my_vanity
        return my_vanity

    def save(self,create_vanity=True,*args,**kwargs):
        if create_vanity:
            self.create_vanity_name()
        super(UserProfile,self).save(*args,**kwargs)

    @staticmethod
    def create_my_profile(sender,**kwargs):
        user = kwargs.get('user')
        user_type = kwargs.get('user_type')
        user_profile,created = UserProfile.objects.get_or_create(user=user)
        if created:
            user_profile.user_type = user_type
            user_profile.save(create_vanity=False)

user_registered.connect(UserProfile.create_my_profile, sender=RegistrationProfile)    

class OrganizationProfile(models.Model):
    """
    The profile of an organization in the system.
    """
    user = models.ForeignKey(User,verbose_name=_('creator'),help_text=_('creator of this company profile'))
    name = models.CharField(_('company name'),max_length=50,blank=False,null=True,help_text=_("e.g. Amigeo"))
    location_city = models.CharField(_('city'),max_length=50,blank=False,null=True,help_text=_("e.g. Berkeley"))
    location_state = models.CharField(_('state'),max_length=2,blank=False,null=True,help_text=_("e.g. CA"))
    location_zip = models.CharField(_('zip'), max_length=10,blank=False,null=True,help_text=_("e.g. 90210"))
    telephone = models.CharField(_('telephone'),max_length=13,blank=False,null=True,help_text=_("e.g. 1-303-555-2432"))
    website = models.URLField(_('website'),verify_exists=True,blank=True,null=True)
    years_in_organization = models.PositiveSmallIntegerField(_('years in organization'),blank=True,null=True)
        
    def __unicode__(self):
        return unicode(self.name)
        
    def create_vanity_name(self):
        if self.name:
            my_vanity = "%s" % self.name.lower()
        else:
            my_vanity = "bumbleorg"
        my_vanity = re.sub(r'\.|\s|\-|\W','',my_vanity)
        up = UserProfile.objects.filter(vanity_name__startswith=my_vanity).order_by('-id')
        if len(up) != 0 and up[0].id is not self.id:
            match = re.search(r'\d+$',up[0].vanity_name)
            if match and match.group(0):
                old_number = int(match.group(0))
                new_number = old_number + 1
                my_vanity = re.sub(r'\d+$',str(new_number),up[0].vanity_name)
            else:
                new_number = '1'
                my_vanity = my_vanity + new_number
        self.vanity_name = "%s" % my_vanity
        return my_vanity

    def save(self,*args,**kwargs):
        self.create_vanity_name()
        super(OrganizationProfile,self).save(*args,**kwargs)

class OrganizationProfileAdmin(models.Model):
    user = models.ForeignKey(User,verbose_name=_('Admin of this company profile'))
    organization = models.ForeignKey(OrganizationProfile)
    
    def __unicode__(self):
        return unicode(self.user.first_name)

class OrganizationProfileMember(models.Model):
    user = models.ForeignKey(User,verbose_name=_('Member of this company profile'))
    organization = models.ForeignKey(OrganizationProfile)
    
    def __unicode__(self):
        return unicode(self.user.first_name)