from django.db import transaction
from django.forms import inlineformset_factory
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from ordersapp.forms import OrderForm, OrderItemForm
from ordersapp.models import Order, OrderItem


class OrderList(ListView):
    model = Order


class OrderCreate(CreateView):
    model = Order
    form_class = OrderForm
    success_url = reverse_lazy('orders:index')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(
            Order, OrderItem, form=OrderItemForm, extra=1
        )

        if self.request.POST:
            formset = OrderFormSet(self.request.POST, self.request.FILES)
        else:
            basket_items = self.request.user.user_basket.all()
            if basket_items and len(basket_items):
                OrderFormSet = inlineformset_factory(
                    Order, OrderItem, form=OrderItemForm, extra=len(basket_items)
                )
                formset = OrderFormSet()
                # for num, form in enumerate(formset.forms):
                # zip(), filter(), map()
                for form, basket_item in zip(formset.forms, basket_items):
                    form.initial['product'] = basket_item.product
                    form.initial['quantity'] = basket_item.quantity
                # basket_items.delete()
            else:
                formset = OrderFormSet()

        data['orderitems'] = formset
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()  # Order object
            if orderitems.is_valid():
                orderitems.instance = self.object  # one to many
                orderitems.save()
            self.request.user.user_basket.all().delete()

        # удаляем пустой заказ
        # if self.object.get_total_cost() == 0:
        #     self.object.delete()

        return super().form_valid(form)


class OrderUpdate(UpdateView):
    model = Order
    form_class = OrderForm
    success_url = reverse_lazy('orders:index')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(
            Order, OrderItem, form=OrderItemForm, extra=1
        )
        if self.request.POST:
            formset = OrderFormSet(
                self.request.POST, self.request.FILES,
                instance=self.object
            )
        else:
            formset = OrderFormSet(instance=self.object)
        data['orderitems'] = formset
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object  # можно закомментировать?
                orderitems.save()

        # удаляем пустой заказ
        # if self.object.get_total_cost() == 0:
        #     self.object.delete()

        return super().form_valid(form)


class OrderDetail(DetailView):
    model = Order


class OrderDelete(DeleteView):
    model = Order
    # success_url = reverse_lazy('ordersapp:orders_list')
    success_url = reverse_lazy('ordersapp:index')
