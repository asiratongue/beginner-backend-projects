from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from .models import Expense


class JWTAuthenticationTest(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.user = get_user_model().objects.create_user(username='testuser', password='testpass')

    def test_ObtainJwtToken(self):

        response = self.client.post('/ExpenseAPI/login/', {'username': 'testuser', 'password': 'testpass'}, format='json')

        self.assertEqual(response.status_code, 201)
        self.assertIn('tokens', response.data)

        

    def test_expiredToken(self):
        response = self.client.post('/ExpenseAPI/login/', {'username': 'testuser', 'password': 'testpass'}, format='json')
        tkn = response.data['tokens']['access']

        response2 = self.client.post('/ExpenseAPI/expense/', {'username': 'testuser', 'password': 'testpass', 'token': tkn})

        self.assertEqual(response2.status_code, 401)
        #to test, change the settings to make access token expire in one second.


class MultiUserTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass')
        self.user2 = get_user_model().objects.create_user(username='testuser2', password='testpass2')

        
        login2 = self.client.post('/ExpenseAPI/login/', {'username': 'testuser2', 'password': 'testpass2'}, format='json')
        self.token2 = login2.data['tokens']['access']


    def test_DataCreationIsolation(self):

        expenserequest = self.client.post('/ExpenseAPI/login/', {'username': 'testuser', 'password': 'testpass'}, format='json') 
        print("Expense Creation Response:", expenserequest.data) 
        self.token = expenserequest.data['tokens']['access']

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        expenserequest = self.client.post('/ExpenseAPI/expense/', {"name" : "testexpensename", "expense" : " 2pound testexpense"}, format ='json')
        print(expenserequest.data)
        expenseobj = Expense.objects.get(name = "testexpensename")   #FIXXXX
        print(expenseobj)
        expense_id = expenseobj.id

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token2)

        updaterequest = self.client.put(f'/ExpenseAPI/expense/{expense_id}', {"name" : "testexpensenameupdate", "expense" : "illegal update attempt"}, format ='json')
        self.assertEqual(updaterequest.status_code, 403)  


class CreateUpdateInvalidTest(TestCase):

    def setUp(self):

        self.client = APIClient()
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass')

        login = self.client.post('/ExpenseAPI/login/', {'username': 'testuser', 'password': 'testpass'}, format='json')
        self.token = login.data['tokens']['access']

    def test_invalidUserRegistration(self):
        
        response = self.client.post('/ExpenseAPI/register/', {'username': 'testuse!2', 'password': 'tes!ass'}, format='json')
        self.assertEqual(response.status_code, 400)

    def test_invalidExpenseCreation(self):

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        CreateExpense = self.client.post('/ExpenseAPI/expense/', {"name" : "testexpens!name", "expense" : " 2pound testexp!se"}, format ='json')
        self.assertEqual(CreateExpense.status_code, 400)



class ExpenseValidationTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass')
        login = self.client.post('/ExpenseAPI/login/', {'username': 'testuser', 'password': 'testpass'}, format='json')
        self.token = login.data['tokens']['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_expense_name_and_description_maximum_length(self):
        valid_name = "x" * 100
        valid_expense_description = "y" * 100
        response = self.client.post('/ExpenseAPI/expense/',{"name": valid_name, "expense": valid_expense_description}, format='json')
        self.assertEqual(response.status_code, 200)

        invalid_name = "x" * 101
        invalid_expense_description = "y" * 101
        response = self.client.post('/ExpenseAPI/expense/', {"name": invalid_name, "expense": invalid_expense_description},format='json')

        self.assertEqual(response.status_code, 400)
        self.assertIn('name', response.data)
        self.assertIn('expense', response.data)
   