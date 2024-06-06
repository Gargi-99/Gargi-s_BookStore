from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm


# customising the builtin forms
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        # fields = __all_
        fields = {"first_name","last_name","username","email","password1","password2"}
        model=User
    
# class AddBookForm(ModelForm):
#     class Meta:
#         fields= "__all__"
        # model = Book
    