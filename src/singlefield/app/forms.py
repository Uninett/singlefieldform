from django import forms

from .models import Book


class BookForm(forms.ModelForm):
    template_name = 'django/forms/dl.html'
    class Meta:
        model = Book
        fields = '__all__'


class SingleFieldFormMixin:
    template_name = 'django/forms/dl.html'
    fieldname: str
    json_backed: bool

    def get_field(self):
        return self[self.fieldname]


class BookTitleForm(SingleFieldFormMixin, forms.ModelForm):
    fieldname = "title"
    json_backed = False

    class Meta:
        model = Book
        fields = ['title']


class BookAuthorForm(SingleFieldFormMixin, forms.ModelForm):
    fieldname = "author"
    json_backed = False

    class Meta:
        model = Book
        fields = ['author']


class BookYearForm(SingleFieldFormMixin, forms.ModelForm):
    fieldname = "year"
    json_backed = False

    class Meta:
        model = Book
        fields = ['year']


class TriviaForm(SingleFieldFormMixin, forms.Form):
    fieldname = "trivia"
    json_backed = True

    trivia = forms.CharField(widget=forms.Textarea)

    def __init__(self, instance=None, **kwargs):
        self.instance = instance
        if instance:
            value = self.instance.misc.get(self.fieldname, '')
            if value:
                kwargs['initial'] = {self.fieldname: value}

#         value = getattr(self.instance.misc, self.fieldname, '')
#         if value:
#             kwargs['initial'] = {'misc': self.instance.misc}
#                 kwargs.get('initial', {iself.fieldname: value})
        super().__init__(**kwargs)

    def save(self, **_):
        if self.is_valid():
            self.instance.misc[self.fieldname] = self.cleaned_data[self.fieldname]
            self.instance.save()
