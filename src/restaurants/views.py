from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.http import HttpResponse,HttpResponseRedirect
from django.views import View
from django.shortcuts import render,get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView
from .models import RestaurantLocation
from .forms import RestaurantCreateForm,RestaurantLocationCreateForm

class RestaurantListView(LoginRequiredMixin,ListView):
	def get_queryset(self):
		return RestaurantLocation.objects.filter(owners = self.request.user)
		 

class RestaurantDetailView(LoginRequiredMixin,DetailView):
	def get_queryset(self):
		return RestaurantLocation.objects.filter(owners = self.request.user)

class ResetUserPassword(auth_views.PasswordResetView):
	template_name = 'registration/password_reset_form.html'
	form_class = auth_views.PasswordResetForm
	email_template_name = 'registration/password_reset_form.html'
	subject_template_name = 'registration/password_reset_subject.txt'


class CreateRestaurantView(LoginRequiredMixin,CreateView):
	form_class = RestaurantLocationCreateForm
	login_url = '/login/'
	template_name = 'form.html'
	# success_url = '/restaurants/'

	def form_valid(self, form):
		instance = form.save(commit = False)
		instance.owners = self.request.user
		print('\n\nyes arriving\n\n')
		return super(CreateRestaurantView , self).form_valid(form)
	def get_context_data(self, *args,**kwargs):
		context = super(CreateRestaurantView, self).get_context_data(*args,**kwargs)
		context['title'] = 'Add Restaurant'
		return context

class RestaurantUpdateView(LoginRequiredMixin,UpdateView):
	form_class = RestaurantLocationCreateForm
	login_url = '/login/'
	template_name = 'restaurants/detail-update.html'
	# success_url = '/restaurants/'
	def get_context_data(self, *args,**kwargs):
		context = super(RestaurantUpdateView, self).get_context_data(*args,**kwargs)
		name = self.get_object().name;
		context['title'] = f'Update Restaurant: {name}'
		return context
	def get_queryset(self):
		return RestaurantLocation.objects.filter(owners = self.request.user)