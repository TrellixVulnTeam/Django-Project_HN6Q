from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.core.urlresolvers import reverse
from django.db.models import Q
from .utils import unique_slug_generator
from .validators import validate_category
# Create your models here.

User = settings.AUTH_USER_MODEL

class RestaurantLocationQuerySet(models.query.QuerySet):
	def search(self, query):
		if query:
			return self.filter(
				Q(name__icontains=query)|
				Q(category__icontains=query)|
				Q(location__icontains=query)|
				Q(item__name__icontains=query)|
				Q(item__contents__icontains=query)
			).distinct()
		return self


class RestaurantLocationManager(models.Manager):
	def get_queryset(self):
		return RestaurantLocationQuerySet(self.model, using=self._db)

	def search(self,query):
		return self.get_queryset().filter(name__icontains=query)


class RestaurantLocation(models.Model):
	owners 		= models.ForeignKey(User)
	name 		= models.CharField(max_length = 120)
	location 	= models.CharField(max_length = 120, null = True, blank = True)
	category 	= models.CharField(max_length = 120, null = True, blank = True, validators = [validate_category])
	timestamp 	= models.DateTimeField(auto_now_add = True)
	updated 	= models.DateTimeField(auto_now = True)
	slug 		= models.SlugField(null = True, blank = True)
	objects 	= RestaurantLocationManager()
	def __str__(self):
		return self.name

	def get_absolute_url(self):
		# return f"/restaurants/{self.slug}"
		return reverse('restaurant:detail',kwargs = {'slug' : self.slug})

	@property
	def title(self):
	    return self.name

def rl_pre_save_reciever(sender, instance, *args, **kwargs):
	if not instance.category is None:
		instance.category = instance.category.capitalize()
	if not instance.slug:
		instance.slug = unique_slug_generator(instance)

# def rl_post_save_reciever(sender, instance, created, *args, **kwargs):
# 	print('saved')
# 	print(instance.timestamp)
	
pre_save.connect(rl_pre_save_reciever, sender = RestaurantLocation)
# post_save.connect(rl_post_save_reciever, sender = RestaurantLocation)