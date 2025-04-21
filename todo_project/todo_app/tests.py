import unittest
from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import TodoItem
import json
from unittest.mock import patch


class TodoItemModelTests(unittest.TestCase):
    """Tests for the TodoItem model using unittest."""
    
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        
        # Create a sample todo item
        self.todo = TodoItem.objects.create(
            user=self.user,
            title='Test Todo',
            description='This is a test todo item',
            status='pending'
        )
    
    def tearDown(self):
        # Clean up test data
        User.objects.all().delete()
        TodoItem.objects.all().delete()
    
    def test_todo_creation(self):
        """Test that a todo item can be created."""
        self.assertEqual(self.todo.title, 'Test Todo')
        self.assertEqual(self.todo.description, 'This is a test todo item')
        self.assertEqual(self.todo.status, 'pending')
        self.assertEqual(self.todo.user, self.user)
    
    def test_todo_str_method(self):
        """Test the string representation of a todo item."""
        self.assertEqual(str(self.todo), 'Test Todo')
    
    def test_status_choices(self):
        """Test that status choices are valid."""
        valid_statuses = ['pending', 'in_progress', 'completed']
        choices = [status[0] for status in TodoItem.STATUS_CHOICES]
        
        for status in valid_statuses:
            self.assertIn(status, choices)


class RegisterViewTests(unittest.TestCase):
    """Tests for the register view using unittest."""
    
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')
        self.todo_list_url = reverse('todo_list')
        
        # Create a test user
        self.user = User.objects.create_user(
            username='existinguser',
            email='existing@example.com',
            password='existingpassword'
        )
    
    def tearDown(self):
        # Clean up test data
        User.objects.all().delete()
    
    def test_register_GET(self):
        """Test GET request to register page."""
        response = self.client.get(self.register_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('register.html', response.templates[0].name)
    
    def test_register_POST_valid_form(self):
        """Test POST request with valid form data."""
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'newpassword123',
            'password2': 'newpassword123'
        }
        
        response = self.client.post(self.register_url, data)
        
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertTrue(User.objects.filter(username='newuser').exists())
    
    def test_register_POST_invalid_form(self):
        """Test POST request with invalid form data."""
        data = {
            'username': 'existinguser',  # Username already exists
            'email': 'new@example.com',
            'password1': 'newpassword123',
            'password2': 'newpassword123'
        }
        
        response = self.client.post(self.register_url, data)
        
        self.assertEqual(response.status_code, 200)  # Stay on same page
        self.assertIn('register.html', response.templates[0].name)
    
    def test_register_redirect_if_authenticated(self):
        """Test that authenticated users are redirected."""
        login_successful = self.client.login(username='existinguser', password='existingpassword')
        self.assertTrue(login_successful)
        
        response = self.client.get(self.register_url)
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.todo_list_url)


