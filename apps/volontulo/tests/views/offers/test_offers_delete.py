# -*- coding: utf-8 -*-

u"""
.. module:: test_offers_delete
"""

from django.contrib.auth.models import User
from django.test import Client
from django.test import TestCase

from apps.volontulo.models import (
    Offer, Organization, UserProfile
)


class TestOfferDelete(TestCase):
    """Class responsible for testing offers deletion."""

    @classmethod
    def setUpTestData(cls):
        u"""Set up data for all tests."""
        cls.organization = Organization.objects.create(
            name='',
            address='',
            description='',
        )

        common_offer_data = {
            'organization': cls.organization,
            'description': '',
            'requirements': '',
            'time_commitment': '',
            'benefits': '',
            'location': '',
            'title': 'volontulo offer',
            'time_period': '',
            'started_at': '2105-10-24 09:10:11',
            'finished_at': '2105-11-28 12:13:14',
            'offer_status': 'unpublished',
            'recruitment_status': 'closed',
            'action_status': 'ongoing',
        }

        cls.inactive_offer = Offer.objects.create(
            status_old='NEW',
            **common_offer_data
        )

        cls.active_offer = Offer.objects.create(
            status_old='ACTIVE',
            **common_offer_data
        )

        volunteer_user = User.objects.create_user(
            'volunteer@example.com',
            'volunteer@example.com',
            '123volunteer'
        )

        cls.volunteer = UserProfile(user=volunteer_user)
        cls.volunteer.save()

        organization_user = User.objects.create_user(
            'cls.organization@example.com',
            'cls.organization@example.com',
            '123org'
        )

        cls.organization_profile = UserProfile(
            user=organization_user,
        )
        cls.organization_profile.save()
        # pylint: disable=no-member
        cls.organization_profile.organizations.add(cls.organization)

        admin_user = User.objects.create_user(
            'admin@example.com',
            'admin@example.com',
            '123admin'
        )

        cls.admin = UserProfile(
            user=admin_user,
            is_administrator=True,
        )
        cls.admin.save()

    def setUp(self):
        u"""Set up each test."""
        self.client = Client()

    # pylint: disable=invalid-name
    def test_offer_deletion_for_anonymous_user(self):
        """Test deletion for anonymous users"""
        response = self.client.get('/offers/delete/{}'
                                   .format(self.inactive_offer.id))
        self.assertEqual(response.status_code, 403)

    # pylint: disable=invalid-name
    def test_offer_deletion_for_volunteer(self):
        u"""Test deletion for account of volunteer."""
        self.client.post('/login', {
            'email': 'volunteer@example.com',
            'password': '123volunteer',
        })
        response = self.client.get('/offers/delete/{}'
                                   .format(self.inactive_offer.id))
        self.assertEqual(response.status_code, 403)

    # pylint: disable=invalid-name
    def test_offer_deletion_for_organization(self):
        u"""Test deletion for account of organization."""
        self.client.post('/login', {
            'email': 'organization@example.com',
            'password': '123org',
        })
        response = self.client.get('/offers/delete/{}'
                                   .format(self.inactive_offer.id))
        self.assertEqual(response.status_code, 403)

    # pylint: disable=invalid-name
    def test_offer_deletion_for_admin(self):
        """Test deletion for account of admin."""
        self.client.post('/login', {
            'email': 'admin@example.com',
            'password': '123admin',
        })
        response = self.client.get('/offers/delete/{}'
                                   .format(self.inactive_offer.id))
        self.assertEqual(response.status_code, 302)
