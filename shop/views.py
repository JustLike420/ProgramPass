from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required  # надо быть залогининым что вы вызвать функцию
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

from .models import Item, OrderItem, Order


# Create your views here.

def item_list(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, "item_list.html", context)


def about(request):
    return render(request, "about.html")


class HomeView(ListView):
    model = Item
    template_name = "item_list.html"
    context_object_name = 'items'


class OrderSummeryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order,
            }
            return render(self.request, 'order_summer.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "У вас нету активного заказа")
            return redirect("/")


class ItemDetailView(DetailView):
    model = Item
    template_name = "product.html"
    context_object_name = 'item'


# добавление товара в корзину
@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            messages.info(request, "Товар уже добавлен в корзину.")
            return redirect("core:product", slug=slug)
        else:
            messages.info(request, "Этот товар был добавлен в вашу корзину.")
            order.items.add(order_item)
            return redirect("core:product", slug=slug)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "Этот товар был добавлен в вашу корзину.")
        return redirect("core:product", slug=slug)


# удаление товара в корзину
@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False)[0]
            order.items.remove(order_item)
            messages.info(request, "Товар был удален из вашей корзины.")
            return redirect("core:product", slug=slug)
        else:
            # заказ не содержит этого товара
            messages.info(request, "Этого товара нет в вашей корзине.")
            return redirect("core:product", slug=slug)
    else:
        # нет заказа
        messages.info(request, "У вас нет активного заказа.")
        return redirect("core:product", slug=slug)
