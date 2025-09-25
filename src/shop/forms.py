from django import forms
from .models import Rating 

class ProductFilterForm(forms.Form):
    search = forms.CharField(
        required=False,
        label="جستجو",
        widget=forms.TextInput(attrs={
            "placeholder": "نام محصول...",
            "class": "form-control text-end ",
            "id": "search"
        })
    )
    min_price = forms.IntegerField(
        required=False,
        label="حداقل قیمت",
        widget=forms.NumberInput(attrs={
            "placeholder": "حداقل",
            "class": "form-control text-end",
            "id": "min_price"
        })
    )
    max_price = forms.IntegerField(
        required=False,
        label="حداکثر قیمت",
        widget=forms.NumberInput(attrs={
            "placeholder": "حداکثر",
            "class": "form-control text-end",
            "id": "max_price"
        })
    )
    availability = forms.ChoiceField(
        required=False,
        label="وضعیت موجودی",
        choices=[
            ("", "همه"),
            ("available", "موجود"),
            ("unavailable", "ناموجود")
        ],
        widget=forms.Select(attrs={
            "class": "form-select text-end",
            "id": "availability"
        })
    )


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['score', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-control',
                'placeholder': 'نظر خود درباره این محصول بنویسید...'
            }),
        }
        labels = {
            'score': 'امتیاز',
            'comment': 'نظر (اختیاری)',
        }
        error_messages = {
            'score': {
                'required': 'لطفاً به محصول امتیاز دهید.',
                'min_value': 'حداقل امتیاز 1 است.',
                'max_value': 'حداکثر امتیاز 5 است.',
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['score'].widget = forms.HiddenInput()