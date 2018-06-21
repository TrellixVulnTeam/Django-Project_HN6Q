from django.core.exceptions import ValidationError

def validate_even(value):
	if value%2 != 0 :
		raise ValidationError(
			'%(value)s is not a even number',
			params = {'value':value}
		)

categories = ['Mexican', 'Chinese', 'Asian', 'American', 'Whatever']

def validate_category(value):
	print(value.capitalize())
	if not value in categories and not value.capitalize() in categories:
		raise ValidationError(
				'%(value)s is not a valid category',
				params = {'value' : value}
			)