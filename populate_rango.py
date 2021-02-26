import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','tango_with_django_project.settings')

import django
django.setup()
from rango.models import Category, Page

def populate():

    python_pages = [
        {"title": "Official Python Tutorial",
        "url":"http://docs.python.org/2/tutorial/",
        "views":"20"},
        {"title":"How to Think like a Computer Scientist",
        "url":"http://www.greenteapress.com/thinkpython/",
        "views":"20"},
        {"title":"Learn Python in 10 Minutes",
        "url":"http://www.korokithakis.net/tutorials/python/",
        "views":"11"} 
        ]

    django_pages =[
        {"title":"Official Django Tutorial",
        "url":"https://docs.djangoproject.com/en/1.9/intro/tutorial01/",
        "views":"10"},
        {"title":"Django Rocks",
        "url":"http://www.djangorocks.com/",
        "views":"33"},
        {"title":"How to Tango with Django",
        "url":"http://www.tangowithdjango.com/",
        "views":"101"}
    ]

    other_pages=[
        {"title":"Bottle",
        "url":"http://bottlepy.org/docs/dev/",
        "views":"22"},
        {"title":"Flask",
        "url":"http://flask.pocoo.org",
        "views":"10"} ]

    cats = {"Python": {"pages": python_pages,'likes':128,'views':64},"Django": {"pages": django_pages,'likes':28,'views':14},"Other Frameworks": {"pages": other_pages,'likes':14,'views':7} }

    for cat, cat_data in cats.items():
        c = add_cat(cat,cat_data['likes'],cat_data['views'])
        for p in cat_data["pages"]:
            add_page(c, p["title"], p["url"], p["views"])

#Print out the categories we have added.
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print("- {0} - {1}".format(str(c), str(p)))

def add_page(cat, title, url, views=0):
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url=url
    p.views=views
    p.save()
    return p

def add_cat(name,likes,views):
    c = Category.objects.get_or_create(name=name)[0]
    c.likes=likes
    c.views=views
    c.save()
    return c

 # Start execution here!
if __name__ == '__main__':
    print("Starting Rango population script...")
    populate()
