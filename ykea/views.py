from django.shortcuts import render
from ykea.models import Item
from ykea.models import Customer
from ykea.models import Shoppingcart
from ykea.models import ItemCart
from ykea.models import ItemBill
from ykea.models import Bill
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from .serializers import ItemSerializer
from rest_framework import permissions
from .permissions import MyPermissions

class ItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Items to be viewed or edited.
    """

    queryset = Item.objects.all().order_by('item_number')

    serializer_class = ItemSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Item.objects.all()
        category = self.request.query_params.get('category', None)
        new = self.request.query_params.get('new', None)
        price = self.request.query_params.get('price', None)


        if category is not None:
            queryset = queryset.filter(category=category)
        if new is not None and new == 'yes':
            queryset = queryset.filter(is_new=True)
        elif new is not None and new =='no':
            queryset = queryset.filter(is_new=False)
        if price is not None:
            queryset = queryset.filter(price__lt=price)
        return queryset

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """

        if self.action == 'list':
            permission_classes = [permissions.IsAuthenticatedOrReadOnly,]

        else:
            permission_classes = [MyPermissions, permissions.IsAuthenticatedOrReadOnly]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        self.permission_classes = [MyPermissions,]
        return super(ItemViewSet, self).create(request, *args, **kwargs)


def index(request):
    categories = Item.CATEGORIES

    context = {
        'categories': categories
    }
    if request.user.is_authenticated():
        context['user'] = request.user
    return render(request, 'ykea/home.html', context)


def items(request, category=""):
    items_by_category = Item.objects.filter(category=category)
    i = Item()
    cat_full_name = i.getCategoryFullName(category)
    cat = (category, cat_full_name)
    context = {
        'items': items_by_category,
        'category': cat,
        'categories': Item.CATEGORIES
    }

    return render(request, 'ykea/items.html', context)


def item(request, item_number=None):
    item = Item.objects.get(item_number=item_number)
    i = Item()
    cat_full_name = i.getCategoryFullName(item.category)
    context = {
        'item': item,
        'categories': Item.CATEGORIES,
        'category': cat_full_name
    }

    return render(request, 'ykea/item.html', context)


@login_required
def shoppingcart(request):
    customer = Customer.objects.get(user=request.user)
    if "shoppingCart" in request.session:
        sc_id = request.session["shoppingCart"]
        sc = Shoppingcart.objects.get(id=sc_id)
    elif customer.shoppingcart:
        sc = customer.shoppingcart
    else:
        sc = Shoppingcart()
        sc.save()
        customer = Customer.objects.get(user=request.user)
        customer.shoppingcart = sc
        customer.save()
    for key in request.POST:
        if key.startswith("checkbox"):
            item = Item.objects.get(item_number=request.POST[key])
            try:
                ItemCart.objects.get(item=item, shoppingcart=sc)
            except:
                itemCart = ItemCart(item=item, shoppingcart=sc, amount=1)
                itemCart.save()

    request.session["shoppingCart"] = sc.id
    return HttpResponseRedirect(reverse('buy'))

@login_required
def buy(request):
    sc_id = request.session["shoppingCart"]
    sc = Shoppingcart.objects.get(id=sc_id)

    context = {
        'shoppingCart': sc.itemcart_set.all(),
        'categories': Item.CATEGORIES
    }

    return render(request, 'ykea/shoppingcart.html', context)


def process_cart(request):
    for key in request.POST:
        if key.startswith("quantity"):
            amount = request.POST[key]
            itemCart_id = int(key[8:])
            itemCart = ItemCart.objects.get(id=itemCart_id)
            itemCart.amount = amount
            itemCart.save()

    if request.POST.get("checkout"):
        sc_id = request.session["shoppingCart"]
        sc = Shoppingcart.objects.get(id=sc_id)
        total = 0
        for item_cart in sc.itemcart_set.all():
            total = total + item_cart.amount * item_cart.item.price
        customer = Customer.objects.get(user=request.user)
        if customer.money >= total:
            customer.money -= float(total)
            customer.save()
            return HttpResponseRedirect(reverse('checkout'))
        else:
            return HttpResponseRedirect(reverse('buy'))
    else:
        for key in request.POST:
            if key.startswith("delete"):
                itemCart_id = int(key[6:])
                print(itemCart_id)
                ItemCart.objects.get(id=itemCart_id).delete()
                return HttpResponseRedirect(reverse('buy'))


def checkout(request):
    sc_id = request.session["shoppingCart"]
    sc = Shoppingcart.objects.get(id=sc_id)
    del request.session["shoppingCart"]
    customer = Customer.objects.get(user=request.user)
    bill = Bill(user=customer)
    bill.save()
    total = 0
    for item_cart in sc.itemcart_set.all():
        item_bill = ItemBill(item=item_cart.item, bill=bill, amount=item_cart.amount)
        item_bill.save()
        total = total + item_cart.amount*item_cart.item.price
        item_cart.delete()
    bill.total = total
    bill.save()
    context = {
        'bill': bill,
        'categories': Item.CATEGORIES,

    }

    return render(request, 'ykea/checkout.html', context)


def login_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        # Correct password, and the user is marked "active"
        auth.login(request, user)
        # Redirect to a success page.
        return HttpResponseRedirect("/account/loggedin/")
    else:
        # Show an error page
        return HttpResponseRedirect("/account/invalid/")


def logout_view(request):
    auth.logout(request)
    # Redirect to a success page.t
    return HttpResponseRedirect("/account/loggedout/")


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            customer = Customer(user=new_user)
            customer.money = 0
            customer.save()
            auth.login(request, new_user)
            return HttpResponseRedirect(reverse("index"))
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {
        'form': form,
    })

@login_required
def comparator(request, ips):
    categories = Item.CATEGORIES

    context = {
        'categories': categories,
        'ips': ips
    }

    return render(request, 'ykea/comparator.html', context)