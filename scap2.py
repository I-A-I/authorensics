import scap

def find_intersection(p1, p2):
    # Finds the intersection of two dictionaries
    # Returns a dictionary
    d = {}
    for x in p1.keys():
        if x in p2.keys():
            d[x] = min([p1[x],p2[x]])
    return d


def find_union(p1, p2):
    # Finds the union of two dictionaries
    # Returns a dictionary
    d = p1.copy()
    for x in p2.keys():
        if x in d:
            d[x] = max(p1[x],p2[x])
        else:
            d[x] = p2[x]
    return d

    
def find_distance(p1,p2):
    # Finds the distance between to dictionaries
    # Returns a magnitude. The higher the magnitude, the more similar
    tup = [x*x for x in find_intersection(p1,p2).values()]
    tup = sum(tup)
    tup = tup/(1.0*max([len(p1.keys()),len(p2.keys())]))
    return tup

def find_percent(p1,p2):
    # Finds the percentage similarity
    # |(p1 ^ p2)| / |(p1 U p2)|
    u = find_union(p1,p2)
    return find_distance(p1,p2)/find_distance(u,u)

def find_all_percents(p1, p2):
    # Finds all the percent similarites between lists of ngrams
    return [ find_percent(x[0],x[1]) for x in zip(p1,p2) ]

def find_dumb_score(l):
    # "Mathematically and Scientifically" figures out how to compare the percents
    # 6-grams are worth more than 2-grams
    return sum([l[0]*2,l[1]*3,l[2]*4,l[3]*5,l[4]*6])

if __name__ == "__main__":
    p1 = {"a":4, "b":1, "c":2}
    p2 = {"a":2, "e":4}
    print find_percent(p1,p2)
    p3 = {"a":4, "b":1, "c":2}
    p4 = {"a":4, "b":1, "c":2}
    print find_percent(p3,p4)
    p5 = {"a":4, "b":1, "c":2}
    p6 = {"a":4, "b":1, "c":1}
    print find_percent(p5,p6)
    p7 = {"a":1}
    p8 = {"b":2, "c":3, "d":5}
    print find_percent(p7,p8)
    s = scap.Profile()
    s.add_text("this is a story about ziwei and his Agar.io :D\nHe is rlly gud at dat game. philipp has acheived nirvana. steven still has to deal with fb's bs. LOL That's some unicode for  you.")
    p = scap.Profile()
    p.add_text("Today in period 7, our software development class, we finished the SCAP algorithm and are now waiting for Philipp to finish making the skeleton. Steven has been working arduosly on the frontend javascript. He is currently making a loading screen. Ziwei is reading a book")
    og = scap.Profile()
    og.add_text("watsup homedog ziwei, how you doin. Philipp has achieved nirvana and is now doing stuff for a teacher. wut a good guy. steven is still working with fb. i hve nothign to do D: LOL")
    print s.analyze_text()
    #print find_all_percents(s.analyze_text(),og.analyze_text())
    #print find_all_percents(p.analyze_text(),og.analyze_text())
    print find_dumb_score(find_all_percents(s.analyze_text(),og.analyze_text()))
    print find_dumb_score(find_all_percents(p.analyze_text(),og.analyze_text()))
