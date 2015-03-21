import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bark.settings')

import django
import random

#TODO import correct models here.
from bark.models import UserProfile, Post, User, Tag, PostTagging, Comment

django.setup()

userNames = [
                # Admins
                "lDicks", "SCOTPAUL", "mmckay99", "projectgoav",

                # Standard Users
                "john335", "leif-tango", "stuck_student55", "charlie94",
                "179346852", "dragon-trainer", "chocolate-boy", "wehavemorefun",
                "ghastly", "test"
            ]

tags = [
            #Special Tags
            "admin", "bark", "all", "open",

            #Random Tags
            "CS", "Computing", "leif", "twd", "artsandcrafts", "c++",
            "CS-1P", "WAD2", "JOOSE", "Maths-2P", "matrix",
            "codegolf", "python", "python-lists", "help", "java",
            "c", "django", "php", "n-tier", "clientside", "server",
            "university", "ADS", "AF2", "AdvancedProgramming",
            "Sigma16"
        ]

institutionTags = [
            "gla.ac.uk",
            "bristol.ac.uk",
            "sta.ac.uk",
            "edu.ac.uk",
            "uws.ac.uk",
            "cityofglasgowcollege.ac.uk",
        ]

defaultPostData = [
    ["C++ Help", "Should I learn C or C++ first?"],
    ["Python Stuck", "What does the % operator mean in Python? I heard it means modulus for C++, is it the same?"],
    ["Django sucks", "I've been using Ruby on Rails and Ruby's functional programming is just so much easier than Python's."],
    ["Class banter", "Who would have guessed that he was eating a sandwich in AF2!"],
    ["Populate.py is hard", "I can't think of sample data for the population script- can I scrape data from Reddit?"],
    ["Stuck with Sigma16!", "How can I implement stacks in Sigma16? Is there a special operation type, like x86?"],
    ["Systems help", "I'm really stuck with Sigma16 and I can't find it on Google, does anyone know where I can get a copy from?"],
    ["Java sucks", "Why is everything a reference? And why are integer types autoboxed!?"],
    ["BinSort is tricky", "What's the advantage of binary sort over merge sort?"],
    ["Python 3 is way better than 2", "Print isn't a statement! This isn't BBC-BASIC, I'm glad Python is catching up with the more modern languages"],
    ["Differece between Java and Javascript?", "I have been taking a course in Java but it seems so different to JS, why doesn't \"var\" work in Java?"],
    ["ADS Lectures", "I've really been enjoying the ADS lectures, that example about the sailing competition was really interesting"],
    ["Bit lost with n-tier architectures", "Can anyone help me out?"],
    ["Did anyone hear Leif's joke this morning?!", "Something about alcohol- I found this really offensive."],
    ["Boyd Orr labs", "Isn't it great how they are open all the time?! I stay close to university and use them to book my holidays, bit cheeky, I know!"],
    ["First year student, bit lost", "I'm confused, do we need 120 credits for our whole year or just one semester? Cheers, Bob :)"],
    ["Check out this cool new language", "Haskell is a functional programming lanaguage and it's really great, but really hard to get my head around. Has anyone got any experience with it?"],
    ["Does anyone still use PHP?", "I once heard PHP called a 'write once, never read' lanaguge! Hilarous!"],
    ["Why is Django written in Python?", "Surely a compiled language such as Java or a functional language would suit the request-response paradigm better?"]
    ]

# Adds some users to the application
# NOTE: These user passwords do not have any password hashing!
# NOTE: They all have the same password (test)
def addUsers():
    print "Adding users and their tags..."
    selectedUserInstitution = 0

    for userName in userNames:
        print "\t> " + userName

        email = userName + "@" + institutionTags[selectedUserInstitution % len(institutionTags)]
        selectedUserInstitution += 1

        u = User.objects.get_or_create(username=userName, email=email)[0]
        u.set_password("test")
        u.save()
    print str(len(userNames)) + " users added!\n"

# Adds some basic information to the users and their profiles.
def addProfiles():
    print "Setting up User Profiles..."

    for userName in userNames:
        user = User.objects.get(username=userName)
        user_profile = UserProfile.objects.get_or_create(user=user)

        print "\t> " + str(user_profile)

    print "Updated all profiles\n"

# Add all tags and a short description
# Note: Add tags have the default description "A tag all about: "
def addTags():
    print "Creating tags..."

    for tag in tags:
        print "\t > " + tag
        Tag.objects.get_or_create(name=tag)

    print str(len(tags)) + " tags added!\n"


def addPosts():
    print "Creating posts..."

    allUsers = UserProfile.objects.all()
    userIndex = 0

    for postIndex in range(0, len(defaultPostData)):
        post_data = defaultPostData[postIndex % len(defaultPostData)]

        post = Post.objects.get_or_create(
            title=post_data[0],
            author=allUsers[userIndex % len(allUsers)],
            content=post_data[1],
            views=random.randint(0, 100)
            )[0]
        print "\t > " + str(post)
        userIndex += 1

        for i in range(random.randint(0, len(tags)-1)):
            PostTagging.objects.create(post=post, tag=Tag.objects.get(name=tags[i]))

        Comment.objects.create(author=allUsers[userIndex % len(allUsers)], post=post, content="This is a great post!")
        Comment.objects.create(author=allUsers[(userIndex + 1) % len(allUsers)], post=post, content="Agreed!")

    print str(len(defaultPostData)) + " posts added!\n"


def populate():
    addUsers()
    addProfiles()
    addTags()
    addPosts()

if __name__ == '__main__':
    print "Starting Bark population script..."
    populate()
    print "Ending..."
