"""
Account API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""
import os
import logging
from unittest import TestCase
from tests.factories import AccountFactory
from service.common import status  # HTTP Status Codes
from service.models import db, Account, init_db
from service.routes import app
from service import talisman

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/postgres"
)

BASE_URL = "/accounts"
HTTPS_ENVIRON = {'wsgi.url_scheme': 'https'}


######################################################################
#  T E S T   C A S E S
######################################################################
class TestAccountService(TestCase):
    """Account Service Tests"""

    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        init_db(app)
        # Disable forced HTTPS for testing
        talisman.force_https = False

    @classmethod
    def tearDownClass(cls):
        """Runs once before test suite"""
        pass

    def setUp(self):
        """Runs before each test"""
        db.session.query(Account).delete()  # clean up the last tests
        db.session.commit()

        self.client = app.test_client()

    def tearDown(self):
        """Runs once after each test case"""
        db.session.remove()

    ######################################################################
    #  H E L P E R   M E T H O D S
    ######################################################################

    def _create_accounts(self, count):
        """Factory method to create accounts in bulk"""
        accounts = []
        for _ in range(count):
            account = AccountFactory()
            response = self.client.post(BASE_URL, json=account.serialize())
            self.assertEqual(
                response.status_code,
                status.HTTP_201_CREATED,
                "Could not create test Account",
            )
            new_account = response.get_json()
            account.id = new_account["id"]
            accounts.append(account)
        return accounts

    ######################################################################
    #  A C C O U N T   T E S T   C A S E S
    ######################################################################

    def test_index(self):
        """It should get 200_OK from the Home Page"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_health(self):
        """It should be healthy"""
        resp = self.client.get("/health")
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertEqual(data["status"], "OK")

    def test_create_account(self):
        """It should Create a new Account"""
        account = AccountFactory()
        response = self.client.post(
            BASE_URL,
            json=account.serialize(),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Make sure location header is set
        location = response.headers.get("Location", None)
        self.assertIsNotNone(location)

        # Check the data is correct
        new_account = response.get_json()
        self.assertEqual(new_account["name"], account.name)
        self.assertEqual(new_account["email"], account.email)
        self.assertEqual(new_account["address"], account.address)
        self.assertEqual(new_account["phone_number"], account.phone_number)
        self.assertEqual(new_account["date_joined"], str(account.date_joined))

    def test_bad_request(self):
        """It should not Create an Account when sending the wrong data"""
        response = self.client.post(BASE_URL, json={"name": "not enough data"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unsupported_media_type(self):
        """It should not Create an Account when sending the wrong media type"""
        account = AccountFactory()
        response = self.client.post(
            BASE_URL,
            json=account.serialize(),
            content_type="test/html"
        )
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_read_an_account(self):
        """It should Read an Account that exists"""
        account = AccountFactory()
        account.create()

        # Make a GET request to read the account
        resp = self.client.get(f"/accounts/{account.id}")

        # Assert that the response status code is 200_OK
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        # Get the data from the response
        data = resp.get_json()

        # Assert that the data matches what we created
        self.assertEqual(data["name"], account.name)
        self.assertEqual(data["email"], account.email)
        self.assertEqual(data["address"], account.address)

    def test_account_not_found(self):
        """It should return 404 when reading a non-existent account"""
        # Make a GET request with a non-existent account ID
        resp = self.client.get("/accounts/0")

        # Assert that the response status code is 404_NOT_FOUND
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_account(self):
        """It should Update an existing Account"""
        # Create an account first
        account = AccountFactory()
        account.create()

        # Update the account data
        new_data = account.serialize()
        new_data["phone_number"] = "999-888-7777"

        # Make a PUT request to update the account
        resp = self.client.put(
            f"/accounts/{account.id}",
            json=new_data,
            content_type="application/json"
        )

        # Assert that the response status code is 200_OK
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        # Get the updated data from the response
        updated_data = resp.get_json()

        # Assert that the phone number was updated
        self.assertEqual(updated_data["phone_number"], "999-888-7777")

    def test_update_account_not_found(self):
        """It should return 404 when updating a non-existent account"""
        # Create some data
        fake_account = AccountFactory()
        data = fake_account.serialize()

        # Make a PUT request with a non-existent account ID
        resp = self.client.put(
            "/accounts/0",
            json=data,
            content_type="application/json"
        )

        # Assert that the response status code is 404_NOT_FOUND
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_account(self):
        """It should Delete an Account"""
        # Create an account first
        account = AccountFactory()
        account.create()

        # Make a DELETE request
        resp = self.client.delete(f"/accounts/{account.id}")

        # Assert that the response status code is 204_NO_CONTENT
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

        # Try to read the deleted account - should return 404
        resp = self.client.get(f"/accounts/{account.id}")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_accounts(self):
        """It should List all Accounts"""
        # Create multiple accounts
        self._create_accounts(5)

        # Make a GET request to list all accounts
        resp = self.client.get("/accounts")

        # Assert that the response status code is 200_OK
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        # Get the data from the response
        data = resp.get_json()

        # Assert that we got 5 accounts back
        self.assertEqual(len(data), 5)

    def test_list_empty_accounts(self):
        """It should return an empty list when there are no accounts"""
        # Make a GET request to list all accounts (should be empty)
        resp = self.client.get("/accounts")

        # Assert that the response status code is 200_OK
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        # Get the data from the response
        data = resp.get_json()

        # Assert that we got an empty list
        self.assertEqual(data, [])

    def test_security_headers(self):
        """It should return security headers when using HTTPS"""
        resp = self.client.get("/", environ_overrides=HTTPS_ENVIRON)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        # Check for security headers
        self.assertEqual(resp.headers.get('X-Frame-Options'), 'SAMEORIGIN')
        self.assertEqual(resp.headers.get('X-Content-Type-Options'), 'nosniff')
        self.assertEqual(resp.headers.get('Content-Security-Policy'), "default-src 'self'; object-src 'none'")
        self.assertEqual(resp.headers.get('Referrer-Policy'), 'strict-origin-when-cross-origin')

    
    def test_cors_headers(self):
        """It should return CORS headers when using HTTPS"""
        resp = self.client.get("/", environ_overrides=HTTPS_ENVIRON)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        
        # Check for CORS header
        self.assertEqual(resp.headers.get('Access-Control-Allow-Origin'), '*')
