from fst import *

# here are some predefined character sets that might come in handy.
# you can define your own
AZ = set("abcdefghijklmnopqrstuvwxyz")
VOWS = set("aeiou")
CONS = set("bcdfghjklmnprstvwxz")
E = set("e")
DBLS = set("nptr")
RN = set("rn")
I = set("i")
A = set("a")

# Implement your solution here
def buildFST():
    #print("Your task is to implement a better FST in the buildFST() function, using the methods described here")
    #print("You may define additional methods in this module (hw1_fst.py) as desired")
    #
    # The states (you need to add more)
    # ---------------------------------------
    # 
    f = FST("q0") # q0 is the initial (non-accepting) state
    f.addState("q1") # a non-accepting state
    f.addState("q_ing") # a non-accepting state
    f.addState("q_e")
    f.addState("q_vow")
    f.addState("q_i")
    f.addState("q_ie")
    f.addState("q_back")
    f.addState("q_rn")
    f.addState("q_vv")
    f.addState("q_ea")

    f.addState("q_EOW", True) # an accepting state (you shouldn't need any additional accepting states)

    #
    # The transitions (you need to add more):
    # ---------------------------------------
    # transduce every element in this set to itself: 
    #f.addSetTransition("q0", AZ, "q1")
    # AZ-E =  the set AZ without the elements in the set E
    f.addSetTransition("q0", AZ-E, "q1")
    f.addTransition("q0", "e", "", "q_e")

    # get rid of this transition! (it overgenerates):
    #f.addSetTransition("q1", AZ, "q_ing")

    f.addSetTransition("q1", AZ - VOWS, "q1")
    f.addTransition("q1", "e", "", "q_e")
    f.addTransition("q_e", "", "", "q_ing")

    # check the char after e
    for c in range(26):
        temp = chr(c + 97)
        if temp in RN:
            f.addTransition("q_e", temp, "e" + temp, "q_rn")
        elif temp in DBLS:
            f.addTransition("q_e", temp, "e" + temp + temp, "q_ing")
            #f.addTransition("q_ing", "", "ing", "q_EOW")
            f.addTransition("q_e", temp, "e" + temp, "q_back")
        else:
            f.addTransition("q_e", temp, "e" + temp, "q1")
    f.addTransition("q_rn", "", "", "q_ing")
    f.addSetTransition("q_rn", AZ - VOWS, "q1")
    f.addSetTransition("q_back", AZ - VOWS, "q1")
    f.addTransition("q_back", "e", "", "q_e")
    f.addTransition("q_back", "i", "", "q_i")
    f.addSetTransition("q_back", VOWS - I - E, "q_vow")

    # check the char after i
    f.addTransition("q1", "i", "", "q_i")
    for c in range(26):
        temp = chr(c + 97)
        if temp in E:
            continue
        if temp in DBLS:
            f.addTransition("q_i", temp, "i" + temp + temp, "q_ing")
            #f.addTransition("q_ing", "", "ing", "q_EOW")
            f.addTransition("q_i", temp, "i" + temp, "q_back")
        else:
            f.addTransition("q_i", temp, "i" + temp, "q1")

    f.addTransition("q_i", "e", "", "q_ie")
    f.addTransition("q_ie", "", "y", "q_ing")
    for c in range(0, 26):
        temp = chr(c + 97)
        f.addTransition("q_ie", temp, "ie" + temp, "q1")
    f.addSetTransition("q_ie", AZ, "q1")

    # check other vows except i&e
    f.addSetTransition("q1", VOWS - I - E, "q_vow")
    #f.addTransition("q_vow", "e", "", "q_e")
    for c in range(26):
        temp = chr(c + 97)
        if temp in E:
            f.addTransition("q_vow", temp, "", "q_e")
        elif temp in DBLS:
            f.addTransition("q_vow", temp, temp + temp, "q_ing")
            #f.addTransition("q_ing", "", "ing", "q_EOW")
            f.addTransition("q_vow", temp, temp, "q_back")
        else:
            f.addTransition("q_vow", temp, temp, "q1")


    f.addTransition("q1", "", "", "q_ing")
    f.addTransition("q_ing", "", "ing", "q_EOW")

    # Return your completed FST
    return f
    

if __name__ == "__main__":
    # Pass in the input file as an argument
    if len(sys.argv) < 2:
        print("This script must be given the name of a file containing verbs as an argument")
        quit()
    else:
        file = sys.argv[1]
    #endif

    # Construct an FST for translating verb forms 
    # (Currently constructs a rudimentary, buggy FST; your task is to implement a better one.
    f = buildFST()
    # Print out the FST translations of the input file
    f.parseInputFile(file)
