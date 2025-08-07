from django import forms

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