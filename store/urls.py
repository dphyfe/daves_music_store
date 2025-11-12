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
]
