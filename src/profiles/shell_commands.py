from django.contrib.auth import get_user_model

User = get_user_model()

random_ = User.objects.last()

#my followers
random.profile.followers.all()

#who i follow
random.is_following.all()