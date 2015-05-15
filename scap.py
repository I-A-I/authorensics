from collections import Counter
import operator

# This is the Source Code Authorship Profile (SCAP) method
# Based primarily on "Identifying Authorship by Byte-Level N-Grams:The Source Code Author Profile (SCAP) Method"
# Publicly available at https://www.utica.edu/academic/institutes/ecii/publications/articles/B41158D1-C829-0387-009D214D2170C321.pdf

# The range of n-grams to use for profiling
N_GRAM_MIN = 2
N_GRAM_MAX = 6

#http://locallyoptimal.com/blog/2013/01/20/elegant-n-gram-generation-in-python/
def find_ngram(input_list, n):
    assert n >= 2
    return zip(*[input_list[i:] for i in xrange(n)])

def find_uni_ngrams(s):
    x = []
    for k in xrange(N_GRAM_MIN, N_GRAM_MAX+1):
        x.append(find_ngram(s, k))
    return x

# Class for author profile
class Profile:
    def __init__(self, name="", *rest_text):
        self.name = name
        self.texts = []
        if rest_text:
            apply(self.add_texts, rest_text)

    # Add a single text
    def add_text(self, new_text):
        self.texts.append(unicode(new_text,'utf-8'))

    # For every n-gram between N_GRAM_MIN and N_GRAM_MAX:
        # ... Count n-grams
        # ... Sort descendingly
        # ... Discard frequency to save memory (?)
    # Return array of arrays
    def analyze_text(self):
        self.ngrams = reduce(operator.add, reduce(operator.add, map(lambda x : find_uni_ngrams(x), self.texts)))
        self.ngram_counters = dict(Counter(self.ngrams))
        return self.ngram_counters

    # Add multiple textsshell
    
    def add_texts(self, *new_texts):
        for new_text in new_texts:
            self.add_text(new_text)

    # For each n-gram, use the shorter profile for comparison
    # Similarity should probably be an _absolute_ measure of intersection
    # Not a proportion
    
def find_intersection(p1, p2):
    # Finds the intersection of two dictionaries
    # Returns a dictionary
    d = {}
    for x in p1.keys():
        if x in p2.keys():
            d[x] = min([p1[x],p2[x]])
    return d

def find_distance(p1,p2):
    # Finds the distance between to dictionaries
    # Returns a magnitude. The higher the magnitude, the more similar
    tup = [x*x for x in find_intersection(p1,p2).values()]
    tup = sum(tup)
    tup = tup/(0.0001*max([len(p1.keys()),len(p2.keys())]))
    return tup

