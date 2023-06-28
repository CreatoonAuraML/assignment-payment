from django.urls import path
from . import views

urlpatterns = [
    path('user', views.UserView.as_view()),
    path('user/<int:pk>', views.UserDetailView.as_view()),
    path('item-category', views.ItemCategoryView.as_view()),
    path('item', views.ItemView.as_view()),
    path('item/<str:pk>', views.ItemDetailsView.as_view()),
    path('order', views.OrderView.as_view()),
    path('order/<str:pk>', views.OrderDetailsView.as_view()),
    path('payment', views.PaymentView.as_view()),
    path('payment/<str:pk>', views.PaymentDetailView.as_view())
]
