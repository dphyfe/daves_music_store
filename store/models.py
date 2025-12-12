"""
store.models
---------------

Data models for the `store` app. This module defines the main data
structures persisted for the music store: categories, instruments,
shopping carts, and cart items.

Notes:
- Keep model methods small and focused: presentation helpers like
  `get_total` and `get_item_count` are intended for templates and the
  admin, not heavy business logic.
"""

from django.db import models
from django.templatetags.static import static
from django.urls import reverse


class Category(models.Model):
    """Category of instruments.

    Fields:
    - name: human-friendly name, unique
    - slug: URL-safe identifier used in category URLs
    - description: optional longer description displayed on category pages
    """

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        # Useful display in admin and shells
        return self.name


class Instrument(models.Model):
    """Represents an instrument available in the store.

    This model contains display fields (name, brand, image), inventory
    flags (`in_stock`, `featured`) and business data (price, condition).

    The `get_absolute_url` helper returns the canonical product URL used
    by templates and the admin.
    """

    CONDITION_CHOICES = [
        ("new", "New"),
        ("used_excellent", "Used - Excellent"),
        ("used_good", "Used - Good"),
        ("used_fair", "Used - Fair"),
    ]

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    # Link back to Category; deleting a category cascades to its instruments
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="instruments")
    brand = models.CharField(max_length=100)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default="new")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=5.0, help_text="Customer rating out of five")
    description = models.TextField()
    specifications = models.TextField(blank=True, help_text="Technical specifications")
    # Optional product image stored under MEDIA_ROOT/instruments/
    image = models.ImageField(upload_to="instruments/", blank=True, null=True)
    in_stock = models.BooleanField(default=True)
    # Re-used as a 'deal' marker in some views/templates
    featured = models.BooleanField(default=False, help_text="Display on homepage")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.brand} {self.name}"

    def get_absolute_url(self):
        """Return the URL to view the product detail page.

        Used by templates and admin display to provide canonical links.
        """

        return reverse("product_detail", kwargs={"slug": self.slug})

    @property
    def image_display_url(self):
        """Return a usable URL for instrument images whether served from static or media."""

        if not self.image:
            return ""

        if staticfiles_storage.exists(self.image.name):
            return static(self.image.name)

        try:
            return self.image.url
        except ValueError:
            return ""


class Cart(models.Model):
    """A simple shopping cart identified by a session key.

    The cart is stored server-side and keyed by the Django session
    `session_key`. It holds related `CartItem` objects accessible via
    the `items` related name.
    """

    session_key = models.CharField(max_length=40, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart {self.session_key}"

    def get_total(self):
        """Compute the total price for all items in the cart.

        This iterates related `CartItem` objects and delegates subtotal
        calculation to each item. Keep this simple — avoid heavy queries
        in templates by prefetching `items` where appropriate.
        """

        return sum(item.get_subtotal() for item in self.items.all())

    def get_item_count(self):
        """Return the total number of units across all cart items."""

        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    """A single instrument entry in a Cart.

    - `unique_together` ensures there is at most one row per `(cart, instrument)`
      pair, simplifying quantity adjustments.
    """

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("cart", "instrument")

    def __str__(self):
        return f"{self.quantity}x {self.instrument.name}"

    def get_subtotal(self):
        """Return the line total for this item (price * quantity)."""

        return self.instrument.price * self.quantity
