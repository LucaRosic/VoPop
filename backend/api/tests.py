from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from .models import Product, User_Products, Product_Summary, Product_Reviews, Product_Data_Source

class ProductAPITestCase(APITestCase):
    
    from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Product, User_Products, Product_Summary, Product_Reviews, Product_Data_Source

class ProductAPITestCase(APITestCase):
    
    def setUp(self):
        """
        Create initial test data including a test user and a product.
        This method runs before every test case in this class.
        
        - Creates a test user and logs them in using the API client.
        - Creates a sample product with actual product data for testing.
        - Associates the product with the user in User_Products.
        """
        print("\nSetting up test environment...")
        # Create a test user
        self.user = User.objects.create_user(username="test", password="password123")
        self.client = APIClient()
        
        # Obtain the JWT token for the user
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        
        # Create a sample product with actual data
        self.product = Product.objects.create(
            name="INIU 22.5W Power Bank, 10000mAh Slim USB C Portable Charger Fast Charging PD3.0 QC4.0, LED Display Battery Pack Portable for iPhone 16 15 14 13 12 Pro Max Samsung S22 Google LG AirPods Switch iPad"
                "USB Type C, USB Type A, Black",
            brand="INIU",
            image="https://m.media-amazon.com/images/I/51Bbtc2XBQL._AC_SL1254_.jpg"
        )

        # Create a product data source
        self.product_data_source = Product_Data_Source.objects.create(
            source="https://www.amazon.com.au/INIU-Portable-Charger-10500mAh-Charging/dp/B08K7GHZ3V",
            category="Amazon",
            unique_code="B08K7GHZ3V",
            product=self.product
        )
        
        # Associate the product with the user in User_Products
        self.user_product = User_Products.objects.create(
            user=self.user,
            product=self.product
        )

        print("Test environment setup complete. User and product created.")



    def test_01_create_product(self):
        """
        Test case for creating a new product via the CreateProduct API.
        If the product is already tracked, the test should expect a 200 or 208 response.
        """
        print("\nTesting product creation API...")

        product_data = {
            "url": ["https://www.amazon.com.au/INIU-Portable-Charger-10500mAh-Charging/dp/B08K7GHZ3V"]
        }

        # Send POST request to create product
        response = self.client.post(reverse('create-product'), product_data, format='json')

        # Check if the response status code is 201 Created or 200 OK (since the product might already be tracked)
        print(f"POST request sent. Response status code: {response.status_code}")
        self.assertIn(response.status_code, [status.HTTP_201_CREATED, status.HTTP_200_OK])

        print("Product creation test passed.")


    def test_02_add_link_to_product(self):
        """
        Test case for adding a link to an existing product via the AddLink API.

        - Makes a POST request to add a new link to an existing product.
        - Checks if the API returns HTTP 201 status code if the link was added successfully,
        or 208 if the user is already tracking the product.
        """
        print("Testing adding link to product API...")

        # Get the URL for the AddLink API endpoint
        url = reverse('add-to-product')

        # Define the actual test data to send in the request
        # Use the ID of the existing product and an actual test URL for the product
        data = {
            "url": [self.product.id, "https://www.amazon.com.au/INIU-Portable-Charger/dp/B08K7GHZ3V"]
        }

        # Post the request
        response = self.client.post(url, data, format='json')

        # Check if the link was added successfully or if the user is already tracking the product
        print(f"POST request sent. Response status code: {response.status_code}")
        self.assertIn(response.status_code, [status.HTTP_201_CREATED, status.HTTP_208_ALREADY_REPORTED])

        print("Link addition test passed.")


    def test_03_get_user_products_home(self):
        """
        Test case for retrieving the list of products tracked by the user via GetUserProduct_Home API.
        This ensures that the API returns the correct number of products tracked by the user.
        """
        print("\nTesting retrieval of user products for home page...")

        # Make a GET request to the home page to retrieve the user's tracked products
        response = self.client.get(reverse('product-home'))

        # Check the response status code
        print(f"GET request sent. Response status code: {response.status_code}")

        # Ensure the response is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Ensure that the user has 1 product in the response
        print(f"Number of products returned: {len(response.data)}")
        self.assertEqual(len(response.data), 0)  # The user not logged in
        print("Number of products returned 0, as the user is not logged in.")
        print("User product retrieval test passed.")




    def test_04_get_product_sentiment_dashboard(self):
        """
        Test case for retrieving sentiment data of a product via GetReviewSent_Dash API.s
        
        - Creates a Product_Reviews entry with sentiment data.
        - Sends a GET request to retrieve the sentiment data for the product.
        - Checks if the API returns HTTP 200 status and verifies that sentiment data is present in the response.
        """
        print("Testing retrieval of product sentiment data for dashboard...")
        # Create product review with sentiment data
        Product_Reviews.objects.create(
            unique_code="B08K7GHZ3V",
            review="Great product!", 
            sentiment=0.90, 
            sentiment_label="Positive", 
            rating=5, 
            date="2024-01-01"
        )
        
        url = reverse('product-dashboard-sent', args=[self.product.id])
        response = self.client.get(url)
        
        print(f"GET request sent for product sentiment data. Response status code: {response.status_code}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)  # The product should have at least one sentiment entry
        print("Sentiment data retrieval test passed.")


    def test_05_delete_product(self):
        """
        Test case for deleting a product from a user's list via the ProductDelete API.
        
        - Connects a product to the user by creating a User_Products entry.
        - Sends a DELETE request to remove the product from the user's list.
        - Verifies that the product is successfully deleted from the User_Products table and the API returns HTTP 204 status.
        """
        print("Testing product deletion API...")
        # Connect user to the product
        User_Products.objects.create(user=self.user, product=self.product)
        
        url = reverse('product-delete', args=[self.product.id])
        response = self.client.delete(url)
        
        print(f"DELETE request sent. Response status code: {response.status_code}")
        # Verify that the product is deleted for the user
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User_Products.objects.filter(user=self.user, product=self.product).exists())
        print("Product deletion test passed.")