if __name__ == "__main__":
    # s = Profile()
    # s.add_text("this is a story about ziwei and his Agar.io :D\nHe is rlly gud at dat game. philipp has acheived nirvana. steven still has to deal with fb's bs. LOL That's some unicode for  you.")
    # p = Profile()
    # p.add_text("Today in period 7, our software development class, we finished the SCAP algorithm and are now waiting for Philipp to finish making the skeleton. Steven has been working arduosly on the frontend javascript. He is currently making a loading screen. Ziwei is reading a book")
    # og = Profile()
    # og.add_text("watsup homedog ziwei, how you doin. Philipp has achieved nirvana and is now doing stuff for a teacher. wut a good guy. steven is still working with fb. i hve nothign to do D: LOL")
    # text = og.analyze_text()
    # print find_distance(s.analyze_text(),text)
    # print find_distance(p.analyze_text(),text)
    text = """Richard Zhan: LOL ok when you edit the readme to add the URL include these two things
    Richard Zhan: I FORGOT TO MENTION YOU CAN'T WALK ON WATER
    We did not request an additional day to work because we are honestly unsure how to solve our current websocketing issue
    Richard Zhan: We did it steven
    Richard Zhan: we're second term seniors
    Steven Zabaloney: smile emoticon
    Steven Zabaloney: its amazing
    Steven Zabaloney: my systems project also doesnt work and i dont know why
    Richard Zhan: im actually really sick
    Steven Zabaloney: but ive done the most work so im not very concerned with it
    Richard Zhan: our systems project works on my cpu
    Richard Zhan: and on homer
    Richard Zhan: but not on my partners'
    Richard Zhan: holy sht is the systems graphed skewed
    Richard Zhan: i think for all commits, additions, adn deletions
    Richard Zhan: my partners and i
    Richard Zhan: occupy 3 of the top 8 spaces
    Richard Zhan: on all 3 fronts
    Richard Zhan: because we wrote a sht ton of comments
    Richard Zhan: and we deleted them
    Richard Zhan: and stuff
    Steven Zabaloney: alright put it in the readme
    Richard Zhan: Harrison did like 40% (but mainly the fancy stuff)
    I did the server stuff and some of the essentials 35%
    and Sisi did most of the essentials 25%
    Richard Zhan: most balanced workflow in a three man group
    Richard Zhan: but you have my condolensces steven
    Richard Zhan: with your group
    Richard Zhan: at least you got inspiriation
    Steven Zabaloney: mine is (classwork aside since that was us yelling at each other)
    Steven Zabaloney: 70% me, 30% jason, 0% david
    Steven Zabaloney: RIP
    Richard Zhan: and david wants to go to yale
    Steven Zabaloney: AND to top it off it doesnt work and i dont know why lmao
    Steven Zabaloney: david bang? really?
    Steven Zabaloney: you know what david said that got me really angry?
    Richard Zhan: 80% Sean
    14% me
    5% you (but you did the video)
    1% albert
    Richard Zhan: ye
    Richard Zhan: what
    Steven Zabaloney: he said he would do the project tuesday and wednesday because he aws too busy doing his softdev project
    Steven Zabaloney: albert LOL
    Richard Zhan: 800 addons
    Richard Zhan: complete bs
    Steven Zabaloney: still tho
    Steven Zabaloney: having to do a softdev project is NOT an excuse to not do systems
    Steven Zabaloney: like hes in the FB chat, he "sees" everything we write, but he just doesnt say/do anything about it
    Richard Zhan: albert
    Richard Zhan: fcking zamansky was like
    Richard Zhan: imma scrutinize what you do for softdev
    Richard Zhan: and who contributed what
    Richard Zhan: and dw flat out said
    Richard Zhan: you guys can work on your own repos and just push it all on the last day becaise i wont be checkign commits
    Steven Zabaloney: in terms of commits and additions im screwed for softdev LOL
    Richard Zhan: you can email dw and ask him to penalize david secretly
    Steven Zabaloney: even moreso than albert
    Steven Zabaloney: see but i dont hate david, at least not until he said what he said
    Steven Zabaloney: now im starting to question him
    Richard Zhan: i can email zamansky and tell him to penalize albert secretly >.>
    Steven Zabaloney: lol
    Steven Zabaloney: might not be a bad idea, at least for the remaining 3 of us
    Richard Zhan: well do what you want
    Richard Zhan: night
    Steven Zabaloney: id like to say that in my defense, i spent a good amount of time trying to understand web socketing and sean's code but to be honest none it really makes sense to me. maybe the JS a little and the google maps but thats about it
    Steven Zabaloney: gn
    Richard Zhan: gl hf gj and welcome to a better life
    Steven Zabaloney: you too dude
    Steven Zabaloney: sorry for this project
    Steven Zabaloney: kinda
    Richard Zhan: np im collegebound
    Richard Zhan: LOOOOOOL
    Steven Zabaloney: nice
    Richard Zhan: we tried
    Steven Zabaloney: i seriously hope ours isnt the only one that flopped
    Steven Zabaloney: yo im getting started on the flappy birds thing, just saying so we dont both do the same thing
    Richard Zhan: DAAAAAAAAAAMN SON
    Richard Zhan: aii
    Richard Zhan: i just woke up
    Richard Zhan: how u doing
    Steven Zabaloney: well
    Steven Zabaloney: it doesnt work
    Steven Zabaloney: but i got the basics down
    Richard Zhan: sweetness
    Steven Zabaloney: youll see
    Steven Zabaloney: i got some green boxes going tho
    Steven Zabaloney: idk whats wrong with them tho
    Richard Zhan: LOOOL
Richard Zhan: ill take a look if i dont pass out
    Steven Zabaloney: i pushed
    Richard Zhan: if i dont look at it by 12 call the cops
Richard Zhan: i might be dead
Steven Zabaloney: ok
Richard Zhan: from linear algebra
Steven Zabaloney: oh
Richard Zhan: the most brutal of all deaths
Richard Zhan: im pretty sure this work is light
Richard Zhan: and im just dumb
Steven Zabaloney: the algebra?
Richard Zhan: ye
Steven Zabaloney: its ok u dont have to do anything today if you dont want to
Richard Zhan: but we must
Richard Zhan: show our OPness
Steven Zabaloney: period 6 is so productive
Richard Zhan: sht
Steven Zabaloney: 7 isnt tho lol
Richard Zhan: IM DONE
Richard Zhan: TIME
2 HOURS AND 15 MINUTES
Richard Zhan: NOT BAD
Richard Zhan: imma shower and check out your code
Steven Zabaloney: ok
Steven Zabaloney: im not sure why theres only one rec
Richard Zhan: why is everything executable
Steven Zabaloney: ?
Richard Zhan: all the files
Richard Zhan: are executable
Steven Zabaloney: its a js and an html file
Richard Zhan: nvm
Steven Zabaloney: yeah i see
Steven Zabaloney: github classifies it as executable
Steven Zabaloney: idk why
Richard Zhan: i fixed yoru code
Richard Zhan: you messed up the math man
Richard Zhan: LOOOL sometimes the space between these pipes are brutal
Steven Zabaloney: really?
Steven Zabaloney: isnt there a way to limit the possible difference
Steven Zabaloney: also the game starts without hitting teh start button i have no idea how or why since the frame thing is never called before
Richard Zhan: OMG YO UWILL BE SO PROUD OF ME
Richard Zhan: LOL
Richard Zhan: im way too tired to continue
Richard Zhan: but i got flappy bird on
Richard Zhan: so all we need is moving and collision
Steven Zabaloney: really?
Richard Zhan: yeah
Richard Zhan: well you cant move
Steven Zabaloney: yeah
Richard Zhan: LOL you just slide across the screen
Richard Zhan: you're prob thinking
Richard Zhan: wtf, that's so ez
Richard Zhan: it is
Richard Zhan: it was like 6 lines of code
Richard Zhan: but it's an imported img
Richard Zhan: night
Steven Zabaloney: gn
Steven Zabaloney: did you push it
Richard Zhan: i am now
Richard Zhan: what
Richard Zhan: anyways
Richard Zhan: pushed
Steven Zabaloney: swag
Richard Zhan: ok imma work? yes no?
Richard Zhan: i will finish it
Steven Zabaloney: ok
Steven Zabaloney: im doing some other work right now
Steven Zabaloney: but you get how im trying to get the collisions to work right?
Richard Zhan: through brute math?
Richard Zhan: is it working?
Richard Zhan: it looks decent
Steven Zabaloney: the console log
Steven Zabaloney: it sorta seems like it works
Steven Zabaloney: i think it stops working in between pipes
Steven Zabaloney: otherwise it seems pretty good (just looking at log)
Richard Zhan: what's the button for
Steven Zabaloney: start? its supposed to start the game lol
Richard Zhan: but it auto starts
Richard Zhan: it doesnt even restart the game
Richard Zhan: LOL
Steven Zabaloney: ik
Steven Zabaloney: its a known issue
Steven Zabaloney: yeah the collision doesnt work so well between pipes
Steven Zabaloney: do you get how i did the collision? i suspect its a math issue somewhere
Richard Zhan: it works fine
Richard Zhan: i believe
Richard Zhan: how do i make the space between pipes
Richard Zhan: wider
Steven Zabaloney: umm
Steven Zabaloney: oh
Richard Zhan: the 275?
Steven Zabaloney: change the modulo
Steven Zabaloney: oh
Steven Zabaloney: you mean that space
Steven Zabaloney: yeah
Steven Zabaloney: but you have to be careful
Steven Zabaloney: change 275 to something smaller, then make the number above that in the random equally smaller
Steven Zabaloney: i tinkered with the speed and spaces and it looked good (i could score a few points)
Steven Zabaloney: but you can change it if you want
Richard Zhan: ok yeah
Richard Zhan: collision is broken
Steven Zabaloney: yeah
Steven Zabaloney: between pipes it starts spamming
Richard Zhan: is it okay
Richard Zhan: if i just restructure this all?
Richard Zhan: what are teh dimensions of this bird?
Richard Zhan: WHAT ARE TEH BIRDS DIMENSIONS
Richard Zhan: FFFF
Steven Zabaloney: i dont know
Steven Zabaloney: i just made up values that worked
Richard Zhan: i got it
Richard Zhan: i think
Richard Zhan: hopefully
Steven Zabaloney: bird.y + 40 is the center of the bird
Steven Zabaloney: and 88 is the x
Steven Zabaloney: bird.y + 40 is the y
Richard Zhan: yeah i got it
Richard Zhan: wait how can
Richard Zhan: y + 40 (means the radius is 40
Richard Zhan: so souldnt the x(which is 10) + 40 be the center
Richard Zhan: nvm you're right
Richard Zhan: ok collisions work
Richard Zhan: i dont think ive ever made
Richard Zhan: so many careless mistakes
Richard Zhan: in a row
Richard Zhan: are you here, please tell me you are
Steven Zabaloney: im here
Richard Zhan: o
Richard Zhan: i did whatever i wanted you to do
Richard Zhan: already
Richard Zhan: LOL
Richard Zhan: it's cool
Richard Zhan: took like 4 lines
Richard Zhan: well there is one problem
Richard Zhan: but it's weird
Richard Zhan: hmmmm
Richard Zhan: going to push
Richard Zhan: pushed
Steven Zabaloney: how is it
Richard Zhan: http://149.89.150.128:8000/flappy.html
Steven Zabaloney: oh nice
Steven Zabaloney: im testing it out
Steven Zabaloney: yeah
Steven Zabaloney: wait you dont need the circle around the bird right?
Richard Zhan: i dont
Richard Zhan: but i kind of want to keep it
Richard Zhan: to show off that we felt
Richard Zhan: we have* a circle hit box
Steven Zabaloney: ill make a show hitbox thingie then
Steven Zabaloney: just so we have a clean version and the circle
Richard Zhan: naaaa, keep it
Richard Zhan: the circle is cool
Richard Zhan: UNLESS YOU REALLY WANT TO
Richard Zhan: then go for it
Steven Zabaloney: its really easy
Richard Zhan: im turning the server off
Richard Zhan: k?
Steven Zabaloney: yeah
Steven Zabaloney: im testing locally
Steven Zabaloney: got it
Steven Zabaloney: added an alert so you know you lost too
Richard Zhan: LOL
Richard Zhan: shower
Steven Zabaloney: pushed
Steven Zabaloney: yo do you know when the softdev hw is due?
Richard Zhan: tomorrow
Richard Zhan: for graphics
Richard Zhan: do you know if we ened to upload it to the gallery?
Steven Zabaloney: we do
Richard Zhan: sht
Richard Zhan: btw
Steven Zabaloney: when is the graphics work due?
Richard Zhan: iunnno
Steven Zabaloney: not monday, im gonna assume
Richard Zhan: yes
Steven Zabaloney: softdev/graphics hw?
Richard Zhan: we didnt present for softdev
Richard Zhan: graphics hw is due friday
Richard Zhan: a symphony of mks
Richard Zhan: kms*
Richard Zhan: happened in the class
Richard Zhan: i left for the doctor during 6th
Richard Zhan: what happened in softdev
Richard Zhan: any assignments?
Steven Zabaloney: the doctor?
Steven Zabaloney: was it like a scheduled thing?
Richard Zhan: yes
Richard Zhan: i got bezier to work
Richard Zhan: had to rederive it
Richard Zhan: and then chesley posted it
Richard Zhan: kms
Steven Zabaloney: uhh we did some backbone stuff with getting the stuff in a database
Steven Zabaloney: so that when you refresh the page the stuff you added is still there
Steven Zabaloney: i was pretty tired so i cant go into detail
Steven Zabaloney: also i got the graphics thing working yesterdayin graphics because i found some website that had the right order of points (piazza was wrong)
Richard Zhan: you shouldnt say piazza was wrong
Richard Zhan: piazza copied dw
Richard Zhan: i copied dw
Richard Zhan: and we both got it wrong
Richard Zhan: so there's a high correlation of being wrong
Richard Zhan: and copying dw
Richard Zhan: (so if your logical, you say dw is wrong, if you're a stat person, you say dw might be wrong)
Richard Zhan: do you know how to do the softdev assignment
Steven Zabaloney: Haven't started
Richard Zhan: im so confused with mongo
Richard Zhan: how do i get mongo to wirth javascript
Richard Zhan: work with*
Steven Zabaloney: I have no idea.
Steven Zabaloney: I'll try to find out tomorrow in school when I start.
Richard Zhan: i got an attention notif from fb
Richard Zhan: tellming me we fcked up the api
Richard Zhan: LOL
Steven Zabaloney: By graphics I figured out the trick is to limit it to 5 iterations no matter what.
"""

    r = Profile()
    s = Profile()
    og = Profile()
    og.add_text("so i was playing this board game; it's called Pairs. each player will be deal a fruit in a triangle 10x10. there is 1 pair, 2 peaches, 3 cherries, etc. the goal of the game is to not get a pair. it is pretty similar to blackjack. i was doing some AP BC stuff, gotta studdy for it. Phoenix Wright is a pretty cool game 10/10 8/8 7/7 would play again. who do you have for english again? oh im so confused D: UofT is my dream school. i want to eat poutine.")
    
    text = text.split("\n")
#FIX THIS
    print find_distance(og.analyze_text(),r.analyze_text())
    print find_distance(og.analyze_text(),s.analyze_text())
    
