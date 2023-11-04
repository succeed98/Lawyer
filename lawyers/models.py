from django.db import models

# Create your models here.
from django.contrib.auth.models import PermissionsMixin
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from django.db import models
from ckeditor.fields import RichTextField

class Role(models.Model):
    title=models.CharField(max_length=250)

    def __str__(self):
        return self.title

class LawyerStatus(models.Model):
    title=models.CharField(max_length=250)



    def __str__(self):
        return self.title


class User(AbstractUser):
    avatar = models.ImageField(
        upload_to="avatars/", null=True, blank=True)
    phone = models.CharField(default="", max_length=50)
    team=models.ForeignKey('lawyers.Team',null=True, on_delete=models.SET_NULL) #added team: 13.04.2021

    is_lawyer = models.BooleanField(default=False)
    # is_other_staff = models.BooleanField(default=False)

    @property
    def get_avatar_url(self):
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url
        else:
            return "./static/assets/images/user.png"

    def get_absolute_url(self):
        return reverse("lawyers:user_detail", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("lawyers:user_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse("lawyers:user_delete", kwargs={"pk": self.pk})

    # def __str__(self):
    #     return "{} {}".format(self.first_name, self.last_name)


class Lawyer(models.Model):
    """Model definition for Lawyer."""
    user = models.OneToOneField("User", on_delete=models.CASCADE)
    bar_number = models.IntegerField(unique=True)
    lawyer_status = models.ForeignKey(
        LawyerStatus, null=True, on_delete=models.SET_NULL)
    per_hour_charge = models.FloatField(null=True, blank=True)

    # TODO: Define fields here

    class Meta:
        """Meta definition for Lawyer."""

        verbose_name = 'Lawyer'
        verbose_name_plural = 'Lawyers'
        ordering = ['user']

    def __str__(self):
        """Unicode representation of Lawyer."""
        full_name = "{} {}".format(self.user.first_name, self.user.last_name)
        return full_name


class OtherStaff(models.Model):
    """Model definition for OtherStaff."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role,null=True,on_delete=models.SET_NULL)
    per_hour_charge = models.IntegerField(null=True, blank=True)

    # TODO: Define fields here

    class Meta:
        """Meta definition for OtherStaff."""

        verbose_name = 'Support Staff'
        verbose_name_plural = 'Support Staff'
        ordering = ['user']

    def __str__(self):
        """Unicode representation of OtherStaff."""
        full_name = "{} {}".format(self.user.first_name, self.user.last_name)
        return full_name

    def get_absolute_url(self):
        return reverse("accounts:staff_detail", kwargs={"pk": self.pk})




class Team(models.Model):
    """Model definition for Team."""
    name=models.CharField(max_length=250)
    practice_head=models.ForeignKey(Lawyer,null=True , related_name="practice_head",on_delete=models.SET_NULL)
    team_leader=models.ForeignKey(Lawyer,null=True , related_name="leader",on_delete=models.SET_NULL)
    date_created=models.DateTimeField(auto_now=False,null=True)
    lawyer=models.ManyToManyField(Lawyer)
    support_staff=models.ManyToManyField(OtherStaff)
    description= RichTextField(blank=True,null=True)
    avatar=models.ImageField(null=True,blank=True,upload_to='team_avi/')

    @property
    def get_photo_url(self):
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url
        else:
            return "./static/assets/images/widgets/education.svg"


    class Meta:
        """Meta definition for Team."""

        verbose_name = 'Team'
        verbose_name_plural = 'Teams'
        ordering = ['name']

    def __str__(self):
        """Unicode representation of Team."""
        return self.name


    def get_absolute_url(self):
        return reverse("accounts:team_detail", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("accounts:team_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse("accounts:team_delete", kwargs={"pk": self.pk})


