from django.test import TestCase
from django.urls import reverse
from catalog.models import Author
from catalog.constants import (
    MAX_AUTHOR_PAGINATE,
    MIN_AUTHOR_PAGINATE,
    AUTHOR_TEST_COUNT
)

class AuthorListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_authors = AUTHOR_TEST_COUNT
        for author_id in range(number_of_authors):
            Author.objects.create(
                first_name=f'Christian {author_id}',
                last_name=f'Surname {author_id}',
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/catalog/authors/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/author_list.html')

    def test_pagination_is_ten(self):
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('is_paginated', response.context)
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(len(response.context['author_list']), MAX_AUTHOR_PAGINATE)

    def test_lists_all_authors(self):
        response = self.client.get(reverse('authors') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertIn('is_paginated', response.context)
        self.assertTrue(response.context['is_paginated'])

        remaining_authors = AUTHOR_TEST_COUNT - MAX_AUTHOR_PAGINATE
        expected_count = (
            MAX_AUTHOR_PAGINATE if remaining_authors > MAX_AUTHOR_PAGINATE
            else remaining_authors if remaining_authors > MIN_AUTHOR_PAGINATE
            else MIN_AUTHOR_PAGINATE
        )

        self.assertEqual(len(response.context['author_list']), expected_count)

