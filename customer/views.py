from django.core.mail import send_mail
from django.shortcuts import render
from django.views import View

from customer.models import MenuItem, OrderModel


class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/index.html')


class About(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/about.html')


class Order(View):
    def get(self, request, *args, **kwargs):
        appetizers = MenuItem.objects.filter(category__name__contains='Appetizer')
        drinks = MenuItem.objects.filter(category__name__contains='Drink')
        desserts = MenuItem.objects.filter(category__name__contains='Dessert')
        entries = MenuItem.objects.filter(category__name__contains='Entre')
        context = {
            'appetizers': appetizers,
            'drinks': drinks,
            'desserts': desserts,
            'entries': entries,
        }
        return render(request, 'customer/order.html', context)

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        street = request.POST.get('street')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip_code')

        order_items = {
            'items': []
        }
        items = request.POST.getlist('items')
        for item in items:
            items_selected_by_user = MenuItem.objects.get(pk__contains=int(item))

            item_data = {
                'id': items_selected_by_user.pk,
                'name': items_selected_by_user.name,
                'price': items_selected_by_user.price,
            }

            order_items['items'].append(item_data)

        price = 0
        item_ids = []

        for item2 in order_items['items']:
            price += item2['price']
            item_ids.append(item2['id'])

        order = OrderModel.objects.create(
                        price=price,
                        name=name,
                        email=email,
                        street=street,
                        city=city,
                        state=state,
                        zip_code=zip_code,
                        )
        order.items.add(*item_ids)

        body = ('Thank you for your order, your food is being delivered soon\n'
                f'your total: {price}\n'
                'Thank you for your order')

        send_mail(
            'Thank you for your order!',
            body,
            'example@gmail.com',
            [email],
            fail_silently=False)

        context = {
            'items': order_items['items'],
            'price': price,
        }

        return render(request, 'customer/order_confirmation.html', context)
