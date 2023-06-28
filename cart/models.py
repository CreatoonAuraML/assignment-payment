from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.db import IntegrityError




class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField()
    address = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name} | {self.email}"

    def save(self, *args, **kwargs):
        if self.pk:
            existing_user = User.objects.filter(id=self.pk).first()
            if existing_user.email != self.email:
                raise ValueError(
                    "Cannot change the email of an existing user.")
        super().save(*args, **kwargs)


class ItemCategory(models.Model):
    type = models.CharField(max_length=100, unique=True)
    description = models.TextField(default="")
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.type} | {self.description}"

    def save(self, *args, **kwargs):
        lowercased_type = self.type.lower()
        existing_category = ItemCategory.objects.filter(
            type=lowercased_type).first()
        print(existing_category)
        if not existing_category:
            super().save(*args, **kwargs)


class Item(models.Model):
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    quantity = models.IntegerField(validators=[MinValueValidator(0)])
    description = models.TextField(default="")
    # Added PROTECT as there can be many items of same category, and delting the category will lead to delete all the items
    category = models.ForeignKey(ItemCategory, on_delete=models.PROTECT)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'brand'], name='unique_item')
        ]

    def save(self, *args, **kwargs):
        try:
            super().save(*args, **kwargs)
        except IntegrityError as e:
            if 'unique_item' in str(e):
                existing_item = Item.objects.filter(name=self.name, brand=self.brand).first()
                if existing_item:
                    print(f"Item with name '{self.name}' and brand '{self.brand}' already exists.")
            else:
                raise


# Add discount table too
class Order(models.Model):
    currency = models.CharField(max_length=3, default='INR')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date_time = models.DateTimeField(auto_now_add=True)
    items = models.ManyToManyField(Item)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    

    # Not sure to keep this or not, but this thing simply dont allow users to update the order after it gets created
    # def save(self, *args, **kwargs):
    #     # Check if the object already exists in the database
    #     if self.pk is not None:
    #         original_instance = Order.objects.get(pk=self.pk)
    #         # Restore the original values
    #         self.currency = original_instance.currency
    #         self.amount = original_instance.amount
    #         self.date_time = original_instance.date_time
    #         # Set the M2M relationships to the original values
    #         self.items.set(original_instance.items.all())
    #         self.user = original_instance.user
    #     super().save(*args, **kwargs)



class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    payment_status = models.CharField(max_length=100)

    def delete(self, *args, **kwargs):
        if self.order:
            raise PermissionError("Cannot delete payment. Associated order exists.")
        super().delete(*args, **kwargs)