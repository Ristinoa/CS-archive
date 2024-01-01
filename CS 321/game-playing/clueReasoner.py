'''ClueReasoner.py - project skeleton for a propositional reasoner
for the game of Clue.  Unimplemented portions have the comment "TO
BE IMPLEMENTED AS AN EXERCISE".  The reasoner does not include
knowledge of how many cards each player holds.
Originally by Todd Neller
Ported to Python by Dave Musicant

Copyright (C) 2019 Dave Musicant

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

Information about the GNU General Public License is available online at:
  http://www.gnu.org/licenses/
To receive a copy of the GNU General Public License, write to the Free
Software Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
02111-1307, USA.'''

# from SATsolver import *
import SATSolver

# Initialize important variables
caseFile = "cf"
players = ["sc", "mu", "wh", "gr", "pe", "pl"]
extendedPlayers = players + [caseFile]

suspects = ["mu", "pl", "gr", "pe", "sc", "wh"]
weapons = ["kn", "ca", "re", "ro", "pi", "wr"]
rooms = ["ha", "lo", "di", "ki", "ba", "co", "bi", "li", "st"]
cards = suspects + weapons + rooms

def printClauses(clauses):
    for clause in clauses:
        print(clause)
    exit()

def getPairNumFromNames(player,card):
    return getPairNumFromPositions(extendedPlayers.index(player),
                                   cards.index(card))

def getPairNumFromPositions(player,card):
    return player*len(cards) + card + 1

# TO BE IMPLEMENTED AS AN EXERCISE
def initialClauses():
    clauses = []

    # Each card is in at least one place (including case file).
    for c in cards:
        clauses.append([getPairNumFromNames(p,c) for p in extendedPlayers])

    # A card cannot be in two places.
    clauses1 = []
    for clause in clauses:
        for x in range(0,len(clause)):
            for y in range(x+1,len(clause)):
                clauses1.append([-clause[x],-clause[y]])

    # At least one card of each category is in the case file.
    clauses2 = []
    for category in [suspects, weapons, rooms]:
        clause = [getPairNumFromNames(caseFile, c) for c in category]
        clauses2.append(clause)
    

    # No two cards in each category can both be in the case file.
    # Essentially creates every possible case file + every negation needed to 'make legal' each case file
    clauses3 = []
    for clause in clauses2:
        for x in range(0,len(clause)):
            for y in range(x+1,len(clause)):
                clauses3.append([-clause[x],-clause[y]])


    clauses = clauses + clauses1 + clauses2 + clauses3
    printClauses(clauses)
    return clauses

# TO BE IMPLEMENTED AS AN EXERCISE  

def hand(player,cards):
    # suspects does not include case file (use cards)
    clauses = []
    for card in cards:
        # giving a card to a player.
        clauses.append([getPairNumFromNames(player,card)])
    return clauses


# TO BE IMPLEMENTED AS AN EXERCISE  
def suggest(suggester,card1,card2,card3,refuter,cardShown):

    advantage = []

    # Scarlett has seen the card => she is either refuting or suggesting (and the refuter is not belligerent)
    if cardShown != None:
        advantage = [[getPairNumFromNames(refuter,cardShown)]]
    
    # Scarlett has not seen the card => either she is suggesting (and the refuter is belligerent) or it is not her turn
    elif refuter != None & cardShown == None:
        ''' 
            4 possible cases once you get to this point:

             A. Scarlet is suggesting and her refuter won't shower her the card—she 
                can conclude her refuter has at least one of three cards, therefore one 
                of the three is not in cf 

             B. Scarlett is witnessing, and has none of the cards in the suggestion. 
                She can conclude the same as in A
            
             C. Scarlett is witnessing, and has one of the cards in the suggestion 
                (but refute happened before her turn). She can conclude the same as in A, 
                except the refuter can have at most two of the cards.

             D. Scarlett is witnessing, and has two of the cards in the suggestion
                (but refute happened before her turn). She can deduce the exact card the 
                refuter has as well as conclude that none of the three cards in the suggestion
                are contained in the cf. 

            Unfortunately, we only have access to refuter and suggester, and I can't
            think of a practical way to implement without player access. :(
            
            Only works if refuter or suggester is Scarlett (since hers is the only hand we know). 
        '''
        # The cards potentially not in the cf:
        advantage = [[
            getPairNumFromNames(refuter,card1),
            getPairNumFromNames(refuter,card2),
            getPairNumFromNames(refuter,card3)
        ]]

    disadvantage = []
    # List of players at a 'disadvantage' in that they can conclude nothing
    # or they can conclude at least on of the three cards in the suggestion is 
    # not in the case file
    if refuter != None:
        
        p = players.index(suggester)+1
        if p == len(players):
            p = 0
    
        while p != players.index(refuter):
            # skip suggester:
            if p == players.index(suggester):
                continue
            
            # add players at disadvantage to disadvantage list:
            disadvantage.append([-getPairNumFromNames(players[p],card1)])
            disadvantage.append([-getPairNumFromNames(players[p],card2)])
            disadvantage.append([-getPairNumFromNames(players[p],card3)])
            p += 1

            # if you hit the max pre-emptively:
            if p == len(players):
                p = 0
                continue
            
    else: # there is no refuter; everybody except suggester gets added
        for p in range(0,len(players)):
            if p != players.index(suggester):
                disadvantage.append([-getPairNumFromNames(players[p],card1)])
                disadvantage.append([-getPairNumFromNames(players[p],card2)])
                disadvantage.append([-getPairNumFromNames(players[p],card3)])

    return advantage + disadvantage

