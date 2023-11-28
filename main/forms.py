from django import forms

class BookSearchForm(forms.Form):
    book_title = forms.CharField(label='도서 이름', max_length=100)