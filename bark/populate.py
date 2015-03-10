import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bark.settings')

import django
import random
from django.contrib.auth import get_user_model
django.setup()

#TODO import correct models here.
from bark.models import UserProfile, Comment, Post, User, Tag, InstitutionTag, UserTag

usernames = [
                #Admins (US)
                "lDicks",
                "SCOTPAUL",
                "mmckay99",
                "projectgoav",

                #Standard Users
                "bat_man_fan123",
                "leifAzz",
                "stuck_student55",
                "johnno94",
                "barry_the_bear",
                "xXDragonMasterXx",
                "gla.Noob.com",
                "bersty",
                "ghastly"
            ]

tags =  [
            #Special Tags
            "@admin",
            "@bark",
            "@all",
            "@open",

            #Random Tags
            "@CS",
            "@Computing",
            "@leif",
            "@twd",
            "@artsandcrafts",
            "@c++",
            "@CS-1P",
            "@WAD2",
            "@JOOSE",
            "@Maths-2P",
            "@matrix",
            "@codegolf",
            "@python",
            "@python-lists",
            "@help",
            "@java",
        ]

sites = [
            #Institution tags
            "@gla.ac.uk",
            "@bristol.ac.uk",
            "@sta.ac.uk",
            "@edu.ac.uk",
            "@uws.ac.uk",
            "@cityofglasgowcollege.ac.uk",

        ]





#Adds some users to the application
#NOTE: These user passwords do not have any password hashing!
#NOTE: They all have the same password (test)
def addUsers():

    print "Adding users and their tags..."
    val = 0

    for user in usernames:

        print "\t> " + user

        if (val % 2 == 0):
            email = user + "@student.gla.ac.uk"
        else:
            email = user + "@bristol.ac.uk"

        val += 1
        u = User.objects.get_or_create(username=user, password="test", email = email)

        userTagName = "@" + user

        ut = UserTag.objects.get_or_create(name=userTagName)


    print str(len(usernames)) + " useres added!\n"


#Adds some basic information to the users and their profiles.
def addProfiles():

    print "Setting up User Profiles..."

    for user in usernames:
        u = User.objects.get(username=user)
        print "\t> " + str(u)

    print "Updated all profiles\n"


#Add all tags and a short descripton
#NOTE: Add tags have the default descriptno "A tag all about: "
def addTags():
    print "Creating tags..."

    for tag in tags:
        print "\t > " + tag
        t = Tag.objects.get_or_create(name=tag)

    print str(len(tags)) + " tags added!\n"

    print "Setting up institution tags..."

    for site in sites:
        print "\t> " + site
        st = InstitutionTag.objects.get_or_create(name=site)

    print "Institution tags setup.\n"


def populate():

    addUsers()
    addTags()


    #addProfiles()

    #for u in User.objects.all():
    #    print u


# Start execution here!
if __name__ == '__main__':
    print "Starting Bark population script..."

    populate()

    print "Ending..."
