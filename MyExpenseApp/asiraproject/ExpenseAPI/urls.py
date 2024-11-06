from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = "ExpenseAPI"

urlpatterns = [
    
    path("register/", views.RegisterUserAPIView.as_view(), name="register"),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', views.LoginUserAPIView.as_view(), name="login"),
    path('expense/', views.CreateExpenseAPIView.as_view(), name="expense"),
    path('expense/<int:idx>', views.UDExpenseAPIView.as_view(), name="UDexpense"),
    path('expense/search/', views.ListExpenseAPIView.as_view(), name='search'),
    
    ]



#So URLS, is the place where uniform resource locator endpoints are stored, and references for them are made.
#the data and logic required of them is retrieved with .views ygm
