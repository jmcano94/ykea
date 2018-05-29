from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Item(models.Model):

    CATEGORIES = (
        ("beds", "Beds & mattressess"),
        ("furn", "Furniture, wardrobes & shelves"),
        ("sofa", "Sofas & armchairs"),
        ("table", "Tables & chairs"),
        ("texti", "Textiles"),
        ("deco", "Decoration & mirrors"),
        ("light", "Lighting"),
        ("cook", "Cookware"),
        ("tablw", "Tableware"),
        ("taps", "Taps & sinks"),
        ("org", "Organisers & storage accesories"),
        ("toys", "Toys"),
        ("leis", "Leisure"),
        ("safe", "safety"),
        ("diy", "Do-it-yourself"),
        ("floor", "Flooring"),
        ("plant", "Plants & gardering"),
        ("food", "Food & beverages")
    )
    item_number = models.CharField(max_length=8, unique=True)
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_new = models.BooleanField()
    size = models.CharField(max_length=40)
    instructions = models.FileField()
    featured_photo = models.ImageField()
    category = models.CharField(max_length=5, choices=CATEGORIES)

    def __str__(self):
        return('[**NEW**]' if self.is_new else '') + "[" + self.category + "] [" + self.item_number + "] " + self.name\
                + " - " + self.description + " (" + self.size + ") : " + str(self.price) + " €"

    def getCategoryFullName(self, category):
        for cat in self.CATEGORIES:
            if cat[0] == category:
                return cat[1]
        return ""


class Shoppingcart(models.Model):
    items = models.ManyToManyField(
        Item,
        through='ItemCart',
        through_fields=('shoppingcart', 'item')
    )


class ItemCart(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    shoppingcart = models.ForeignKey(Shoppingcart, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    money = models.FloatField()
    shoppingcart = models.ForeignKey(Shoppingcart, on_delete=models.CASCADE, null=True)


class Bill(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    items = models.ManyToManyField(
        Item,
        through='ItemBill',
        through_fields=('bill', 'item')
    )
    total = models.FloatField(default=0.0)


class ItemBill(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)




