
from django import forms
from myapp.models import Order, Review, Member

class SearchForm(forms.Form):
    CATEGORY_CHOICES = [
        ('S', 'Scinece&Tech'),
        ('F', 'Fiction'),
        ('B', 'Biography'),
        ('T', 'Travel'),
        ('O', 'Other')
    ]
    name = forms.CharField(max_length=100, required=False, label='Your name')
    category = forms.ChoiceField(widget=forms.RadioSelect,choices = CATEGORY_CHOICES, required=False, label='Select a category')
    max_price = forms.IntegerField(label='Maximum Price', min_value=0, required=True)

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['books', 'member', 'order_type']
        widgets = {'books': forms.CheckboxSelectMultiple(), 'order_type':forms.RadioSelect}
        labels = {'member': u'Member name', }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['reviewer', 'book', 'comments', 'rating']
        widgets = {'book': forms.RadioSelect()}
        labels = {
            'reviewer': u'Please enter a valid email',
            'rating': u'Rating: An integer between 1 (worst) and 5 (best)'
        }

class MemberForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Member
        fields = ['first_name', 'last_name', 'email', 'username', 'status', 'address', 'city', 'province']
        widgets = {'address': forms.Textarea(attrs={'rows': 2})}

    def clean(self):
        cleaned_data = super().clean()
        passw = cleaned_data['password']