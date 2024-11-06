from rest_framework import serializers
from ExpenseAPI.models import Expense
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):

    def validate_user(self, value):
        import re
        if not re.match("^[A-Za-z0-9]*$", value):
            raise serializers.ValidationError("Only letters and numbers are allowed!")
        return value
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only':True}, 'id' : {'read_only':True}}




    def create(self, validated_data):
        print("creating user:", validated_data)
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    

class ExpenseSerializer(serializers.ModelSerializer):

    def validate_expense(self, value):

        import re
        if not re.match("^[A-Za-z0-9]*$", value):
            raise serializers.ValidationError("Only letters and numbers are allowed!")
        return value
    
    class Meta:
        model = Expense
        fields = ['userID', 'name', 'expense']
        extra_kwargs = {'id' : {'read_only':True}}
        
    def create(self, validated_data):
    
        return super().create(validated_data)

#remember, serialiser is used to convert the raw model data into json compatible data

#will need to create update, delete functions for the user model w serializer, if data needs modifying