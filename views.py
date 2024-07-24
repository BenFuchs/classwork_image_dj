"""
This module contains views for handling user registration and product management.
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound

from django.contrib.auth.models import User
from .serializers import ProductSerializer
from .models import Product

class UserRegistrationView(APIView):
    """
    Handle user registration.
    """
    def post(self, request):
        """
        Register a new user.

        Args:
            request: The HTTP request object containing user data.

        Returns:
            Response: A Response object indicating the result of the registration.
        """
        user = User.objects.create_user(
            username=request.data['username'],
            email=request.data['email'],
            password=request.data['password']
        )
        user.is_active = True
        user.is_staff = False
        user.save()
        return Response("New user created", status=status.HTTP_201_CREATED)


class IndexView(APIView):
    """
    A simple endpoint for testing.
    """
    def get(self, request):
        """
        Handle GET requests for testing.

        Args:
            request: The HTTP request object.

        Returns:
            Response: A Response object containing a simple greeting.
        """
        return Response('Hello')


class ProductDetailView(APIView):
    """
    Handle CRUD operations for products based on HTTP method.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, product_id=None):
        """
        Retrieve product details or a list of products.

        Args:
            request: The HTTP request object.
            product_id (int, optional): The ID of the product. Defaults to None.

        Returns:
            Response: A Response object containing product data or an error message.
        """
        if product_id is None:
            products = Product.objects.all()
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)
        
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist as exc:
            raise NotFound("Product not found") from exc

        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def post(self, request):
        """
        Create a new product.

        Args:
            request: The HTTP request object containing product data.

        Returns:
            Response: A Response object containing the created product data or an error message.
        """
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, product_id):
        """
        Update an existing product.

        Args:
            request: The HTTP request object containing updated product data.
            product_id (int): The ID of the product to update.

        Returns:
            Response: A Response object containing the updated product data or an error message.
        """
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist as exc:
            raise NotFound("Product not found") from exc

        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, product_id):
        """
        Delete a product.

        Args:
            request: The HTTP request object.
            product_id (int): The ID of the product to delete.

        Returns:
            Response: A Response object indicating the result of the delete operation.
        """
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist as exc:
            raise NotFound("Product not found") from exc

        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
