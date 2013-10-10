from student.tests.factories import UserFactory
from student.models import UserStanding
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test.client import Client


class UserStandingTest(TestCase):
    """docstring for UserStandingTests"""

    def setUp(self):
        self.bad_user = UserFactory.create()
        self.good_user = UserFactory.create()
        self.non_staff = UserFactory.create()
        self.admin = UserFactory.create(
            username='admin',
            is_staff=True
        )
        for user in [self.bad_user, self.good_user, self.admin]:
            self.client.login(username=user.username, password=user.password)
            # why is this always returning false?

    def test_disable_account(self):
        response = self.client.post(reverse('disable_account_ajax'), {
            'username': self.bad_user.username,
            'user': self.admin,
            'account_action': 'disable',
        })
        import ipdb; ipdb.set_trace()
        self.assertEqual(UserStanding.objects.get(user=self.bad_user.id).account_status, u'account_disabled')

    def test_disabled_account_403s(self):
        response = self.client.get(reverse('dashboard'), {
            'user': self.bad_user
        })
        self.assertEqual(response.status_code, 403)

    def test_disabled_account_cache(self):
        response = self.client.get(reverse('dashboard'), {
            'user': self.bad_user,
        })
        self.assertEqual(self.client.session.get(self.bad_user), None)

    def test_good_account_cache(self):
        response = self.client.get(reverse('dashboard'), {
            'user': self.good_user,
        })
        # should this be response.client.session?
        self.assertEqual(self.client.session.get(self.good_user), 'logged_in')

    def test_reenable_account(self):
        response = self.client.post(reverse('disable_account_ajax'), {
            'username': self.bad_user.username,
            'user': self.admin,
            'account_action': 'reenable'
        })
        self.assertEqual(UserStanding.objects.get(user=self.bad_user.id).account_status, u'account_enabled')

    def non_staff_cant_access_disable_view(self):
        response = self.client.get(reverse('disable_account'), {
            'username': self.bad_user.username,
            'user': self.good_user,
            'account_action': 'disable'
        })
        self.assertEqual(response.status_code, 404)

    def non_staff_cant_disable_account(self):
        response = self.client.post(reverse('disable_account'), {
            'username': self.good_user.username,
            'user': self.non_staff,
            'account_action': 'disable'
        })
        self.assertEqual(response.status_code, 404)
        self.assertEqual(UserStanding.objects.filter(user=good_user.id).count(), 0)
