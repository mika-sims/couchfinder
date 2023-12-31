from .models import Review
from django import forms


class ReviewForm(forms.ModelForm):
    """
    Form for creating a review
    """

    class Meta:
        model = Review
        fields = ("content",)
        widgets = {
            "content": forms.Textarea(
                attrs={"rows": 3, "placeholder": "Write your review here..."}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["content"].label = ""
