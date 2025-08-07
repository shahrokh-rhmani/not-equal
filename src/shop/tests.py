from django.test import TestCase, Client
from .models import Product

class ListViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        
        # Create test products
        self.product1 = Product.objects.create(name="Product 1", price=900, is_available=True)
        self.product2 = Product.objects.create(name="Product 2", price=1000, is_available=True)
        self.product3 = Product.objects.create(name="Product 3", price=1100, is_available=False)
        self.product4 = Product.objects.create(name="Product 4", price=1000, is_available=False)
        self.product5 = Product.objects.create(name="Product 5", price=800, is_available=True)

    # Test method1 excludes products with price=1000 using exclude()
    def test_method1_excludes_price_1000(self):
        response = self.client.get('/')
        method1_results = response.context['method1']
        
        self.assertEqual(method1_results.count(), 3)
        self.assertFalse(method1_results.filter(price=1000).exists())
        
        self.assertIn(self.product1, method1_results)
        self.assertIn(self.product5, method1_results)
        self.assertNotIn(self.product2, method1_results)
        self.assertNotIn(self.product4, method1_results)

    # Test method2 excludes products with price=1000 using Q objects
    def test_method2_excludes_price_1000_with_q(self):
        response = self.client.get('/')
        method2_results = response.context['method2']
        
        self.assertEqual(method2_results.count(), 3)
        self.assertFalse(method2_results.filter(price=1000).exists())
        
        method1_results = response.context['method1']
        self.assertEqual(set(method1_results), set(method2_results))

    #  Test method3 gets only products with price=1000 using double exclude
    def test_method3_gets_only_price_1000(self):
        response = self.client.get('/')
        method3_results = response.context['method3']
        
        self.assertEqual(method3_results.count(), 2)
        self.assertTrue(all(p.price == 1000 for p in method3_results))
        
        expected_products = {self.product2, self.product4}
        self.assertEqual(set(method3_results), expected_products)

    # Test combined filter: available=True and price!=1000
    def test_combined_filters_available_and_excludes_price_1000(self):
        response = self.client.get('/')
        combined_results = response.context['combined']
        
        self.assertEqual(combined_results.count(), 2)
        
        self.assertIn(self.product1, combined_results)
        self.assertIn(self.product5, combined_results)
        self.assertNotIn(self.product2, combined_results)
        self.assertNotIn(self.product3, combined_results)
        self.assertNotIn(self.product4, combined_results)
        
        self.assertTrue(all(p.is_available for p in combined_results))
        self.assertTrue(all(p.price != 1000 for p in combined_results))

    # Test that correct template is used
    def test_template_used(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'list_view.html')

    # Test that method1 and method2 produce identical results
    def test_method1_and_method2_consistency(self):
        response = self.client.get('/')
        method1 = set(response.context['method1'])
        method2 = set(response.context['method2'])
        self.assertEqual(method1, method2)
        
        combined = set(response.context['combined'])
        self.assertTrue(combined.issubset(method1))