"""
API views for the store app using Django REST framework.
"""

from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Category, Instrument, CartItem
from .serializers import CategorySerializer, InstrumentSerializer, CartSerializer
from .views import get_or_create_cart


@api_view(["GET"])
def api_categories(request):
    categories = Category.objects.all().order_by("name")
    serializer = CategorySerializer(categories, many=True)
    return Response({"results": serializer.data})


@api_view(["GET"])
def api_instruments(request):
    instruments = Instrument.objects.select_related("category").all()

    category_slug = request.query_params.get("category")
    if category_slug:
        instruments = instruments.filter(category__slug=category_slug)

    condition = request.query_params.get("condition")
    if condition:
        instruments = instruments.filter(condition=condition)

    selected_brands = request.query_params.getlist("brand")
    if selected_brands:
        instruments = instruments.filter(brand__in=selected_brands)

    search_query = request.query_params.get("search")
    if search_query:
        instruments = instruments.filter(Q(name__icontains=search_query) | Q(brand__icontains=search_query) | Q(description__icontains=search_query))

    in_stock = request.query_params.get("in_stock")
    if in_stock in {"true", "false"}:
        instruments = instruments.filter(in_stock=(in_stock == "true"))
    else:
        instruments = instruments.filter(in_stock=True)

    serializer = InstrumentSerializer(instruments, many=True, context={"request": request})
    return Response({"results": serializer.data})


@api_view(["GET"])
def api_instrument_detail(request, slug):
    instrument = get_object_or_404(Instrument.objects.select_related("category"), slug=slug)
    serializer = InstrumentSerializer(instrument, context={"request": request})
    return Response(serializer.data)


@api_view(["GET"])
def api_cart(request):
    cart = get_or_create_cart(request)
    serializer = CartSerializer(cart, context={"request": request})
    return Response(serializer.data)


@api_view(["POST"])
def api_cart_add(request):
    slug = request.data.get("slug")
    quantity = request.data.get("quantity", 1)

    if not slug:
        return Response({"error": "Missing slug"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        quantity = int(quantity)
    except (TypeError, ValueError):
        return Response({"error": "Invalid quantity"}, status=status.HTTP_400_BAD_REQUEST)

    if quantity <= 0:
        return Response({"error": "Quantity must be greater than 0"}, status=status.HTTP_400_BAD_REQUEST)

    instrument = get_object_or_404(Instrument, slug=slug)
    cart = get_or_create_cart(request)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, instrument=instrument)
    if created:
        cart_item.quantity = quantity
    else:
        cart_item.quantity += quantity
    cart_item.save()

    serializer = CartSerializer(cart, context={"request": request})
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def api_cart_item_update(request, item_id):
    quantity = request.data.get("quantity")

    if quantity is None:
        return Response({"error": "Missing quantity"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        quantity = int(quantity)
    except (TypeError, ValueError):
        return Response({"error": "Invalid quantity"}, status=status.HTTP_400_BAD_REQUEST)

    cart_item = get_object_or_404(CartItem, id=item_id)
    if quantity <= 0:
        cart_item.delete()
    else:
        cart_item.quantity = quantity
        cart_item.save()

    cart = get_or_create_cart(request)
    serializer = CartSerializer(cart, context={"request": request})
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def api_cart_item_remove(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()

    cart = get_or_create_cart(request)
    serializer = CartSerializer(cart, context={"request": request})
    return Response(serializer.data, status=status.HTTP_200_OK)
