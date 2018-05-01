from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save
from django.core.mail import send_mail
from .utils import code_generator



User = settings.AUTH_USER_MODEL


class Profile(models.Model):
	user			= models.OneToOneField(User)
	activated		= models.BooleanField(default=False)
	activation_key  = models.CharField(max_length=120,blank=True,null=True)

	def __str__(self):
	    return self.user.username

	class Meta:
	    verbose_name='Profile'
	    verbose_name_plural='Profiles'

	def send_activation_email(self):
		if not self.activated:
			self.activation_key = code_generator()	
			self.save()
			path_ = reverse('activate', kwargs={"code": self.activation_key})
			subject = 'Activate Account'
			from_email = settings.DEFAULT_FROM_EMAIL
			message = 'Activate your account here: {0}'.format(path_)
			recipient_list = [self.user.email]
			html_message = '<p>Activate your account here: {0}</p>'.format(path_)
			print(html_message)
			# sent_mail = send_mail(
			# 				subject, 
			# 				message, 
			# 				from_email, 
			# 				recipient_list, 
			# 				fail_silently=False, 
			# 				html_message=html_message)
			sent_mail = False
			return sent_mail


def post_save_user_receiver(sender, instance, created, *args, **kwargs):
	if created:
		profile, is_created = Profile.objects.get_or_create(user=instance)


post_save.connect(post_save_user_receiver, sender=User)




class Post(models.Model):
	profile     = models.ForeignKey(Profile, on_delete=models.CASCADE) 
	title       = models.CharField(max_length=120, null=True, blank=True)
	content     = models.TextField(null=False, blank=False,default=None)
	timestamp   = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.title

	class Meta:
		verbose_name='Post'
		verbose_name_plural='Posts'
		ordering = ['-timestamp']

	def get_absolute_url(self):
		return reverse('custom:post-detail', kwargs={'pk': self.pk})
    


class Comment(models.Model):
	profile         = models.ForeignKey(Profile, on_delete=models.CASCADE) 
	post            = models.ForeignKey(Post)
	content         = models.TextField(verbose_name='Comment', null=False, blank=False,default=None)
	timestamp       = models.DateTimeField(auto_now_add = True)
	
	def __str__(self):
		return self.content[0:50]