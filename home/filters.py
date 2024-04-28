import django_filters
from django import forms

from home.models import Product, Category


class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', label='Name', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Please enter name'}))
    description = django_filters.CharFilter(lookup_expr='icontains', label='Description', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Please enter description'}))

    category = django_filters.ModelChoiceFilter(label='Category', field_name='category',
                                                queryset=Category.objects.all(),
                                                widget=forms.Select(attrs={'class': 'form-select'}))

    price_gte = django_filters.NumberFilter(field_name='price', lookup_expr='gte',
                                            widget=forms.NumberInput(
                                                attrs={'class': 'form-control', 'type': 'number',
                                                       'placeholder': 'Please enter minimum price'}))

    price_lte = django_filters.NumberFilter(field_name='price', lookup_expr='lte',
                                            widget=forms.NumberInput(
                                                attrs={'class': 'form-control', 'type': 'number',
                                                       'placeholder': 'Please enter maximum price'}))

    created_date_gte = django_filters.DateFilter(field_name='created', lookup_expr='gte',
                                                 widget=forms.DateInput(
                                                     attrs={'class': 'form-control', 'type': 'date'}))

    created_date_lte = django_filters.DateFilter(field_name='created', lookup_expr='lte',
                                                 widget=forms.DateInput(
                                                     attrs={'class': 'form-control', 'type': 'date'}))


    YES_OR_NO = (
        (True, 'Yes'),
        (False, 'No')
    )

    active = django_filters.BooleanFilter(
        field_name='is_active',
        label='Product is active:',
        widget=forms.RadioSelect(choices=YES_OR_NO, attrs={'class': 'form-check-inline'})
    )

    sort_by = django_filters.ChoiceFilter(
        label='Sort by',
        choices=[
            ('price_asc', 'Price (Low to High)'),
            ('price_desc', 'Price (High to Low)'),
            ('alphabetical_asc', 'Alphabetical (A to Z)'),
            ('alphabetical_desc', 'Alphabetical (Z to A)'),
            ('created_at_asc', 'Created Date (Oldest to Newest)'),
            ('created_at_desc', 'Created Date (Newest to Oldest)'),
        ],
        method='filter_sort_by',
        widget=forms.Select(attrs={'class': 'form-select custom-select'})
    )

    def filter_sort_by(self, queryset, name, value):
        sort_options = {
            'price_asc': 'price',
            'price_desc': '-price',
            'alphabetical_asc': 'name',
            'alphabetical_desc': '-name',
            'created_at_asc': 'created',
            'created_at_desc': '-created',
        }
        return queryset.order_by(sort_options.get(value, 'id'))

    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'price_gte', 'price_lte', 'created_date_gte', 'created_date_lte',
                  'active']
