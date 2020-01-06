# Import necessary classes
from django.http import HttpResponse
from .models import Publisher, Book, Member, Order


# Create your views here.
def index(request):
    response = HttpResponse()
    booklist = Book.objects.all().order_by('id')[:10]
    publisherlist = Publisher.objects.all().order_by('-city')
    heading1 = '<p>' + 'List of available books: ' + '</p>'
    response.write(heading1)
    for book in booklist:
        para = '<p>' + str(book.id) + ': ' + str(book) + '</p>'
        response.write(para)

    for publisher in publisherlist:
        para = '<p>' + str(publisher.name) + ': ' + str(publisher.city) + '</p>'
        response.write(para)

    return response


def about(request):
    aboutResponse = HttpResponse()
    txtDisplay = '<p>' + 'This is an eBook APP' + '</p>'
    aboutResponse.write(txtDisplay)
    return aboutResponse

def detail(request, book_id):
    response = HttpResponse()
    booklist = Book.objects.all().order_by('id')[:10]
    for book in booklist:
        if book.id == book_id:
            para = '<p>' + 'Title: ' + str(book.title).upper() + ', Price: ' + '$' + str(book.price) + ', Publisher: ' + str(book.publisher)
            response.write(para)
    return response
