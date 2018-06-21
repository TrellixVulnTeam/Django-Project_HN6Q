from django.contrib.auth import get_user_model
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import CreateView, DetailView, View
from restaurants.models import RestaurantLocation
from menus.models import Item
from .forms import RegisterForm
from .models import Profile

User = get_user_model()

def activate_user_view(request, code=None, *args, **kwargs):
    if code:
        act_profile_qs = Profile.objects.filter(activation_key=code)
        if act_profile_qs.exists() and act_profile_qs.count() == 1:
            act_obj = act_profile_qs.first()
            if not act_obj.activated:
                user_ = act_obj.user
                user_.is_active = True
                user_.save()
                act_obj.activated=True
                act_obj.activation_key=None
                act_obj.save()
                return redirect("/login")
    return redirect("/login")


class RegisterView(CreateView):
	form_class = RegisterForm
	template_name = 'registration/register.html'
	success_url = '/'

	def dispatch(self, *args, **kwargs):
		if self.request.user.is_authenticated():
			return redirect("/logout")
		return super(RegisterView, self).dispatch(*args, **kwargs)

class ProfileFollowToggle(LoginRequiredMixin, View):
	def post(self, request, *args, **kwargs):
		username_to_toggle = request.POST.get("username")
		profile_, is_following = Profile.objects.toggle_follow(request.user, username_to_toggle)
		print(is_following)
		return redirect(f"/u/{profile_.user.username}/")

class profileDetailView(DetailView):
	queryset = User.objects.filter(is_active = True)
	template_name = 'profiles/user.html'

	def get_object(self):
		username = self.kwargs.get("username")
		if username is None:
			raise Http404
		return get_object_or_404(User, username__iexact = username, is_active=True)

	def get_context_data(self,*args,**kwargs):
		context = super(profileDetailView, self).get_context_data(*args,**kwargs)
		user = context['user']
		is_following = False
		if user.profile in self.request.user.is_following.all():
			is_following = True
		context['is_following']=is_following
		query = self.request.GET.get('q')
		item_exists = Item.objects.filter(user=user).exists()
		qs = RestaurantLocation.objects.filter(owners=user).search(query)
		if item_exists and qs.exists():
			context['locations'] = qs
		return context