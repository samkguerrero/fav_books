from django.shortcuts import render, redirect
from apps.books.models import Book
from apps.log_reg.models import User

# Create your views here.
def index(request):
    if 'logged_in_user' in request.session:
        me = User.objects.get(id=request.session['logged_in_user_id'])
        context = {
            "all_books_home": Book.objects.all(),
            "all_books_liked_by_me": Book.objects.filter(users_who_like_this_book=me),
            "all_books_not_liked_by_me": Book.objects.exclude(users_who_like_this_book=me),
        }
        return render(request, "books/index.html", context)
    else:
        return redirect("/")

def books(request, book_id):
    book_to_lookup = Book.objects.get(id=book_id)
    logged_in_user_fav_book = False
    for i in book_to_lookup.users_who_like_this_book.all():
        if int(request.session['logged_in_user_id']) == int(i.id):
            logged_in_user_fav_book = True
    context = {
        'book_to_show': book_to_lookup,
        'users_who_like_book': User.objects.filter(books_liked=book_to_lookup),
        'logged_in_user_fav_book': logged_in_user_fav_book
    }
    if request.session['logged_in_user_id'] == book_to_lookup.one_user_who_uploaded_this_book.id:
        return render(request, "books/edit_book.html", context)
    else:
        return render(request, "books/view_book.html", context)
###################################################
def add_book(request):
    if request.method == "POST":
        print("*"*100)
        print(request.POST)
        user_adding_book = User.objects.get(id=int(request.POST['id_of_user_creating_book']))
        Book.objects.create(
            title=request.POST['title'],
            desc=request.POST['desc'],
            one_user_who_uploaded_this_book=user_adding_book,
        )
        return redirect("/")
###################################################
def user_fav_a_book(request):
    if request.method == "POST":
        print(request.POST)
        book_bieng_favorited = Book.objects.get(id=request.POST['book_to_favorite_from_home'])
        user_favorite_a_book = User.objects.get(id=request.POST['user_at_home_favorite_a_book'])
        user_favorite_a_book.books_liked.add(book_bieng_favorited)
        return redirect("/books/" + str(book_bieng_favorited.id))

def user_update_book(request):
    if request.method == "POST":
        print("UPDATE"*100)
        updating_this_book = Book.objects.get(id=request.POST['book_to_update'])
        updating_this_book.title = request.POST['title']
        updating_this_book.desc = request.POST['desc']
        updating_this_book.save()
        return redirect("/books/" + request.POST['book_to_update'])

def user_delete_book(request):
    if request.method == "POST":
        book_to_delete = Book.objects.get(id=request.POST['book_to_delete_id'])
        if int(request.POST['user_delete_book_id']) == int(book_to_delete.one_user_who_uploaded_this_book.id):
            book_to_delete.delete()
        return redirect("/books")

def user_un_fav_book(request):
    if request.method == "POST":
        print(request.POST)
        book_bieng_unfavorited = Book.objects.get(id=request.POST['book_bieng_unfavorited'])
        user_unfavorited_book = User.objects.get(id=request.POST['user_unfavorited_book'])
        user_unfavorited_book.books_liked.remove(book_bieng_unfavorited)
        return redirect("/books/" + str(request.POST['book_bieng_unfavorited']))