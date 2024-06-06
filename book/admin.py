from django.contrib import admin

from book.models import category,Book, Order, Feedback

class BookAdmin(admin.ModelAdmin):
    list_display= ('title', 'author','price','is_available')
    search_fields = ('title',)
    list_editable = ('is_available',)
    list_filter = ('is_available','category')
class OrderAdmin(admin.ModelAdmin):
    list_display= ('user', 'book','quantity','status')
    search_fields = ('user','book')
    list_editable = ('status', )
    list_filter = ('status', )



# letting admin know that theres a category

admin.site.register(category)
admin.site.register(Feedback)
admin.site.register(Book, BookAdmin)
admin.site.register(Order, OrderAdmin)
# the things we want to see in the admin side