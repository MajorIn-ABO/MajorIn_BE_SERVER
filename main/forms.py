from django import forms
from .models import Usedbooktrade


class BookSearchForm(forms.Form):
    book_title = forms.CharField(label='도서 이름', max_length=100)


class UsedBookTradeForm(forms.ModelForm):
    # 손상도 선택을 위한 필드
    DAMAGE_LEVEL_CHOICES = [
        ('없음', '손상도 없음'),
        ('조금있음', '손상도 조금있음'),
        ('많음', '손상도 많음'),
    ]
    damage_level = forms.ChoiceField(choices=DAMAGE_LEVEL_CHOICES, label='손상도')

    class Meta:
        model = Usedbooktrade
        fields = ['title', 'author', 'seller', 'publisher', 'price', 'imgfile', 'description', 'damage_level']