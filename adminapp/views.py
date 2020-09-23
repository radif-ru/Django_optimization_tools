from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from adminapp.forms import AdminShopUserCreateForm, AdminShopUserUpdateForm, \
    AdminProductCategoryCreateForm, AdminProductUpdateForm
from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product


# Незалогиненного отправляем логинится. Проверяем является ли пользователь суперюзером
# @user_passes_test(lambda x: x.is_superuser)
# def index(request):
#     users_list = get_user_model().objects.all().order_by(
#         '-is_active', '-is_superuser', '-is_staff', 'username'
#     )
#
#     context = {
#         'page_title': 'админка/пользователи',
#         'users_list': users_list,
#     }
#
#     return render(request, 'adminapp/index.html', context)


class OnlySuperUserMixin:
    @method_decorator(user_passes_test(lambda x: x.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class PageTitleMixin:
    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data(object_list=None, **kwargs)
        # print(data)
        data['page_title'] = self.page_title
        return data


class UsersList(OnlySuperUserMixin, PageTitleMixin, ListView):
    model = get_user_model()

    page_title = 'админка/пользователи'

    # extra_context = {
    #     'page_title': 'админка/пользователи',
    # }

    # def get_queryset(self):
    #     qs = super().get_queryset()
    #     return qs
    #     # return self.model.objects.all().order_by()


@user_passes_test(lambda x: x.is_superuser)
def user_create(request):
    if request.method == 'POST':
        user_form = AdminShopUserCreateForm(request.POST, request.FILES)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('my_admin:index'))
    else:
        user_form = AdminShopUserCreateForm()

    context = {
        'page_title': 'пользователи/создание',
        'user_form': user_form,
    }

    return render(request, 'adminapp/user_update.html', context)


@user_passes_test(lambda x: x.is_superuser)
def user_update(request, pk):
    user = get_object_or_404(get_user_model(), pk=pk)
    if request.method == 'POST':
        user_form = AdminShopUserUpdateForm(request.POST, request.FILES, instance=user)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('my_admin:index'))
    else:
        user_form = AdminShopUserUpdateForm(instance=user)

    context = {
        'page_title': 'пользователи/редактирование',
        'user_form': user_form,
    }

    return render(request, 'adminapp/user_update.html', context)


@user_passes_test(lambda x: x.is_superuser)
def user_delete(request, pk):
    user = get_object_or_404(get_user_model(), pk=pk)
    # user.delete()
    if request.method == 'POST':
        user.is_active = False
        user.save()
        return HttpResponseRedirect(reverse('my_admin:index'))

    context = {
        'page_title': 'пользователи/удаление',
        'user_to_delete': user,
    }

    return render(request, 'adminapp/user_delete.html', context)


# @user_passes_test(lambda x: x.is_superuser)
# def categories_read(request):
#     context = {
#         'page_title': 'админка/категории',
#         'categories_list': ProductCategory.objects.all(),
#     }
#
#     return render(request, 'adminapp/categories_list.html', context)

# FBS vs CBV


# class CategoriesRead(ListView):
#     model = ProductCategory
#     template_name = 'adminapp/categories_list.html'
#     context_object_name = 'categories_list'


# class CategoriesRead(ListView):
#     model = ProductCategory
#     template_name = 'adminapp/categories_list.html'


class ProductCategoriesRead(OnlySuperUserMixin, PageTitleMixin, ListView):
    model = ProductCategory
    page_title = 'админка/категории'
    # paginate_by = 3
    # extra_context = {
    #     'page_title': 'админка/категории',
    # }


class ProductCategoryCreate(OnlySuperUserMixin, PageTitleMixin, CreateView):
    model = ProductCategory
    page_title = 'админка/категории/создание'
    # success_url = reverse('my_admin:index')
    success_url = reverse_lazy('my_admin:categories_read')
    # fields = '__all__'
    form_class = AdminProductCategoryCreateForm


class ProductCategoryUpdate(OnlySuperUserMixin, PageTitleMixin, UpdateView):
    model = ProductCategory
    page_title = 'админка/категории/редактирование'
    success_url = reverse_lazy('my_admin:categories_read')
    form_class = AdminProductCategoryCreateForm
    pk_url_kwarg = 'category_pk'


class ProductCategoryDelete(OnlySuperUserMixin, PageTitleMixin, DeleteView):
    model = ProductCategory
    page_title = 'админка/категории/удаление'
    success_url = reverse_lazy('my_admin:categories_read')

    # Переопределяем delete для того, чтобы вместо жесткого удаления делать категорию инактивной
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.success_url)


@user_passes_test(lambda u: u.is_superuser)
def category_products(request, category_pk):
    category = get_object_or_404(ProductCategory, pk=category_pk)
    object_list = category.product_set.all()

    context = {
        'page_title': f'категория {category.name}/продукты',
        'category': category,
        'object_list': object_list,
    }
    return render(request, 'adminapp/category_products_list.html', context)


@user_passes_test(lambda u: u.is_superuser)
def product_create(request, category_pk):
    category = get_object_or_404(ProductCategory, pk=category_pk)
    if request.method == 'POST':
        form = AdminProductUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse(
                'my_admin:category_products',
                kwargs={'category_pk': category.pk}
            ))
    else:
        form = AdminProductUpdateForm(
            initial={
                'category': category,
                # 'name': 'начальное имя'
                # 'quantity': 18,
                # 'price': 157.9,
            }
        )

    context = {
        'page_title': 'продукты/создание',
        'form': form,
        'category': category
    }
    return render(request, 'adminapp/product_update.html', context)


@user_passes_test(lambda u: u.is_superuser)
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    # print(product)

    if request.method == 'POST':
        form = AdminProductUpdateForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse(
                'my_admin:category_products',
                kwargs={'category_pk': product.category.pk}
            ))
    else:
        form = AdminProductUpdateForm(instance=product)

    context = {
        'page_title': 'продукты/редактирование',
        'form': form,
        'category': product.category
    }
    return render(request, 'adminapp/product_update.html', context)


@user_passes_test(lambda u: u.is_superuser)
def product_delete(request, pk):
    obj = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        obj.is_active = False
        obj.save()
        return HttpResponseRedirect(reverse(
            'my_admin:category_products',
            kwargs={'category_pk': obj.category.pk}
        ))

    context = {
        'page_title': 'продукты/удаление',
        'object': obj,
    }
    return render(request, 'adminapp/product_delete.html', context)


class ProductDetail(PageTitleMixin, DetailView):
    page_title = 'Продукт'
    model = Product
    pk_url_kwarg = 'product_pk'
    context_object_name = 'product'
