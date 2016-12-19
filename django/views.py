from django.shortcuts import render
from django.http import HttpResponse

#request variable recieves the an possible POST or GET command from the user
def main_page(request):
    output ='''
        <html>
            <head><title>%s</p>
        </body>
    </html>
    ''' % (
        'Django Bookmarks',
        'Welcome To Django Bookmarks',
        'Where you can store bookmarks!'
    )
    return HttpResponse(output)
# Create your views here.
