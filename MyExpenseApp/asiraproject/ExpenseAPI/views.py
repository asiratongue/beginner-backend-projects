from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User
from .models import Expense
from .serializers import UserSerializer, ExpenseSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.exceptions import AuthenticationFailed
from datetime import datetime
import jsonify


class RegisterUserAPIView(APIView):
    model = User

    def post(self, request):
        serializer = UserSerializer(data=request.data)  ###get data from the http request

        if serializer.is_valid():  #check if request data matches with serializer 
            user = serializer.save()

            token_serializer = TokenObtainPairSerializer(data={
                "username": user.username,
                "password": request.data["password"]    
            })

            if token_serializer.is_valid():
                tokens = token_serializer.validated_data

                return Response({
                    'user': serializer.data,
                    'tokens' : tokens  
                }, status=status.HTTP_201_CREATED)

            else: 
                print(serializer.errors)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   

        else:
            print("errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
class LoginUserAPIView(APIView):
    model = User

    def post(self, request):
        user = authenticate(username = request.data["username"], password = request.data["password"])

        token_serializer = TokenObtainPairSerializer(data={
            "username": request.data["username"],
            "password": request.data["password"]    
        })

        if token_serializer.is_valid():
            tokens = token_serializer.validated_data

            if user is not None:
                return Response({f"hello { request.data['username'] }!" : "login authenticated successfully", 'tokens' : tokens}, status=status.HTTP_201_CREATED)
            
            else:
                return Response({"detail": "Invalid credentials. Please try again."}, status=status.HTTP_400_BAD_REQUEST)        
        else:
            return Response({"detail": "Invalid credentials for token. Please try again."}, status=status.HTTP_401_UNAUTHORIZED)

class CreateExpenseAPIView(APIView):           #create a get request method for retrieving all expenses
    model = Expense
    permission_classes = [IsAuthenticated]

    def post(self, request):    
        user = request.user
        serializer = ExpenseSerializer(data=request.data)

        if serializer.is_valid():
            serializer.validated_data['userID'] = user.username
            Expense = serializer.save()

            return Response({'userID' : Expense.userID, "name" : Expense.name, 
                             "expense" : Expense.expense})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UDExpenseAPIView(APIView):

    model = Expense
    permission_classes = [IsAuthenticated]

    def put(self, request, idx=None):
        if idx:

            try:
                expenseobj = Expense.objects.get(id=idx)
                userid = expenseobj.userID
                user = request.user
                UserObj = User.objects.get(username = user.username)

                if userid != UserObj.username:
                    return Response({"error" : "wrong token/userID for the selected index!"}, status=status.HTTP_403_FORBIDDEN)
                
                else:                        
                    expenseobj.name = request.data["name"]
                    expenseobj.expense = request.data["expense"]
                    expenseobj.save()

                return Response({"you have successfully updated the expense" : f"id{expenseobj.id}", "name": expenseobj.name, "expense" : expenseobj.expense})

            except Expense.DoesNotExist:
                return Response({"error": "Expense not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error":"check your url!"}) 

    def delete(self, request, idx=None):
        if idx:

            try:
                expenseobj = Expense.objects.get(id=idx)
                userid = expenseobj.userID
                user = request.user
                UserObj = User.objects.get(username = user.username)

                if userid != UserObj.username:
                    return Response({"error" : "wrong token/userID for the selected index!"})
                
                else:   
                    expenseobj.delete()
                return Response ({f"object with id: {idx} deleted": "goodbye!"})
            
            except Expense.DoesNotExist:
                return Response({"error": "Expense not found"}, status=status.HTTP_404_NOT_FOUND)    


class ListExpenseAPIView(APIView):

    model = Expense
    permission_classes = [IsAuthenticated]

     
    def get(self, request):

        
        try:
            DataDict = {}
            user = request.user
            daterange = request.GET.get('from', None)
            MonthDay = daterange.split('-')

            ExpensesList = Expense.objects.filter(createdat__gte=datetime(2024, int(MonthDay[0]), int(MonthDay[1])))

            for index, obj in enumerate(ExpensesList):
                jsondata = {"expense": obj.expense, "name" : obj.name, "id" : obj.id}

                if user.username == obj.userID:
                    DataDict[obj.userID + str(index)] = jsondata

                else:
                    continue

            return Response(DataDict, status=status.HTTP_202_ACCEPTED)
        
        except Expense.DoesNotExist:
            return Response({"error": "query parameters may be wrong"}, status=status.HTTP_404_NOT_FOUND)



