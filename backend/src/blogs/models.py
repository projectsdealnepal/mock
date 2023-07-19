from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

class UserInquiry(models.Model):

    first_name = models.CharField(_("first name"), max_length=60)
    last_name = models.CharField(_("last name"), max_length=60)
    email = models.CharField(_("email"), max_length=60)
    message = models.TextField(_("message"))
    received_date = models.DateTimeField(_("inquiry received date"), auto_now_add=True)
    

    class Meta:
        verbose_name = _("user inquiry")
        verbose_name_plural = _("user inquiries")

    def __str__(self):
        return self.email


class EmailTemplate(models.Model):
    template_name = models.CharField(_("template name"), max_length=120)
    email_subject = models.CharField(_("subject"), max_length=120)
    email_content = models.TextField(_("email content"))
    created_date = models.DateField(_("created date"),  auto_now_add=True)
    updated_date = models.DateTimeField(_("updated date"), auto_now=True, auto_now_add=False)

    class Meta:
        verbose_name = _("email template")
        verbose_name_plural = _("email templates")

    def __str__(self):
        return self.template_name
    
class EmailHistory(models.Model):
    template_name = models.CharField(_("template name"), max_length=120)
    email_subject = models.CharField(_("subject"), max_length=120)
    email_content = models.TextField(_("email content"))
    sent_to = models.CharField(_("email sent to"), max_length=510)
    sent_status = models.CharField(_("email sent status"), max_length=1020)
    sent_date = models.DateField(_("created date"),  auto_now_add=True)
    
    class Meta:
        verbose_name = _("email history")
        verbose_name_plural = _("email histories")

    def __str__(self):
        return self.template_name



