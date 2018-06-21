from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from .utils import code_generator
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
# Create your models here.
User = settings.AUTH_USER_MODEL

class ProfileManager(models.Manager):
	def toggle_follow(self, request_user, username_to_toggle):
		
		profile_ = Profile.objects.get(user__username__iexact=username_to_toggle)
		user = request_user
		# print(user)
		is_following = False
		if user in profile_.followers.all():
			profile_.followers.remove(user)
		else:
			profile_.followers.add(user)
			is_following=True
		return profile_, is_following

class Profile(models.Model):
	user     	= models.OneToOneField(User)
	followers	= models.ManyToManyField(User, related_name = 'is_following', blank = True)
	#following	= models.ManyToManyField(User, related_name = 'following', blank = True)
	activation_key = models.CharField(max_length=120, blank=True, null=True)
	activated   = models.BooleanField(default = False)
	timestamp   = models.DateTimeField(auto_now_add = True)
	updated     = models.DateTimeField(auto_now = True)
	objects= ProfileManager()

	def __str__(self):
		if self.user.username:
			return self.user.username
		return self

	def send_activation_email(self):
		if not self.activated:
			self.activation_key = code_generator()
			self.save()
			path_ = reverse('activate', kwargs={"code": self.activation_key})
			subject = 'Activate Account'
			from_email = settings.DEFAULT_FROM_EMAIL
			message = f'Activate your acccount here: {path_}'
			recipient_list = [self.user.email]
			html_message = f'<p>Activate your acccount here: {path_}</p>'
			sent_mail = send_mail(subject,
								 message, 
								 from_email,
								 recipient_list,
								 fail_silently=False,
								 html_message=html_message
							)
			return sent_mail
		pass

def post_save_user_reciever(sender, instance, created, *args, **kwargs):
	if created:
		profile, is_created = Profile.objects.get_or_create(user=instance)
		default_user_profile = Profile.objects.get_or_create(user_id=2)[0]
		default_user_profile.followers.add(instance)
		profile.followers.add(default_user_profile.user)
		# profile.followers.add(3)

post_save.connect(post_save_user_reciever, sender=User)