import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bark.settings')

import django
import random

#TODO import correct models here.
from bark.models import UserProfile, Post, User, Tag, PostTagging, Comment, CommentLike, PostLike

django.setup()

userNames = [
                # Admins
                "ldicks", "scotpaul", "mmckay99", "projectgoav",

                # Standard Users
                "john335", "leif-tango", "stuck_student55", "charlie94",
                "179346852", "dragon-trainer", "chocolate-boy", "wehavemorefun",
                "ghastly", "test"
            ]

tags = [
            #Special Tags
            "admin", "bark", "all", "open",

            #Random Tags
            "cs", "computing", "leif", "twd", "artsandcrafts", "c++",
            "cs-1p", "wad2", "joose", "maths-2p", "matrix",
            "codegolf", "python", "python-lists", "help", "java",
            "c", "django", "php", "n-tier", "clientside", "server",
            "university", "ads", "af2", "advanced_programming",
            "sigma16", "systems", "boredom", "javascript", "java-help",
            "code-help", "python-help", "coding-careers", "codemonkey",
            "banter", "lectures", "cs2t", "database", "postgre", "mysql",
            "sqlite", "sqlite3", "sql"
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
    ["C++ Help", "Should I learn C or C++ first?", ["I'd go with C first, as C++ is derived from C, it's a natural progression!:)", "C++: nobody uses C anymore", "Why not just learn BCPL?"]],
    ["Python Stuck", "What does the % operator mean in Python? I heard it means modulus for C++, is it the same?", ["I think it's also the modulus operator? Not 100% sure though as I think operators can be overloaded"]],
    ["Django sucks", "I've been using Ruby on Rails and Ruby's functional programming is just so much easier than Python's.", ["Django is amazing! Have you read Tango With Django? It really helped me understand the API"]],
    ["Class banter", "Who would have guessed that he was eating a sandwich in AF2!",["I know haha, hilarious!", "Thought it was a wrap?", "I didn't understand the lecture at all... too distracted! :P"]],
    ["Populate.py is hard", "I can't think of sample data for the population script- can I scrape data from Reddit?",[ "I think scraping data from websites is harder than you think- just be imaginative and come up with your own posts?"]],
    ["Stuck with Sigma16!", "How can I implement stacks in Sigma16? Is there a special operation type, like x86?", ["No idea, I don't think there is a special instruction", "No, it's a RISC instruction set", "What's RISC?"]],
    ["Systems help", "I'm really stuck with Sigma16 and I can't find it on Google, does anyone know where I can get a copy from?", ["No I think it's the lecturer's own project", "I saw someting similar on the MIT website?"]],
    ["Java sucks", "Why is everything a reference? And why are integer types autoboxed!?",["Java definetly does suck!", "I know right?! Why isn't there a &special syntax for references!"]],
    ["BinSort is tricky", "What's the advantage of binary sort over merge sort?", ["I think Binary Sort (and binary search?) can run in Log(n) times- although I'm not sure what that means", "I think n is the size of the data set?"]],
    ["Python 3 is way better than 2", "Print isn't a statement! This isn't BBC-BASIC, I'm glad Python is catching up with the more modern languages",["Yeah Python 3 RULES!:P", "Yeah in most languages it's a function", "I kind of liked Python 2..."]],
    ["Difference between Java and Javascript?", "I have been taking a course in Java but it seems so different to JS, why doesn't \"var\" work in Java?", ["In Java, variable types have to be declared, so you have to say 'Integer x'", "No idea, I thought they were the same thing!"]],
    ["ADS Lectures", "I've really been enjoying the ADS lectures, that example about the sailing competition was really interesting", ["Yeah! Wasn't it!", "It was a shame half the class didn't show up...","I really enjoy ADS, it's a more theory based course than WAD"]],
    ["Bit lost with n-tier architectures", "Can anyone help me out?", ["I think n-tier is where you can have many middleware units?", "Not sure- maybe ask @leif?"]],
    ["Did anyone hear Leif's joke this morning?!", "Something about alcohol- I found this really offensive.", ["Aw don't be a jelly, it's just banter!", "I think he's hilarious!", "He kind of scares me sometimes..."]],
    ["Boyd Orr labs", "Isn't it great how they are open all the time?! I stay close to university and use them to book my holidays, bit cheeky, I know!", ["It's ALWAYS busy, especially with people on Facebook...", "I think it's a great place but I wish you could eat and drink..."]],
    ["First year student, bit lost", "I'm confused, do we need 120 credits for our whole year or just one semester? Cheers, Bob :)", "Hi Bob, yeah it's just for the year.", "120 credits per semester?! I'm going to need a time turner! :P", "Think it's just for the year mate..."],
    ["Check out this cool new language", "Haskell is a functional programming lanaguage and it's really great, but really hard to get my head around. Has anyone got any experience with it?", ["I read a good book- Learn you a Haskell or something?", "Haskell is GREAT for multi-core systems! When functions don't have side effects parallelism is trivial"]],
    ["Does anyone still use PHP?", "I once heard PHP called a 'write once, never read' lanaguge! Hilarous!",["I don't think PHP is used in industry much anymore", "My cousin uses PHP in his job, but I think he would prefer Python."]],
    ["Why is Django written in Python?", "Surely a compiled language such as Java or a functional language would suit the request-response paradigm better?", ["A lot of the Django functions rely on reflection- and Java's reflection is a bit poor...", "Yeah agreed! I'm going to write Javango! :p"]]
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
        Tag.objects.get_or_create(name = tag)

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

        for i in range(random.randint(0, len(tags) - 1)):
            PostTagging.objects.create(post=post, tag = Tag.objects.get(name = tags[i]))

        for commentIndex in range(len(post_data[2])):
            author = allUsers[random.randint(0, len(allUsers) - 1)]

            comment = Comment.objects.create(author = author, post = post, content=post_data[2][commentIndex])

            for user in allUsers:
                if (random.randint(0, 1) == 1):
                    CommentLike.objects.get_or_create(author = user, comment = comment)

        # Get some random users to like the post.
        # We pretend each post in the site is visited by the first half of the user base,
        # each user that visits it will randomly like or not like the post.
        for postLikerIndex in range(0, random.randint(0, len(allUsers) / 2)):
            postLiker = allUsers[postLikerIndex]

            if (random.randint(0, 1) == 0):
                PostLike.objects.get_or_create(author = postLiker, post = post)

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
