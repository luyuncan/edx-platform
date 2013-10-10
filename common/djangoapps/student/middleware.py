from django.http import HttpResponseForbidden
from student.models import UserStanding

class UserStandingMiddleware(object):
	"""
	Checks a user's standing on request. Deletes their session if the user's
	status is 'disabled'.
	"""
	def process_request(self, request):
		user = request.user
		try:
			user_account = UserStanding.objects.get(user=user.id)
			# because user is a unique field in UserStanding, there will either be
			# one or zero user_accounts associated with a UserStanding
		except UserStanding.DoesNotExist:
			pass
		else:
			if user_account.account_status == u'account_disabled':
				request.session.flush()
				return HttpResponseForbidden()
