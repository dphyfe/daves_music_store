from django.contrib import admin
from .models import Category, Instrument

# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ["name"]


@admin.register(Instrument)
class InstrumentAdmin(admin.ModelAdmin):
    list_display = ["name", "brand", "category", "condition", "price", "in_stock", "featured", "created_at"]
    list_filter = ["category", "condition", "in_stock", "featured", "created_at"]
    list_editable = ["price", "in_stock", "featured"]
    prepopulated_fields = {"slug": ("brand", "name")}
    search_fields = ["name", "brand", "description"]
    date_hierarchy = "created_at"
    ordering = ["-created_at"]
