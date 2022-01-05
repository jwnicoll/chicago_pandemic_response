from django.shortcuts import render

posts = [
    {
        'author': 'LL',
        'title': 'Test Post 1',
        'content': 'qwertyuiop',
        'date_posted': '2021'
    },
    {
        'author': 'JC',
        'title': 'Test Post 2',
        'content': 'asdfghjkl',
        'date_posted': '2021'
    }
]


def home(request):
    context = {
        'posts': posts
    }
    return render(request, 'blog/home.html', context)


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})