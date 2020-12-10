from __future__ import division
import os.path
import sys 

class Transition:
    # string_in
    # string_out
    def __init__(self, inState, inString, outString, outState):
        self.state_in = inState
        self.string_in = inString
        self.string_out = outString
        self.state_out = outState

    def equals(self, t):
        if self.state_in == t.state_in \
        and self.string_in == t.string_in \
        and self.string_out == t.string_out \
        and self.state_out == t.state_out:
            return True
        else:
            return False

class FSTstate:
    # id: an integer ID of the state
    # isFinal: is this a final state?
    def __init__(self, n, isF, fst):
        self.id = n
        self.isFinal = isF
        self.transitions = dict() # map inStrings to a set of all possible transitions
        self.FST = fst

    def addTransition(self, inString, outString, outState):
        newTransition = Transition(self, inString, outString, outState)
        if inString in self.transitions:
            for t in self.transitions[inString]:
                if t.equals(newTransition):
                    return
            self.transitions[inString].add(newTransition)
        else:
            self.transitions[inString] = set([])
            self.transitions[inString].add(newTransition)
    
    def parseInputFromStartState(self, inString):
        parseTuple = ("", self.id)
        parses = []
        (accept, stringParses) = self.parseInput(inString)
        if accept:
            for p in stringParses:
                completeParse = [parseTuple]
                completeParse.extend(p)
                parses.append(completeParse)
        return (accept, parses)

    def parseInput(self, inString):
        parses = []
        isAccepted = True
        
        DEBUG = False
        if DEBUG:
            print("parseInput: state: ", self.id, " parsing: " , inString)
        
        # Case 1: no suffix
        if inString == "":
            epsilonParses = []
            epsilonAccepted = False
            # try all epsilon transitions
            if "" in self.transitions:
                transSet = self.transitions[""]
                for t in transSet:
                    outString = t.string_out
                    toStateID = t.state_out
                    toState = self.FST.allStates[toStateID]
                    parseTuple = (outString, toStateID)
                    (suffixAccepted, suffixParses) = toState.parseInput(inString)
                    if suffixAccepted:
                        epsilonAccepted = True
                        if suffixParses == []: #accepts.
                            parse_s = [parseTuple]
                            epsilonParses.append(parse_s)
                        else:
                            for s in suffixParses:
                                parse_s = [parseTuple]
                                parse_s.extend(s)
                                epsilonParses.append(parse_s)
            # if epsilon is accepted, add all its parses
            if epsilonAccepted:
                parses.extend(epsilonParses)
            # if this is a final state, add an empty parse
            if self.isFinal or parses != []:
                if DEBUG:
                    print("Accepted in state ", self.id)
                return (True, parses)
            else:
                if DEBUG:
                    print("Rejected in state ", self.id)
                return (False, None)
        # case 2: non-empty suffix: there needs to be one suffix that parses!)
        hasAcceptedSuffix = False
        for i in range(0,len(inString)+1):
            prefix = inString[0:i]
            suffix = inString[i:len(inString)]
            if DEBUG:
                print("\t prefix: \'", prefix, "\' I=", i)
            if prefix in self.transitions:
                if DEBUG:
                     print("\t prefix: ", prefix,  "suffix: ", suffix, "I=", i)
                transSet = self.transitions[prefix]
                for t in transSet:
                    outString = t.string_out
                    toStateID = t.state_out
                    toState = self.FST.allStates[toStateID]
                    parseTuple = (outString, toStateID)
                    (suffixAccepted, suffixParses) = toState.parseInput(suffix)
                    if suffixAccepted:
                        hasAcceptedSuffix = True
                        if suffixParses == []:
                            parse_s = [parseTuple]
                            parses.append(parse_s)
                            thisPrefixParses = True
                        for s in suffixParses:
                            parse_s = [parseTuple]
                            parse_s.extend(s)
                            parses.append(parse_s)
        if hasAcceptedSuffix:
            return (True, parses)
        else:
            return (False, None)
                            


    def printState(self):
        if self.isFinal:
            FINAL = "FINAL"
        else: FINAL = ""
        print("State", self.id, FINAL)
        for inString in self.transitions:
            transList = self.transitions[inString]
            for t in transList:
                print("\t", inString, ":", t.string_out, " => ", t.state_out)

                    


