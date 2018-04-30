from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse



User = settings.AUTH_USER_MODEL


class Profile(models.Model):
    user			= models.OneToOneField(User)

    def __str__(self):
	    return self.user.username

    class Meta:
	    verbose_name='Profile'
	    verbose_name_plural='Profiles'
		

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