from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView
from django.forms import ModelForm

from ..utils import BreadcrumbMixin

from .models import Book
from .forms import BookForm, SingleFieldFormMixin


def get_forms(data=None, obj=None):
    data = {} if data is None else data
    forms = {}
    for Form in SingleFieldFormMixin.__subclasses__():
        kwargs = {}
        #if isinstance(Form, ModelForm):
        kwargs['instance'] = obj
        if Form.fieldname in data:
            kwargs['data'] = data
        form = Form(**kwargs)
        forms[form.fieldname] = form
    return forms


class ConvenienceMixin(BreadcrumbMixin):
    def get_context_data(self, **kwargs):
        subtype = self.subtype if self.subtype else ''
        page_title = f': {subtype}' if subtype else ''
        misc = self.get_misc_fields()
        return super().get_context_data(
            subtype=subtype,
            page_title=page_title,
            misc=misc,
            **kwargs,
        )

    def get_misc_fields(self):
        misc = []
        for fieldname, form in get_forms().items():
            if form.json_backed:
                misc.append(fieldname)
        return misc

    def get_success_url(self):
        if hasattr(self, 'success_url'):
            return reverse(self.success_url)
        return ''

    def get_breadcrumbs(self):
        super().get_breadcrumbs()
        breadcrumb = (reverse(self.success_url), self.subtype)
        return self.add_final_breadcrumb(breadcrumb)

    def add_final_breadcrumb(self, breadcrumb):
        if self.subtype in breadcrumb[0] and not breadcrumb in self.breadcrumbs:
            self.breadcrumbs.append(breadcrumb)
        return self.breadcrumbs


class ClassicMixin:
    subtype: str = 'multifield'
    success_url = 'book-list'


class SingleFieldMixin:
    subtype: str = 'singlefield'
    success_url = 'book-list2'


class HTMxSingleFieldMixin:
    subtype: str = 'singlefield-htmx'
    success_url = 'book-list3'


class ListBookView(ClassicMixin, ConvenienceMixin, ListView):
    model = Book


class SinglefieldListBookView(SingleFieldMixin, ConvenienceMixin, ListView):
    model = Book
    template_name = 'singlefield_app/book_list2.html'


class HTMxSinglefieldListBookView(HTMxSingleFieldMixin, SinglefieldListBookView):
    template_name = 'singlefield_app/book_list3.html'


class CreateBookView(ClassicMixin, ConvenienceMixin, CreateView):
    model = Book
    form_class = BookForm

    def get_breadcrumbs(self):
        super().get_breadcrumbs()
        breadcrumb = (reverse('book-new'), 'Add new')
        return self.add_final_breadcrumb(breadcrumb)


class SinglefieldCreateBookView(SingleFieldMixin, ConvenienceMixin, CreateView):
    model = Book
    fields = '__all__'
    template_name = 'singlefield_app/book_form2.html'

    def get_forms(self):
        return get_forms(data=self.request.POST)

    def get_context_data(self, **kwargs):
        forms = self.get_forms()
        return super().get_context_data(forms=forms, **kwargs)

    def get_breadcrumbs(self):
        super().get_breadcrumbs()
        breadcrumb = (reverse('book-new2'), 'Add new')
        return self.add_final_breadcrumb(breadcrumb)


class HTMxSinglefieldCreateBookView(HTMxSingleFieldMixin, SinglefieldCreateBookView):

    def get_breadcrumbs(self):
        super().get_breadcrumbs()
        breadcrumb = (reverse('book-new3'), 'Add new')
        return self.add_final_breadcrumb(breadcrumb)


class DeleteBookView(ClassicMixin, ConvenienceMixin, DeleteView):
    model = Book

    def get_breadcrumbs(self):
        super().get_breadcrumbs()
        breadcrumb = (
            reverse('book-delete', kwargs={'pk': self.kwargs['pk']}),
            'Delete',
        )
        return self.add_final_breadcrumb(breadcrumb)


class SinglefieldDeleteBookView(SingleFieldMixin, DeleteBookView):
    def get_breadcrumbs(self):
        super().get_breadcrumbs()
        breadcrumb = (
            reverse('book-delete2', kwargs={'pk': self.kwargs['pk']}),
            'Delete',
        )
        return self.add_final_breadcrumb(breadcrumb)


class HTMxSinglefieldDeleteBookView(HTMxSingleFieldMixin, SinglefieldDeleteBookView):
    def get_breadcrumbs(self):
        super().get_breadcrumbs()
        breadcrumb = (
            reverse('book-delete3', kwargs={'pk': self.kwargs['pk']}),
            'Delete',
        )
        return self.add_final_breadcrumb(breadcrumb)


class UpdateBookView(ClassicMixin, ConvenienceMixin, UpdateView):
    model = Book
    form_class = BookForm

    def get_breadcrumbs(self):
        super().get_breadcrumbs()
        breadcrumb = (
            reverse('book-edit', kwargs={'pk': self.kwargs['pk']}),
            'Edit',
        )
        return self.add_final_breadcrumb(breadcrumb)


class SinglefieldUpdateBookView(SingleFieldMixin, ConvenienceMixin, UpdateView):
    model = Book
    fields = '__all__'
    template_name = 'singlefield_app/book_edit.html'

    def get_forms(self):
        instance = self.get_object()
        return get_forms(data=self.request.POST, obj=instance)

    def get_context_data(self, **kwargs):
        forms = self.get_forms()
        return super().get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        forms = self.get_forms()
        valid = False
        for form in forms.values():
            if form.is_bound and form.is_valid():
                valid = True
        if valid:
            return self.form_valid(forms)
        return self.form_invalid(forms)

    def form_valid(self, forms):
        for fieldname, form in forms.items():
            if not (form.is_bound and form.is_valid()):
                continue
            form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_breadcrumbs(self):
        super().get_breadcrumbs()
        breadcrumb = (
            reverse('book-edit2', kwargs={'pk': self.kwargs['pk']}),
            'Edit',
        )
        return self.add_final_breadcrumb(breadcrumb)


class HTMxSinglefieldUpdateBookView(HTMxSingleFieldMixin, SinglefieldUpdateBookView):
    template_name = 'singlefield_app/book_edit.html'

    def get_breadcrumbs(self):
        super().get_breadcrumbs()
        breadcrumb = (
            reverse('book-edit2', kwargs={'pk': self.kwargs['pk']}),
            'Edit',
        )
        return self.add_final_breadcrumb(breadcrumb)


class SinglefieldGetBookFieldView(SingleFieldMixin, DetailView):
    model = Book
    template_name = 'singlefield_app/book_field_form.html'

    def get_forms(self):
        instance = self.get_object()
        return get_forms(data=request.POST, obj=instance)

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        forms = get_forms(obj=self.object)
        fieldname = self.kwargs["fieldname"]
        form = forms[fieldname]
        context = super().get_context_data(fieldname=fieldname, form=form, **kwargs)
        return context


class HTMxSinglefieldGetBookFieldView(HTMxSingleFieldMixin, SinglefieldGetBookFieldView):
    template_name = 'singlefield_app/_book_field_form.html'
