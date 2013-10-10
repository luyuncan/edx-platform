from student.tests.factories import UserFactory, UserStandingFactory
from student.models import UserStanding
from django.test import TestCase, TransactionTestCase


class UserStandingTest(TestCase):
	"""docstring for UserStandingTests"""

	def setUp(self):
        self.bad_user = UserFactory.create()
        self.good_user = UserFactory.create()
		self.admin = UserFactory.create(
			username = 'admin'
			is_staff = True
		)
		for user in [self.bad_user, self.good_user, self.admin]:
			self.client.login(user.username, user.password)
			session = self.client.session
			session['logged_in'] = "Yep"
			session.save()

	def test_disable_account(self):
		response = self.client.post(reverse('disable_account_ajax'), {
			'username': self.bad_user.username,
			'user': self.admin,
			'account_action': 'disable',
		})
		self.assertEqual(UserStanding.objects.get(user = self.user.id).account_status, u'account_disabled')

	def test_disabled_account_403s(self):
		response = self.client.get('unused_url', {
			'user' = self.bad_user
		})
		self.assertEqual(response.status, 403)

	def test_disabled_account_cache(self):
		response = self.client.get('unused_url', {
			'user' = self.bad_user
		})
		self.assertEqual(response.session.get('logged_in') is None, True)

	def test_reenable_account(self):
		response = self.client.post(reverse('disable_account_ajax'), {
			'username': self.bad_user.username,
			'user': self.admin,
			'account_action': 'reenable'
		})
		self.assertEqual(UserStanding.objects.get(user = self.user.id).account_status, u'account_enabled')