class TodoListViewTests(unittest.TestCase):
    """Tests for the todo_list view using unittest."""
    
    def setUp(self):
        self.client = Client()
        self.todo_list_url = reverse('todo_list')
        
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        
        # Create some todo items for the user
        self.todo1 = TodoItem.objects.create(
            user=self.user,
            title='Test Todo 1',
            description='This is test todo 1',
            status='pending'
        )
        
        self.todo2 = TodoItem.objects.create(
            user=self.user,
            title='Test Todo 2',
            description='This is test todo 2',
            status='in_progress'
        )
    
    def tearDown(self):
        # Clean up test data
        User.objects.all().delete()
        TodoItem.objects.all().delete()
    
    def test_todo_list_login_required(self):
        """Test that login is required to access the todo list."""
        response = self.client.get(self.todo_list_url)
        
        # Should redirect to login page
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))
    
    def test_todo_list_GET(self):
        """Test GET request to todo list page."""
        login_successful = self.client.login(username='testuser', password='testpassword')
        self.assertTrue(login_successful)
        
        response = self.client.get(self.todo_list_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('todo_list.html', response.templates[0].name)
        self.assertIn('todos', response.context)
        self.assertIn('form', response.context)
        self.assertEqual(len(response.context['todos']), 2)
    
    def test_todo_list_POST_valid_form(self):
        """Test POST request with valid form data."""
        login_successful = self.client.login(username='testuser', password='testpassword')
        self.assertTrue(login_successful)
        
        data = {
            'title': 'New Todo',
            'description': 'This is a new todo',
            'status': 'pending'
        }
        
        response = self.client.post(self.todo_list_url, data)
        
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertEqual(TodoItem.objects.count(), 3)
        self.assertTrue(TodoItem.objects.filter(title='New Todo').exists())
    
    def test_todo_list_POST_invalid_form(self):
        """Test POST request with invalid form data."""
        login_successful = self.client.login(username='testuser', password='testpassword')
        self.assertTrue(login_successful)
        
        data = {
            'title': '',  # Title is required
            'description': 'This is a new todo',
            'status': 'pending'
        }
        
        response = self.client.post(self.todo_list_url, data)
        
        self.assertEqual(response.status_code, 200)  # Stay on same page
        self.assertEqual(TodoItem.objects.count(), 2)


class EditTodoViewTests(unittest.TestCase):
    """Tests for the edit_todo view using unittest."""
    
    def setUp(self):
        self.client = Client()
        
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        
        # Create another user for testing access control
        self.other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='otherpassword'
        )
        
        # Create a todo item for the test user
        self.todo = TodoItem.objects.create(
            user=self.user,
            title='Test Todo',
            description='This is a test todo',
            status='pending'
        )
        
        self.edit_url = reverse('edit_todo', kwargs={'todo_id': self.todo.id})
    
    def tearDown(self):
        # Clean up test data
        User.objects.all().delete()
        TodoItem.objects.all().delete()
    
    def test_edit_todo_login_required(self):
        """Test that login is required to edit a todo."""
        response = self.client.get(self.edit_url)
        
        # Should redirect to login page
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))
    
    def test_edit_todo_GET(self):
        """Test GET request to edit todo page."""
        login_successful = self.client.login(username='testuser', password='testpassword')
        self.assertTrue(login_successful)
        
        response = self.client.get(self.edit_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('todo_list.html', response.templates[0].name)
        self.assertIn('form', response.context)
        self.assertIn('todo', response.context)
        self.assertTrue(response.context['edit_mode'])
    
    def test_edit_todo_POST_valid_form(self):
        """Test POST request with valid form data."""
        login_successful = self.client.login(username='testuser', password='testpassword')
        self.assertTrue(login_successful)
        
        data = {
            'title': 'Updated Todo',
            'description': 'This is an updated todo',
            'status': 'in_progress'
        }
        
        response = self.client.post(self.edit_url, data)
        
        self.assertEqual(response.status_code, 302)  # Redirect
        
        # Refresh from database
        updated_todo = TodoItem.objects.get(id=self.todo.id)
        self.assertEqual(updated_todo.title, 'Updated Todo')
        self.assertEqual(updated_todo.description, 'This is an updated todo')
        self.assertEqual(updated_todo.status, 'in_progress')
    
    def test_edit_todo_POST_invalid_form(self):
        """Test POST request with invalid form data."""
        login_successful = self.client.login(username='testuser', password='testpassword')
        self.assertTrue(login_successful)
        
        data = {
            'title': '',  # Title is required
            'description': 'This is an updated todo',
            'status': 'in_progress'
        }
        
        response = self.client.post(self.edit_url, data)
        
        self.assertEqual(response.status_code, 200)  # Stay on same page
        
        # Todo should not be updated
        updated_todo = TodoItem.objects.get(id=self.todo.id)
        self.assertEqual(updated_todo.title, 'Test Todo')
    
    def test_edit_todo_access_control(self):
        """Test that users can only edit their own todos."""
        login_successful = self.client.login(username='otheruser', password='otherpassword')
        self.assertTrue(login_successful)
        
        response = self.client.get(self.edit_url)
        
        # Should return 404 for other users' todos
        self.assertEqual(response.status_code, 404)


class UpdateTodoStatusViewTests(unittest.TestCase):
    """Tests for the update_todo_status view using unittest."""
    
    def setUp(self):
        self.client = Client()
        
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        
        # Create another user for testing access control
        self.other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='otherpassword'
        )
        
        # Create a todo item for the test user
        self.todo = TodoItem.objects.create(
            user=self.user,
            title='Test Todo',
            description='This is a test todo',
            status='pending'
        )
        
        self.update_url = reverse('update_todo_status', kwargs={'todo_id': self.todo.id})
    
    def tearDown(self):
        # Clean up test data
        User.objects.all().delete()
        TodoItem.objects.all().delete()
    
    def test_update_todo_status_login_required(self):
        """Test that login is required to update a todo status."""
        response = self.client.post(self.update_url)
        
        # Should redirect to login page
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))
    
    def test_update_todo_status_ajax(self):
        """Test updating todo status via AJAX."""
        login_successful = self.client.login(username='testuser', password='testpassword')
        self.assertTrue(login_successful)
        
        data = {'status': 'completed'}
        response = self.client.post(
            self.update_url, 
            data,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertTrue(response_data['success'])
        
        # Refresh from database
        updated_todo = TodoItem.objects.get(id=self.todo.id)
        self.assertEqual(updated_todo.status, 'completed')
    
    def test_update_todo_status_invalid(self):
        """Test updating todo status with invalid status."""
        login_successful = self.client.login(username='testuser', password='testpassword')
        self.assertTrue(login_successful)
        
        data = {'status': 'invalid_status'}
        response = self.client.post(
            self.update_url, 
            data,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertFalse(response_data['success'])
        
        # Status should not be updated
        updated_todo = TodoItem.objects.get(id=self.todo.id)
        self.assertEqual(updated_todo.status, 'pending')
    
    def test_update_todo_status_non_ajax(self):
        """Test updating todo status with non-AJAX request."""
        login_successful = self.client.login(username='testuser', password='testpassword')
        self.assertTrue(login_successful)
        
        data = {'status': 'completed'}
        response = self.client.post(self.update_url, data)
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertFalse(response_data['success'])
        
        # Status should not be updated
        updated_todo = TodoItem.objects.get(id=self.todo.id)
        self.assertEqual(updated_todo.status, 'pending')
    
    def test_update_todo_status_access_control(self):
        """Test that users can only update their own todos."""
        login_successful = self.client.login(username='otheruser', password='otherpassword')
        self.assertTrue(login_successful)
        
        data = {'status': 'completed'}
        response = self.client.post(
            self.update_url, 
            data,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        
        # Should return 404 for other users' todos
        self.assertEqual(response.status_code, 404)


class DeleteTodoViewTests(unittest.TestCase):
    """Tests for the delete_todo view using unittest."""
    
    def setUp(self):
        self.client = Client()
        
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        
        # Create another user for testing access control
        self.other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='otherpassword'
        )
        
        # Create a todo item for the test user
        self.todo = TodoItem.objects.create(
            user=self.user,
            title='Test Todo',
            description='This is a test todo',
            status='pending'
        )
        
        self.delete_url = reverse('delete_todo', kwargs={'todo_id': self.todo.id})
        self.todo_list_url = reverse('todo_list')
    
    def tearDown(self):
        # Clean up test data
        User.objects.all().delete()
        TodoItem.objects.all().delete()
    
    def test_delete_todo_login_required(self):
        """Test that login is required to delete a todo."""
        response = self.client.post(self.delete_url)
        
        # Should redirect to login page
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))
    
    def test_delete_todo_POST(self):
        """Test deleting a todo."""
        login_successful = self.client.login(username='testuser', password='testpassword')
        self.assertTrue(login_successful)
        
        response = self.client.post(self.delete_url)
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.todo_list_url)
        
        # Todo should be deleted
        self.assertEqual(TodoItem.objects.count(), 0)
    
    def test_delete_todo_GET(self):
        """Test that GET requests are redirected."""
        login_successful = self.client.login(username='testuser', password='testpassword')
        self.assertTrue(login_successful)
        
        response = self.client.get(self.delete_url)
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.todo_list_url)
        
        # Todo should not be deleted
        self.assertEqual(TodoItem.objects.count(), 1)
    
    def test_delete_todo_access_control(self):
        """Test that users can only delete their own todos."""
        login_successful = self.client.login(username='otheruser', password='otherpassword')
        self.assertTrue(login_successful)
        
        response = self.client.post(self.delete_url)
        
        # Should return 404 for other users' todos
        self.assertEqual(response.status_code, 404)
        
        # Todo should not be deleted
        self.assertEqual(TodoItem.objects.count(), 1)


def load_tests(loader, tests, pattern):
    """Custom test suite loader to run all tests."""
    test_classes = [
        TodoItemModelTests,
        RegisterViewTests,
        TodoListViewTests,
        EditTodoViewTests,
        UpdateTodoStatusViewTests,
        DeleteTodoViewTests,
    ]
    
    suite = unittest.TestSuite()
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    return suite


if __name__ == '__main__':
    unittest.main()
