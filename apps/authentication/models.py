from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.utils.translation import gettext_lazy as _
from PIL import Image
from hrm.models import Employee


# Create your models here.
class User(AbstractUser):
    class Meta:
        permissions = [
            ("set_password", "Set user password"),
            ("change_password", "Change user password"),]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='default.jpg', upload_to='profile_images', verbose_name=_("avatar"))
    employee = models.ForeignKey(Employee, on_delete=models.RESTRICT, null=True, blank=True)

    class Meta:
        permissions = (("set_profile", "Set user profile"),)

    def __str__(self):
        return self.user

    # resizing images
    def save(self, *args, **kwargs):
        super().save()
        img = Image.open(self.avatar.path)
        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)


class Group(Group):
    Group.add_to_class('description',
        models.CharField(max_length=150, null=True, blank=True, verbose_name=_("Description")))