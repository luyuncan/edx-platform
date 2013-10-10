from django.shortcuts import redirect
from django.core.urlresolvers import reverse

class UserStandingMiddleware(object):
	"""
	Checks a user's standing on request. Deletes their session if the user's
	status is 'disabled'.
	"""
	def process_request(self, request):
		student = request.user
		if student.standing.account_status == u'account_disabled':
			request.session.flush()
			return redirect(reverse('login'))