from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("guitars/", views.guitars_page, name="guitars"),
    path("basses/", views.basses_page, name="basses"),
    path("drums/", views.drums_page, name="drums"),
    path("horns/", views.horns_page, name="horns"),
    path("keyboards/", views.keyboards_page, name="keyboards"),
    path("amps-effects/", views.amps_effects_page, name="amps_effects"),
    path("lessons/", views.lessons_page, name="lessons"),
    path("products/", views.product_list, name="product_list"),
    path("categories/", views.category_list, name="category_list"),
    path("product/<slug:slug>/", views.product_detail, name="product_detail"),
    path("cart/", views.cart_view, name="cart_view"),
    path("cart/add/<slug:slug>/", views.add_to_cart, name="add_to_cart"),
    path("cart/update/<int:item_id>/", views.update_cart_item, name="update_cart_item"),
    path("cart/remove/<int:item_id>/", views.remove_from_cart, name="remove_from_cart"),
]
