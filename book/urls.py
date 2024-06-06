from django.urls import path
from book.views import all_books, book_details,category_books,add_to_cart,cart, remove_from_cart,check_out, place_order, orders, add_feedback
urlpatterns=[
    path("", all_books, name="all_books"),
    path("<int:id>/", book_details, name="book_details"),
    path("category/<int:cid>/", category_books, name="book_category"),
    path("add_to_cart", add_to_cart, name="add_to_cart"),
    path("cart/", cart , name="cart"),
    path("remove_from_cart/<int:id>", remove_from_cart , name="remove_from_cart"),
    path("check_out/", check_out , name="check_out"),
    path("place_order/", place_order , name="place_order"),
    path("orders/", orders , name="orders"),
    path("add_feedback/", add_feedback , name="add_feedback"),
    # id in <> is variable which is dynamically changable

]