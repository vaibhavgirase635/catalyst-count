from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Company
from .forms import Add_User_Form

class UserRegistrationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')

    def test_register_user_success(self):
        response = self.client.post(self.register_url, {
            'email': 'test@example.com',
            'username': 'testuser',
            'password1': 'password123',
            'password2': 'password123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_register_user_password_mismatch(self):
        response = self.client.post(self.register_url, {
            'email': 'test2@example.com',
            'username': 'testuser2',
            'password1': 'password123',
            'password2': 'password321'
        })
        self.assertEqual(response.status_code, 302)  # Redirect back to register
        self.assertFalse(User.objects.filter(username='testuser2').exists())

class UserLoginTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_login_user_success(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password1': 'password123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect to home

    def test_login_user_failure(self):
        response = self.client.post(self.login_url, {
            'username': 'wronguser',
            'password1': 'password123'
        }, follow=True)  # Follow the redirect
        self.assertEqual(response.status_code, 200)  # Now should be 200 because we followed the redirect
        self.assertContains(response, "Email or password is incorrect")

class HomeViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.home_url = reverse('home')
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_home_view_authenticated_user(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'myapp/home.html')

    def test_home_file_upload(self):
        self.client.login(username='testuser', password='password123')
        with open(r'media\uploads\test.csv', 'r') as file:
            response = self.client.post(self.home_url, {'file': file})
        self.assertEqual(response.status_code, 200)

class QueryBuilderViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.query_url = reverse('query_builder')
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')

    def test_query_builder_view(self):
        response = self.client.get(self.query_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'myapp/query.html')

class AddUserViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.add_user_url = reverse('add_user')

    def test_add_user_get(self):
        response = self.client.get(self.add_user_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'myapp/add_user.html')

    def test_add_user_post(self):
        response = self.client.post(self.add_user_url, {
            'username': 'newuser12',
            'email': 'newuser@example.com',
            'first_name':'new',
            'last_name':'user',
            'password1': 'geekyshows123@',
            'password2': 'geekyshows123@'
        },follow=True)
        # Print form errors if the user wasn't created
        if not User.objects.filter(username='newuser12').exists():
            print(response.context['form'].errors)
        self.assertEqual(response.status_code, 200)  # Redirect to show_users
        self.assertTrue(User.objects.filter(username='newuser12').exists())

class DeleteUserTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='deleteuser', password='password123')
        self.delete_user_url = reverse('delete_user', args=[self.user.id])

    def test_delete_user(self):
        response = self.client.post(self.delete_user_url)
        self.assertEqual(response.status_code, 302)  # Redirect to show_users
        self.assertFalse(User.objects.filter(username='deleteuser').exists())

class MyTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_login(self):
        # Simulate login
        self.client.login(username='testuser', password='password123')
        
        # Access a protected view
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        # Simulate login
        self.client.login(username='testuser', password='password123')
        
        # Logout the user
        self.client.logout()
        
        # Try to access a protected view
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 302)  # Redirect to login

#testing of models



class CompanyModelTest(TestCase):

    def setUp(self):
        # Create a user for associating with the Company model
        self.user = User.objects.create_user(username='testuser', password='password123')
        # Create a Company instance to be used in tests
        self.company = Company.objects.create(
            user=self.user,
            name="Test Company",
            domain="testcompany.com",
            year_founded=1999,
            industry="Technology",
            size_range="100-500",
            locality="San Francisco, CA",
            country="USA",
            linkedin_url="https://www.linkedin.com/company/testcompany",
            current_employee_estimate=250,
            total_employee_estimate=300,
        )

    def test_company_creation(self):
        """Test that a Company instance can be created and saved"""
        company = self.company
        self.assertTrue(isinstance(company, Company))
        self.assertEqual(company.__str__(), company.name)

    def test_company_fields(self):
        """Test the fields of the Company model"""
        company = self.company
        self.assertEqual(company.name, "Test Company")
        self.assertEqual(company.domain, "testcompany.com")
        self.assertEqual(company.year_founded, 1999)
        self.assertEqual(company.industry, "Technology")
        self.assertEqual(company.size_range, "100-500")
        self.assertEqual(company.locality, "San Francisco, CA")
        self.assertEqual(company.country, "USA")
        self.assertEqual(company.linkedin_url, "https://www.linkedin.com/company/testcompany")
        self.assertEqual(company.current_employee_estimate, 250)
        self.assertEqual(company.total_employee_estimate, 300)

    def test_company_default_values(self):
        """Test default and optional field values"""
        company = Company.objects.create(
            user=self.user,
            name="Another Company",
            domain="anothercompany.com",
            year_founded=2000,
            industry="Finance"
        )
        self.assertEqual(company.size_range, None)
        self.assertEqual(company.locality, None)
        self.assertEqual(company.country, None)
        self.assertEqual(company.linkedin_url, None)
        self.assertEqual(company.current_employee_estimate, None)
        self.assertEqual(company.total_employee_estimate, None)

    def test_company_unique_constraints(self):
        """Test that name and domain fields are unique"""
        with self.assertRaises(Exception):
            Company.objects.create(
                user=self.user,
                name="Test Company",  
                domain="testcompany.com",  # Same domain as in setUp
                year_founded=2001,
                industry="Retail"
            )

# testing of forms

class AddUserFormTest(TestCase):

    def test_add_user_form_valid_data(self):
        """Test form is valid with correct data"""
        form = Add_User_Form(data={
            'username': 'newuser',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'newuser@example.com',
            'password1': 'geekyshows@123',
            'password2': 'geekyshows@123',
        })
        self.assertTrue(form.is_valid())

    def test_add_user_form_invalid_data(self):
        """Test form is invalid with incorrect data"""
        form = Add_User_Form(data={
            'username': 'newuser',
            'first_name': '',
            'last_name': 'Doe',
            'email': 'newuser@example.com',
            'password1': 'password123',
            'password2': 'differentpassword',
        })
        print(form.errors)
        self.assertFalse(form.is_valid())
        
        self.assertIn('password2', form.errors)  # Check that password confirmation failed

    def test_add_user_form_existing_username(self):
        """Test form is invalid if the username already exists"""
        User.objects.create_user(username='newuser', password='password123')
        form = Add_User_Form(data={
            'username': 'newuser',  # Duplicate username
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'newuser@example.com',
            'password1': 'password123',
            'password2': 'password123',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)

    def test_add_user_form_password_mismatch(self):
        """Test form is invalid if passwords don't match"""
        form = Add_User_Form(data={
            'username': 'newuser',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'newuser@example.com',
            'password1': 'password123',
            'password2': 'differentpassword',  # Mismatched passwords
        })
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_add_user_form_invalid_email(self):
        """Test form is invalid if the email is not correctly formatted"""
        form = Add_User_Form(data={
            'username': 'newuser',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'invalid-email',  # Invalid email format
            'password1': 'password123',
            'password2': 'password123',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)