from django.shortcuts import render, HttpResponse, redirect

from .forms import LoginForm, SignupForm
from .models import Book, User, Loan
from datetime import date, timedelta
from django.contrib.auth import authenticate, login, logout

def listBooks(request):
    allBooks = Book.objects.all()
    return render(request, 'books.html', {'books':allBooks, 'option':'All books', 'count':len(allBooks)})

def listAvailable(request):
    #Set up dictionary with count of all books in library
    allBooks = Book.objects.all()
    bookCount = dict()
    for each in allBooks:
        if each.quantity>0:
            bookCount[each] = each.quantity
    #Count number of each book loaned out; this gives available books.
    listOfLoans = Loan.objects.all()
    for loan in listOfLoans:
        book = loan.bookID
        if book in bookCount:    
            if bookCount[book] <= 1:
                del bookCount[book]
            else:
                bookCount[book] -=1
        print(book)
            
    #Keys = objects = available books
    availableBooks = bookCount.keys()

    #Check if the book has been borrowed by current user
    myLoans = Loan.objects.filter(userID=request.user)
    currentLoans = dict()
    for each in myLoans:
        currentLoans[each.bookID] = each.returnDate.isoformat()


    return render(request, 'books.html', {'books': availableBooks, 'option':'Available books', 'count':len(availableBooks), 'currentLoans':currentLoans})

#View for books that are currently on Loan
def listOnLoan(request):
    onLoan = Loan.objects.all()
    loans = []

    books = []
    for loan in onLoan:
        book = loan.bookID
        books.append(book)
        borrowerID = loan.userID
        borrower = User.objects.get(email=borrowerID)
        returnDate = loan.returnDate
        loans.append(
            {'firstname':borrower.firstname,
             'lastname':borrower.lastname,
             'email':borrowerID,
             'bookTitle':book.title,
             'return': returnDate,
             'image': book.imageUrl}
        )
    
    return render(request, 'books.html', {'books':books, 'loans':loans, 'option':'Books on loan','count':len(loans)})

#View for books due today
def listDueToday(request):
    onLoan = Loan.objects.all()
    dueToday = []
    for loan in onLoan:
        book = loan.bookID
        if loan.returnDate.isoformat() == date.today().isoformat():
            dueToday.append(book)
        print(loan.returnDate, date.today().isoformat())
    return render(request, 'books.html', {'books':dueToday, 'option':'Books due today', 'count':len(dueToday)})


#Helper function to display correct view based on filter selected
def processOption(request):
     if request.method == 'POST':
        selected_option = request.POST.get('option', None)
        # All books
        if selected_option == 'option1':
            return redirect('listBooks')
        # All available to borrow
        elif selected_option == 'option2':
            return redirect('listAvailable')
        # All currently on loan
        elif selected_option == 'option3':
            return redirect('listOnLoan')
        # All due today
        elif selected_option == 'option4':
            return redirect('listDueToday')

#Helper function to create an entry for a borrowed book for current user
def borrowBook(request):
    selectedBookID = request.POST.get('book')
    currentUser = request.user
    book = Book.objects.get(pk=selectedBookID)

    defaultReturnDate = date.today() + timedelta(days=7)
    if Loan.objects.filter(bookID=book,userID=currentUser):
        return HttpResponse(f'You have already borrowed this book.')
    Loan.objects.create(bookID = book, userID = currentUser, returnDate = defaultReturnDate)
    return redirect('listAvailable')

#View for signup + signup entry into db
def signupView(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {'form': SignupForm})
    form = SignupForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('loginView')
    return HttpResponse(f'Invalid signup.')

#View for login + login functionality
def loginView(request):
    if request.method == 'GET':
        return render(request, 'login.html', {'form': LoginForm})
    form = LoginForm(request.POST)
    if form.is_valid():
        username = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(request, email=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
    return redirect('loginView')

#Logout function
def logoutView(request):
    logout(request)
    return redirect('loginView')

#Main page
def index(request):
    return render(request, 'index.html')
