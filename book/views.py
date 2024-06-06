from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.conf import settings
from book.models import Book, category, Order, Feedback
from user.models import Address

from django.template.loader import render_to_string #with html tags and evrything
from django.utils.html import strip_tags #returns only string
from datetime import date, timedelta #to add things like 7days


def all_books(request):
    books = Book.objects.all()
    categories = category.objects.all().order_by('category')
    # print(books.query)
    context ={
        "books" : books,
        "categories":categories
    }
    return render(request, "book/books.html",context)

def book_details(request, id):
    # book=Book.objects.get(id=id)
    book = get_object_or_404(Book, id=id)
    feedbacks = Feedback.objects.filter(book=book)
    quantity = 1
    if request.session.get("cart_items"):
        if request.session.get('cart_items').get(str(id)):
            quantity = request.session.get("cart_items")[str(id)]
    context={
        "book" : book,
        "quantity": quantity,
        "feedbacks" : feedbacks,
    }
    return render(request, "book/book.html",context)

def category_books(request,cid):
    books = Book.objects.filter(category=cid)
    categories = category.objects.all().order_by('category')
    # print(books.query)
    context ={
        "books" : books,
        "categories":categories
    }
    return render(request, "book/books.html",context)


def add_to_cart(request):
    if request.method == "POST":
        book_id = request.POST.get("book_id")
        quantity = request.POST.get("quantity")
        cart_items={}
        if request.session.get("cart_items"):
            cart_items= request.session.get("cart_items")
        cart_items[book_id] = quantity
        request.session["cart_items"]=cart_items
        print(request.session.get("cart_items"))
    return redirect("cart")


# def get_cart_details(request):
#     cart_items = request.session.get('cart_items')


def cart(request):
    cart_details, total_price = get_cart_details(request)
    context={
        "books":cart_details,
        "total_price":total_price
    }
    return render(request, 'book/cart.html',context)


# to input multiple objects
def place_order(request):
    if request.method == "POST":
        user = request.user
        address= request.POST.get("address")
        address = Address.objects.get(id=address)
        payment_mode = request.POST.get("payment_mode")
        cart_details, total_price = get_cart_details(request)
        orders = []
        for book in cart_details:
            order = Order(
                book = Book.objects.get(id=book['id']),
                user = user,
                address = address,
                quantity = book['quantity'],
                price = book['price'],
                payment_method = payment_mode
            )
            orders.append(order)
        Order.objects.bulk_create(orders)

        mail_context={
            "username" : request.user.first_name+" "+request.user.last_name,
            "books": cart_details,
            "address": address,
            "delivery_date": date.today() + timedelta(days=7),
            "total_price":total_price
        }
        subject = "Order is placed successfully"
        # body = f"Your Order is placed successfully. Amount {total_price}. Will be delivered to Address: {address}" 
        html_message = render_to_string('book/mail_template.html',mail_context)
        plain_message = strip_tags(html_message)
        to= [request.user.email,]
        from_email = settings.EMAIL_HOST_USER
        # send_mail(subject=subject, message=body, from_email=from_email, recipient_list=to, fail_silently=False)
        send_mail(subject=subject, message=plain_message, from_email=from_email, recipient_list=to, fail_silently=False, html_message=html_message)


        request.session['cart_items']={}
        return redirect('all_books')


def orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-id') # will fetch by reverse order of id
    context = {
        "orders": orders
    }
    return render(request, 'book/orders.html',context)



def get_cart_details(request):
    total_price=0
    cart_details=[]
    if not request.session.get('cart_items'):
        return cart_details, total_price
    cart_items = request.session.get('cart_items')
    books = Book.objects.filter(id__in=list(cart_items.keys())) #getting the keys from dictionary
    for book in books:
        quantity = int(cart_items[str(book.id)])
        price = quantity*book.price
        total_price += price
        cart_details.append({
            "id": book.id,
            "title": book.title,
            "quantity": quantity,
            "price": price,
            "image":book.image
        })
    return cart_details,total_price

def remove_from_cart(request, id):
    cart_items= request.session.get('cart_items')
    del cart_items[str(id)]
    request.session['cart.items'] = cart_items
    return redirect("cart")

def check_out(request):
    addresses = Address.objects.filter(user=request.user)
    cart_details, total_price = get_cart_details(request)
    context = {
        "addresses":addresses,
        "books":cart_details,
        "total_price":total_price
    }
    return render(request, 'book/check_out.html', context)

'''
according to industry standard every function show have a docstring defined
purpose
input
return
'''
def add_feedback(request):
    if request.method == "POST":
        user = request.user
        book_id = request.POST.get("book_id")
        book = Book.objects.get(id=book_id)
        rating =  request.POST.get("rating")
        comment =  request.POST.get("comment")
        feedback = None
        # keep try and except block in the email form too
        try:
            feedback = Feedback.objects.get(user=user, book=book)
        except:
            print("Feedback not available")
        if feedback is None:
            feedback = Feedback()
            feedback.user = user
            feedback.book = book
        feedback.rating = rating 
        feedback.comment = comment
        feedback.save()
        return redirect('orders')

