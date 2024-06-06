from django.urls import path

from pages import views
urlpatterns =[
    path("", views.index, name="index"),
    path("about", views.aboutus, name="aboutus")
]

# name= if ever django want to call then it will use 'name' and it shall be always unique throughout
# "" => this url is for user