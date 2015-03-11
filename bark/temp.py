import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bark.settings')

import django
django.setup()

#TODO import correct models here.
from bark.models import UserProfile, Comment, Post,


#Adds some users to the application
def addUsers():

    u = User.objects.get_or_create(username="bat_man_fan123", password="test", email="bat_man_fan_123@student.gla.ac.uk")



    #u = User.objects.createsuperuser

def add_User(user, tags):
        u = UserProfile.objects.get_or_create(user=user, followed_tags=tags)[0]
        return u



def populate():
    python_cat = add_cat('Python',128,64)

    add_page(cat=python_cat,
        title="Official Python Tutorial",
        url="http://docs.python.org/2/tutorial/",
        views=2)

    add_page(cat=python_cat,
        title="How to Think like a Computer Scientist",
        url="http://www.greenteapress.com/thinkpython/",
        views=12)

    add_page(cat=python_cat,
        title="Learn Python in 10 Minutes",
        url="http://www.korokithakis.net/tutorials/python/",
        views=33)

    django_cat = add_cat("Django",64,32)

    add_page(cat=django_cat,
        title="Official Django Tutorial",
        url="https://docs.djangoproject.com/en/1.5/intro/tutorial01/")

    add_page(cat=django_cat,
        title="Django Rocks",
        url="http://www.djangorocks.com/")

    add_page(cat=django_cat,
        title="How to Tango with Django",
        url="http://www.tangowithdjango.com/",
        views=50)

    frame_cat = add_cat("Other Frameworks")

    add_page(cat=frame_cat,
        title="Bottle",
        url="http://bottlepy.org/docs/dev/")

    add_page(cat=frame_cat,
        title="Flask",
        url="http://flask.pocoo.org")


    #Chapter 6 : Extensions
    student_cat = add_cat("Ewan")

    add_page(cat=student_cat,
        title="Github",
        url="https://github.com/projectgoav",
        views=100
        )

    add_page(cat=student_cat,
        title="Python Anywhere",
        url="https://www.pythonanywhere.com/user/projectgoav",
        views = 20
        )

    # Print out what we have added to the user.
    for c in Category.objects.all():

        #Debug for adding likes and views
        #print 'Views:' + str(c.views)
        #print 'Likes:' + str(c.likes)

        for p in Page.objects.filter(category=c):
            print "- {0} - {1}".format(str(c), str(p))

def add_page(cat, title, url, views=0):
    p = Page.objects.get_or_create(category=cat, title=title, url=url, views=views)[0]
    return p

def add_cat(name, views=0, likes=0):
    c = Category.objects.get_or_create(name=name, views=views, likes=likes)[0]
    return c


# Start execution here!
if __name__ == '__main__':
    print "Starting Bark population script..."


    print "Ending..."
    #populate()