class FST:
    def __init__(self, initialStateName="q0"):
        self.nStates = 0
        self.initState = FSTstate(initialStateName, False, self) 
        self.allStates = dict()
        self.allStates[initialStateName] = self.initState
       
    def addState(self, name, isFinal=False):
        if name in self.allStates:
            print("ERROR addState: state", name, "exists already")
            sys.exit()
        elif len(self.allStates) >= 30:
            print("ERROR addState: you can't have more than 30 states")
            sys.exit()
        else:  
            newState = FSTstate(name, isFinal, self)
            self.allStates[name] = newState

    def addTransition(self, inStateName, inString, outString, outStateName):
        if (len(inString) > 1):
            print("ERROR: addTransition: input string ", inString, " is longer than one character")
            sys.exit()
        if inStateName not in self.allStates:
            print("ERROR: addTransition: state ", inStateName, " does not exist")
            sys.exit()
        if outStateName not in self.allStates:
            print("ERROR: addTransition: state ", outStateName, " does not exist")
            sys.exit()
        inState = self.allStates[inStateName]
        inState.addTransition(inString, outString, outStateName)

    # epsilon:epsilon
    def addEpsilonTransition(self, inStateName, outStateName):
        if inStateName not in self.allStates:
            print("ERROR: addEpsilonTransition: state ", inStateName, " does not exist")
            sys.exit()
        if outStateName not in self.allStates:
            print("ERROR: addEpsilonTransition: state ", outStateName, " does not exist")
            sys.exit()
        if inStateName == outStateName:
            print("ERROR: we don't allow epsilon loops")
            sys.exit()
        inState = self.allStates[inStateName]
        inState.addTransition("", "", outStateName)

    # map every element in inStringSet to itself
    def addSetTransition(self, inStateName, inStringSet, outStateName):
         if inStateName not in self.allStates:
            print("ERROR: addSetTransition: state ", inStateName, " does not exist")
            sys.exit()
         if outStateName not in self.allStates:
            print("ERROR: addSetTransition: state ", outStateName, " does not exist")
            sys.exit()
         for s in inStringSet:
            self.addTransition(inStateName, s, s, outStateName)

    # map string to itself
    def addSelfTransition(self, inStateName, inString, outStateName):
         if inStateName not in self.allStates:
            print("ERROR: addSetTransition: state ", inStateName, " does not exist")
            sys.exit()
         if outStateName not in self.allStates:
            print("ERROR: addSetTransition: state ", outStateName, " does not exist")
            sys.exit()
         self.addTransition(inStateName, inString, inString, outStateName)

    # map every element in inStringSet to outString
    def addSetToStringTransition(self, inStateName, inStringSet, outString, outStateName):
         if inStateName not in self.allStates:
            print("ERROR: addSetDummyTransition: state ", inStateName, " does not exist")
            sys.exit()
         if outStateName not in self.allStates:
            print("ERROR: addSetDummyTransition: state ", outStateName, " does not exist")
            sys.exit()
         for s in inStringSet:
            self.addTransition(inStateName, s, outString, outStateName)
    
            
    # map every element in inStirngSet to outString
    def addSetEpsilonTransition(self, inStateName, inStringSet, outStateName):
         if inStateName not in self.allStates:
            print("ERROR: addSetEpsilonTransition: state ", inStateName, " does not exist")
            sys.exit()
         if outStateName not in self.allStates:
            print("ERROR: addSetEpsionTransition: state ", outStateName, " does not exist")
            sys.exit()
         for s in inStringSet:
            self.addTransition(inStateName, s, "", outStateName)
            
    def parseInput(self, inString):
        SHOW_STATES = False#True
        inString = inString.rstrip('\n')
        (canParse, allParses)  = self.initState.parseInputFromStartState(inString)
        allParsesAsString = ""
        if canParse:
            for parse in allParses:
                for tuple in parse:
                    outString, outState = tuple
                    allParsesAsString += outString
                if SHOW_STATES:
                    allParsesAsString += "\t  States: "
                    i = 0
                    for tuple in parse:
                        i += 1
                        outString, outState = tuple
                        allParsesAsString += outState
                        if i < len(parse):
                            allParsesAsString += " => "
                    allParsesAsString += "; "
          
            print(inString, " ==> ", allParsesAsString)
            return True
        else:
            print(inString, " ==> ", "FAIL")
            return False

    def printFST(self):
        print("Printing FST", str(self))
        for stateID in self.allStates:
            state = self.allStates[stateID]
            state.printState()

    def parseInputFile(self, fileName):
        if os.path.isfile(fileName):
            file = open(fileName, "r")
            nParses = 0
            totalStrings = 0
            for line in file:
                totalStrings += 1
                canParse = self.parseInput(line)
                if canParse:
                    nParses += 1
            fraction = nParses/totalStrings
            print("### ", fraction,  "(", nParses, " out of ", totalStrings, ") parsed") 
