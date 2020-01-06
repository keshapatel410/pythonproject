from django.contrib import admin
from.models import Publisher, Book, Member, Order, Review
from django.db.models import F

def tax (model, req, query):
    query.update(price=F('price') + 10)
tax.short_description = "Add $10 to current price of books"

class BookAdmin(admin.ModelAdmin):
    fields = [('title', 'category', 'publisher'), ('num_pages', 'price', 'num_reviews')]
    list_display = ('title', 'category', 'price')
    actions = [tax]

class OrderAdmin(admin.ModelAdmin):
    fields = [('books'), ('member', 'order_type', 'order_date')]
    list_display = ('id', 'member', 'order_type', 'order_date', 'total_items')

class PublisherAdmin(admin.ModelAdmin):
    fields = [('name', 'website'), ('city', 'country')]
    list_display = ('name','city')

class MemberAdmin(admin.ModelAdmin):
    fields = [('first_name','last_name'),('status'),('borrowed_books'),'image','password']
    list_display = ('id','first_name','status','password')
    readonly_fields = ['image_tag']


admin.site.register(Publisher, PublisherAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Review)