# TO BE IMPLEMENTED AS AN EXERCISE  
def accuse(accuser,card1,card2,card3,isCorrect):
    if isCorrect:
        return [[getPairNumFromNames("cf",card1)],[getPairNumFromNames("cf",card2)],[getPairNumFromNames("cf",card3)]]
    else:
        # return negation of accused hand, don't really know how to kick player out of accusing more
        return [[-getPairNumFromNames(accuser,card1),-getPairNumFromNames(accuser,card2),-getPairNumFromNames(accuser,card3)]]

def query(player,card,clauses):
    return SATSolver.testLiteral(getPairNumFromNames(player,card),clauses)

def queryString(returnCode):
    if returnCode == True:
        return 'Y'
    elif returnCode == False:
        return 'N'
    else:
        return '-'

def printNotepad(clauses):
    for player in players:
        print('\t', player, end=' ')
    print('\t', caseFile)
    for card in cards:
        print(card,'\t', end=' ')
        for player in players:
            print(queryString(query(player,card,clauses)),'\t', end=' ')
        print(queryString(query(caseFile,card,clauses)))

def playClue():
    clauses = initialClauses()
    clauses.extend(hand("sc",["wh", "li", "st"]))
    clauses.extend(suggest("sc", "sc", "ro", "lo", "mu", "sc")) 
    clauses.extend(suggest("mu", "pe", "pi", "di", "pe", None)) 
    clauses.extend(suggest("wh", "mu", "re", "ba", "pe", None))
    clauses.extend(suggest("gr", "wh", "kn", "ba", "pl", None))
    clauses.extend(suggest("pe", "gr", "ca", "di", "wh", None))
    clauses.extend(suggest("pl", "wh", "wr", "st", "sc", "wh"))
    clauses.extend(suggest("sc", "pl", "ro", "co", "mu", "pl"))
    clauses.extend(suggest("mu", "pe", "ro", "ba", "wh", None))
    clauses.extend(suggest("wh", "mu", "ca", "st", "gr", None))
    clauses.extend(suggest("gr", "pe", "kn", "di", "pe", None))
    clauses.extend(suggest("pe", "mu", "pi", "di", "pl", None))
    clauses.extend(suggest("pl", "gr", "kn", "co", "wh", None))
    clauses.extend(suggest("sc", "pe", "kn", "lo", "mu", "lo"))
    clauses.extend(suggest("mu", "pe", "kn", "di", "wh", None))
    clauses.extend(suggest("wh", "pe", "wr", "ha", "gr", None))
    clauses.extend(suggest("gr", "wh", "pi", "co", "pl", None))
    clauses.extend(suggest("pe", "sc", "pi", "ha", "mu", None))
    clauses.extend(suggest("pl", "pe", "pi", "ba", None, None))
    clauses.extend(suggest("sc", "wh", "pi", "ha", "pe", "ha"))
    clauses.extend(suggest("wh", "pe", "pi", "ha", "pe", None))
    clauses.extend(suggest("pe", "pe", "pi", "ha", None, None))
    clauses.extend(suggest("sc", "gr", "pi", "st", "wh", "gr"))
    clauses.extend(suggest("mu", "pe", "pi", "ba", "pl", None))
    clauses.extend(suggest("wh", "pe", "pi", "st", "sc", "st"))
    clauses.extend(suggest("gr", "wh", "pi", "st", "sc", "wh"))
    clauses.extend(suggest("pe", "wh", "pi", "st", "sc", "wh"))
    clauses.extend(suggest("pl", "pe", "pi", "ki", "gr", None))
    print('Before accusation: should show a single solution.')
    printNotepad(clauses)
    print()
    clauses.extend(accuse("sc", "pe", "pi", "bi", True))
    print('After accusation: if consistent, output should remain unchanged.')
    printNotepad(clauses)

if __name__ == '__main__':
    playClue()