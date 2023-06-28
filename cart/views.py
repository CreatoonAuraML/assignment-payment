from rest_framework import generics, status
from rest_framework.response import Response
from .models import User, Item, Order, ItemCategory, Payment
from .serializers import UserSerializer, ItemSerializer, ItemCategorySerializer, OrderSerializer, PaymentSerializer


class UserView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


'''
    Item Category View
'''


class ItemCategoryView(generics.ListCreateAPIView):
    queryset = ItemCategory.objects.all()
    serializer_class = ItemCategorySerializer


'''
Item View
'''


class ItemView(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class ItemDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


'''
Order Views
'''


class OrderView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


'''
Payment views
'''

class PaymentView(generics.ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

class PaymentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def destroy(self, request, *args, **kwargs):
        payment = self.get_object()
        
        if payment.order:
            return Response({"detail": "Cannot delete payment. Associated order exists."}, status=status.HTTP_400_BAD_REQUEST)

        return super().destroy(request, *args, **kwargs)