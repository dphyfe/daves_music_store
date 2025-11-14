from django.contrib import admin
from .models import Category, Instrument, Cart, CartItem

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


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ["added_at"]


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ["session_key", "created_at", "updated_at", "get_item_count", "get_total"]
    readonly_fields = ["session_key", "created_at", "updated_at"]
    inlines = [CartItemInline]

    def get_item_count(self, obj):
        return obj.get_item_count()

    get_item_count.short_description = "Items"

    def get_total(self, obj):
        return f"${obj.get_total()}"

    get_total.short_description = "Total"
