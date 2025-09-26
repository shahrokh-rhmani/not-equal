from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.query import QuerySet

from .models import Product, Rating
from .views import ProductListView
from .forms import ProductFilterForm, RatingForm

class ProductViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Creating test data
        cls.user = User.objects.create_user(username='testuser', password='12345')
        cls.product1 = Product.objects.create(
            name='Product 1', 
            price=100, 
            is_available=True,

        )
        cls.product2 = Product.objects.create(
            name='Product 2', 
            price=200, 
            is_available=False,

        )
        cls.product3 = Product.objects.create(
            name='Another item', 
            price=150, 
            is_available=True,

        )
        
        # Creating ratings
        Rating.objects.create(
            product=cls.product1,
            user=cls.user,
            score=4,
            comment='Good product'
        )
        Rating.objects.create(
            product=cls.product1,
            user=User.objects.create_user(username='otheruser', password='12345'),
            score=2,
            comment='Not so good'
        )

    def setUp(self):
        self.factory = RequestFactory()

    def test_product_list_view_get_queryset(self): # 1
        # Test queryset for product list without filter
        request = self.factory.get(reverse('product_list'))
        view = ProductListView()
        view.request = request
        
        queryset = view.get_queryset()
        self.assertIsInstance(queryset, QuerySet)
        self.assertEqual(queryset.count(), 3)
        
        # check annotate
        first_product = queryset.first()
        self.assertTrue(hasattr(first_product, 'average_rating'))
        self.assertTrue(hasattr(first_product, 'ratings_count'))

    def test_product_list_view_with_filters(self): # 2
        # test search filter 
        request = self.factory.get(reverse('product_list'), {'search': 'Product'})
        view = ProductListView()
        view.request = request
        
        queryset = view.get_queryset()
        self.assertEqual(queryset.count(), 2)
        
        # test price filter 
        request = self.factory.get(reverse('product_list'), {'min_price': 150, 'max_price': 200})
        view = ProductListView()
        view.request = request
        
        queryset = view.get_queryset()
        self.assertEqual(queryset.count(), 2)
        
        # test inventory filter 
        request = self.factory.get(reverse('product_list'), {'availability': 'available'})
        view = ProductListView()
        view.request = request
        
        queryset = view.get_queryset()
        self.assertEqual(queryset.count(), 2) 

    def test_product_list_view_context_data(self): # 3
        # test the context data passed to the template
        request = self.factory.get(reverse('product_list'))
        response = ProductListView.as_view()(request)
        
        self.assertIn('products', response.context_data)
        self.assertIn('filter_form', response.context_data)
        self.assertIsInstance(response.context_data['filter_form'], ProductFilterForm)

    def test_product_detail_view_get_context_data(self): # 4  
        # Test for logged-in user
        self.client.force_login(self.user)
        response = self.client.get(reverse('product_detail', args=[self.product1.pk]))
        
        self.assertEqual(response.status_code, 200)
        
        # Check presence of all context variables
        context = response.context
        self.assertIn('filter_form', context)
        self.assertIsInstance(context['filter_form'], ProductFilterForm)
        self.assertIn('form', context)
        self.assertIsInstance(context['form'], RatingForm)
        self.assertIn('ratings', context)
        self.assertIn('average_rating', context)
        self.assertIn('ratings_count', context)
        self.assertIn('user_rating', context)
        
        # Check values
        self.assertEqual(context['average_rating'], 3)  # (4+2)/2
        self.assertEqual(context['ratings_count'], 2)
        self.assertEqual(context['ratings'].count(), 2)
        self.assertEqual(context['user_rating'].score, 4)  # Current user's rating
        
        # Check ratings ordering
        self.assertEqual(
            list(context['ratings'].values_list('id', flat=True)),
            list(Rating.objects.filter(product=self.product1)
                .order_by('-created_at').values_list('id', flat=True))
        )
        
        # Test for guest user
        self.client.logout()
        response = self.client.get(reverse('product_detail', args=[self.product1.pk]))
        self.assertIsNone(response.context['user_rating'])
        
        # Test for product without ratings
        response = self.client.get(reverse('product_detail', args=[self.product3.pk]))
        self.assertIsNone(response.context['average_rating'])
        self.assertEqual(response.context['ratings_count'], 0)
        

    def test_product_detail_view_post_rating_authenticated(self): # 5
        # Log in the user
        self.client.login(username='testuser', password='12345')
        
        # send POST request
        response = self.client.post(reverse('product_detail', args=[self.product2.pk]), {
            'submit_rating': '1',
            'score': 5,
            'comment': 'Excellent'
        })
        
        # Verify that the rating was created
        rating_exists = Rating.objects.filter(
            product=self.product2,
            user=self.user
        ).exists()
        self.assertTrue(rating_exists)
        
        # Check redirect to product page
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('product_detail', args=[self.product2.pk]))


    def test_product_detail_view_post_rating_unauthenticated(self): # 6
        # send POST request with client (not logged in)
        response = self.client.post(reverse('product_detail', args=[self.product1.pk]), {
            'submit_rating': '1',
            'score': 5,
            'comment': 'Excellent'
        })
        
        # Verify redirect to login page
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse('login')))


    def test_product_detail_view_update_rating(self): # 7
        # test updating an existing rating
        initial_rating = Rating.objects.create(
            product=self.product3,
            user=self.user,
            score=3,
            comment='Average'
        )
        
        # Log in user with client
        self.client.login(username='testuser', password='12345')
        
        # send POST request with client
        response = self.client.post(reverse('product_detail', args=[self.product3.pk]), {
            'submit_rating': '1',
            'score': 1,
            'comment': 'Changed my mind'
        })
        
        # verify rating update
        updated_rating = Rating.objects.get(pk=initial_rating.pk)
        self.assertEqual(updated_rating.score, 1)
        self.assertEqual(updated_rating.comment, 'Changed my mind')
        
        # verify redirect
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('product_detail', args=[self.product3.pk]))


    def test_product_list_view_pagination(self):
        # Create enough products to test pagination (you already have 3, let's create 2 more)
        Product.objects.create(name='Product 4', price=250, is_available=True)
        Product.objects.create(name='Product 5', price=300, is_available=True)
        
        # Test first page
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(len(response.context['products']), 4)  # paginate_by is 4
        
        # Test second page (should have 1 item)
        response = self.client.get(reverse('product_list') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(len(response.context['products']), 1)

    def test_product_list_view_pagination_with_filters(self):
        # Create additional products (5 total)
        Product.objects.create(name='Filtered Product 1', price=50, is_available=True)
        Product.objects.create(name='Filtered Product 2', price=60, is_available=True)
        Product.objects.create(name='Filtered Product 3', price=70, is_available=True)
        Product.objects.create(name='Filtered Product 4', price=80, is_available=True)
        Product.objects.create(name='Filtered Product 5', price=90, is_available=True)
        
        # Make sure existing product don't interfere by setting their prices outside the range
        self.product1.price = 120
        self.product1.save()
        
        # Apply a filter that will return exactly 5 products
        response = self.client.get(reverse('product_list'), {'min_price': 50, 'max_price': 100})
        
        # First page should have 4 items
        self.assertEqual(len(response.context['products']), 4)
        
        # Second page should have 1 item (5 total - 4 on first page)
        response = self.client.get(reverse('product_list'), {'min_price': 50, 'max_price': 100, 'page': 2})
        self.assertEqual(len(response.context['products']), 1)