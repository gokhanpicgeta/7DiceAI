import itertools
import math
import random


class Player:

    id_obj = itertools.count()

    def __init__(self,human=False):
        self.human = human
        self.id = next(Player.id_obj)
        self.cards = {"S":[], "C":[], "H":[], "D":[]}
        self.cardCount = 0
        self.sevenDiamonds = False

    def playCard(self,suit,faceValue):

        print("in play card", suit, faceValue, self.cards)

        if suit in self.cards.keys() and faceValue in self.cards[suit]:
            print("ISSA LEGAL")
            self.cards[suit].remove(faceValue)
            return True

        else:
            return False


class Card:

    def __init__(self):
        self.count = 52
        self.cardList = {"S":[], "C":[], "H":[], "D":[]}

        for key,val in self.cardList.items():

            for i in range(1,14):
                self.cardList[key].append(i)

    def getRand(self):

        while(True):
            suit = random.randint(1,4)
            faceValue = random.randint(1,13)

            if suit == 1 and faceValue in self.cardList["S"]:
                self.cardList["S"].remove(faceValue)
                return ("S",faceValue)
            elif suit == 2 and faceValue in self.cardList["C"]:
                self.cardList["C"].remove(faceValue)
                return ("C", faceValue)
            elif suit == 3 and faceValue in self.cardList["H"]:
                self.cardList["H"].remove(faceValue)
                return ("H", faceValue)
            elif suit == 4 and faceValue in self.cardList["D"]:
                self.cardList["D"].remove(faceValue)
                return ("D", faceValue)

class Game:

    def __init__(self):

        self.playerTurn = None
        self.playerCount = 0
        self.playerList = []
        self.boardState = {"S":[], "C":[], "H":[], "D":[]}
        self.cards = Card()
        self.gameOver = False
        self.winner = None

    def addPlayer(self):
        player = Player()
        self.playerList.append(player)
        self.playerCount+=1
        return player

    def addHuman(self):
        player=Player(True)
        self.playerList.append(player)
        self.playerCount+=1


    def distributeCards(self):

        for i in range(self.playerCount):

            for j in range(52//self.playerCount):

                suit,faceValue = self.cards.getRand()
                if(suit == "D" and faceValue == 7):
                    self.playerList[i].sevenDiamonds = True
                #print(suit,faceValue)
                self.playerList[i].cards[suit].append(faceValue)
                self.playerList[i].cardCount+=1

            print(self.playerList[i].cards)

    def getLegalMoves(state):
        print(state)
        return state["cards"]
        board = state["board"]
        cards = state["cards"]

        #TODO: Random Legal card
        legalMoves = {"S":[], "C":[], "H":[], "D":[]}
        for key,value in board.items():

            if(len(value)>0):

                lowerVal = min(board[key])
                upperVal = max(board[key])

                if lowerVal-1 in cards[key]:
                    legalMoves[key].append(lowerVal-1)

                if upperVal+1 in cards[key]:
                    legalMoves[key].append(upperVal+1)

        for suit,faceValue in cards.items():

            if(7 in faceValue):

                legalMoves[suit].append(7)



        if(len(legalMoves["S"]) == 0 ):
            del legalMoves["S"]
        if(len(legalMoves["C"]) == 0 ):
            del legalMoves["C"]
        if(len(legalMoves["H"]) == 0 ):
            del legalMoves["H"]
        if(len(legalMoves["D"]) == 0 ):
            del legalMoves["D"]

        print("legal moves are ",legalMoves)
        legalMovesAsList = [(suit, value) for suit, values in legalMoves.items() for value in values]
        return legalMovesAsList



    def get_state(self):
        """
        Get the state which includes board state, card state and possibly whos turn it is?
        """
        state = {}
        if self.playerTurn == 0:
            state={
                "board": self.boardState,
                "cards": self.playerList[0].cards
            }

        else:
            state={
                "board": self.boardState,
                "cards": self.playerList[1].cards
            }
        legalMoves = {"S": [], "C": [], "H": [], "D": []}
        for key, value in state["board"].items():

            if (len(value) > 0):

                lowerVal = min(state["board"][key])
                upperVal = max(state["board"][key])

                if lowerVal - 1 in state["cards"][key]:
                    legalMoves[key].append(lowerVal - 1)

                if upperVal + 1 in state["cards"][key]:
                    legalMoves[key].append(upperVal + 1)

        for suit, faceValue in state["cards"].items():

            if (7 in faceValue):
                legalMoves[suit].append(7)

        if (len(legalMoves["S"]) == 0):
            del legalMoves["S"]
        if (len(legalMoves["C"]) == 0):
            del legalMoves["C"]
        if (len(legalMoves["H"]) == 0):
            del legalMoves["H"]
        if (len(legalMoves["D"]) == 0):
            del legalMoves["D"]

        print("legal moves are ", legalMoves)
        legalMovesAsList = [(suit, value) for suit, values in legalMoves.items() for value in values]

        new_state = {
            "board": self.boardState,
            "cards": legalMovesAsList
        }


        print("state is ", new_state )
        return new_state


    def playCard(self,player,suit,faceValue,passTurn=False):

        if(passTurn == False):

            if player.playCard(suit,faceValue):
                self.boardState[suit].append(faceValue)
                self.boardState[suit] = sorted(self.boardState[suit])
                player.cardCount-=1

            print("Card played")
            print("Board State ", self.boardState)
            print("Hand State ", player.cards)

            if player.cardCount == 0:

                print("Player ", player.id," HAS WON!!")

                if(player.id == 0):
                    self.winner = 0
                    loser = 1
                else:
                    self.winner = 1
                    loser = 0

                print("Losers hand was", self.playerList[1-self.winner].cards)
                #exit()

            if self.playerTurn == 0:
                self.playerTurn = 1
            else:
                self.playerTurn = 0

        else:
            if self.playerTurn == 0:
                self.playerTurn = 1
            else:
                self.playerTurn = 0



class SevenDiceAI():

    def __init__(self,alpha=0.5,epsilon=0.1):
        """
        Initialize AI with empty learning Q dictionary alpha learning rate and an epsilon rate.
        """

        self.q = dict()
        self.alpha = alpha
        self.epsilon = epsilon
        #self.player1 = Game.addPlayer()
        #self.player2 = Game.addPlayer()
        #self.playerTurn = 0


    def update(self, old_state, action, new_state, reward):
        """
        Update Q-learning model, given an old state, an action taken
        in that state, a new resulting state, and the reward received
        from taking that action.
        """
        old = self.get_q_value(old_state, action)
        best_future = self.best_future_reward(new_state)
        self.update_q_value(old_state, action, old, reward, best_future)

    def get_q_value(self,state,action):
        """
        Return the Q-value for the state `state` and the action `action`.
        If no Q-value exists yet in `self.q`, return 0.
        """
        print(state)
        board = state["board"].items()
        cards = state["cards"]
        state_str=""
        for suit, values in board:
            state_str+=suit
            for value in values:
                state_str+=str(value)

        for suit,values in cards:
            state_str+=suit+str(values)
            #for value in values:
                #state_str+=str(value)

        #print(tuple(board),tuple(cards))
        #condensed_state = tuple(board)+ tuple(cards)
        if (state_str,action) not in self.q.keys():
            return 0
        #print("getting q value", state, action, self.q[tuple(state), action])
        #for key in self.q.keys():
            #print(key[0][0])
        return self.q[state_str,action]


        #raise NotImplementedError

    def update_q_value(self, state, action, old_q, reward, future_rewards):
        """
        Update the Q-value for the state `state` and the action `action`
        given the previous Q-value `old_q`, a current reward `reward`,
        and an estiamte of future rewards `future_rewards`.

        Use the formula:

        Q(s, a) <- old value estimate
                   + alpha * (new value estimate - old value estimate)

        where `old value estimate` is the previous Q-value,
        `alpha` is the learning rate, and `new value estimate`
        is the sum of the current reward and estimated future rewards.
        """
        #TODO: its only taking in the state as the words board and card as that is what tuple state does I have to change that to take into accont actual board state and card statee
        print("Updating q values", state,tuple(state["board"]), action)



        board = state["board"].items()
        cards = state["cards"]
        state_str = ""
        for suit, values in board:
            state_str+=suit
            for value in values:
                state_str+=str(value)


        for suit,values in cards:
            state_str+=suit+str(values)
            #for value in values:
                #state_str+=str(value)
        print(state_str)
        #print(tuple(board),tuple(cards))
        #condensed_state = (tuple(board),tuple(cards))
        #print(condensed_state)
        #print((condensed_state),action)
        #print(type(condensed_state))
        #print(type(action))
        self.q[(state_str, action)] = old_q + self.alpha * ((reward + future_rewards) - old_q)


        #raise NotImplementedError

    def best_future_reward(self,state):

        """
        Given a state `state`, consider all possible `(state, action)`
        pairs available in that state and return the maximum of all
        of their Q-values.

        Use 0 as the Q-value if a `(state, action)` pair has no
        Q-value in `self.q`. If there are no available actions in
        `state`, return 0.
        """
        maxQ = 0
        for action in Game.getLegalMoves(state):
            maxQ = max(self.get_q_value(state, action), maxQ)

        return maxQ
        #raise NotImplementedError

    def choose_action(self,state,epsilon=False): #TODO change to true

        """
        Given a state `state`, return an action `(i, j)` to take.

        If `epsilon` is `False`, then return the best action
        available in the state (the one with the highest Q-value,
        using 0 for pairs that have no Q-values).

        If `epsilon` is `True`, then with probability
        `self.epsilon` choose a random available action,
        otherwise choose the best action available.

        If multiple actions have the same Q-value, any of those
        options is an acceptable return value.
        """

        print("Choosing action the state is ", state)
        #TODO: choose action from available actions in class Player but might have to modify card hand logic

        if epsilon:
            print("wtf is a state ", state)
            state_tuple = tuple(state['board'].items()), tuple(state['cards'].items())
            print(state_tuple)
            print(self.q)
            #Choose random move for exploring
            if random.random()<=self.epsilon:

                actionList = []

                for suit,faceValue in Game.getLegalMoves(state):

                    actionList.append((suit,faceValue))

                #TODO prolly have to fix this appending to actionList logic as it is from a dict

                randMove = random.choice(actionList)
                print("randmove")
                return randMove

        #Best possible move

        #TODO might have to take into account logic of passing??

        maxReward = -math.inf
        actions = Game.getLegalMoves(state)

        #PASS TURN?
        if len(actions) == 0:
            bestAction="Pass"
            return bestAction

        for action in actions:

            if self.get_q_value(state,action) > maxReward:
                maxReward = self.get_q_value(state,action)
                bestAction = action

        return bestAction


        #raise NotImplementedError

def train(n, discount_factor=0.9):
    """
    Training an AI by playing n games against itself using Q-learning with backpropagation
    :param n: Number of training games
    :param discount_factor: Discount factor for backpropagation
    :return: Trained AI
    """

    ai = SevenDiceAI()

    for _ in range(n):
        print(f"Playing training game {_+1}")
        game = Game()
        game.addPlayer()
        game.addPlayer()
        game.distributeCards()

        # FIGURING OUT WHO GOES FIRST WITH SEVEN DICE AND STUFF
        for i in range(len(game.playerList)):
            if game.playerList[i].sevenDiamonds:
                game.playCard(game.playerList[i], "D", 7)
                game.playerTurn = 1 if i == 0 else 0

        # Keep track of all moves made by either player in the episode
        episode_moves = []

        # Game loop
        while True:
            state = game.get_state()
            action = ai.choose_action(state)
            episode_moves.append({"state": state, "action": action})

            # Make move
            print("ACTION TO TAKE IS ", action)

            if action == "Pass":
                game.playerTurn = 1 - game.playerTurn
            else:
                game.playCard(game.playerList[game.playerTurn], action[0], action[1])
                new_state = game.get_state()

            if game.winner is not None:
                loser_score = sum(value for face_values in game.playerList[1 - game.winner].cards.values() for value in face_values)
                total_reward = 1 * loser_score

                # Backpropagate rewards or penalties through the entire episode
                for t in range(len(episode_moves)):
                    player_turn = game.playerTurn if t % 2 == 0 else 1 - game.playerTurn
                    move = episode_moves[t]
                    ai.update(move["state"], move["action"], new_state, total_reward)
                    total_reward *= discount_factor

                break

            # If the game is continuing, no rewards yet
            #elif episode_moves[-1]["state"] is not None:
                #ai.update(episode_moves[-1]["state"], episode_moves[-1]["action"], new_state, 0)

    print("done training")
    learntCounter = 0
    for key, val in ai.q.items():
        if val != 0.0:
            learntCounter+=1
            print(key, val)
    print(len(ai.q))
    print(learntCounter)
    return ai


def play(ai):
    """
    Play human game against ai
    """

    game = Game()
    human = game.addPlayer()
    aiPlayer = game.addPlayer()
    game.distributeCards()
    #Start the game with seven of dice

    for i in range(len(game.playerList)):
        if game.playerList[i].sevenDiamonds == True:
            game.playCard(game.playerList[i], "D", 7)

            if i == 0:
                game.playerTurn = 1
            else:
                game.playerTurn = 0

    while True:

        print()
        print("Board:")
        for suit,faceVal in game.boardState.items():
            print(suit, " ", faceVal)
        print()

        print("Turn is ", game.playerTurn, human.id)

        if(game.playerTurn == 0):
            print("Your cards are: ", human.cards)
            state = game.get_state()
            legalMoves = state["cards"]

            print("Your turn, if you want to pass Type P in the suit")
            while True:
                suit = input("Choose suit ")
                if(suit!= "P"):
                    faceValue = int(input("Choose card "))
                    #game.playCard(human, suit, faceValue)
                else:
                    if(len(legalMoves) == 0 and suit == "P"):
                        game.playCard(human, suit, None, True)
                        break
                if(suit,faceValue) in legalMoves:
                    print("Valid card")
                    game.playCard(human, suit, faceValue)
                    break
                else:
                    print("invalid card try again")

                #break

        else:
            print("AI's turn")

            state = game.get_state()
            print("state for ai is ", state)
            action = ai.choose_action(state)
            game.playCard(game.playerList[game.playerTurn], action[0], action[1])
            print("AI chose to play", action[0], action[1])

        if game.winner is not None:
            print()
            print("GAME OVER")
            winner = "Human" if game.winner == 0 else "AI"
            print(f"Winner is {winner}")
            return




#game = Game()
#game.addPlayer()
#game.addPlayer()

#print(game.playerCount)
#game.distributeCards()


#Play game
"""

def playRandomGame():

    for i in range(len(game.playerList)):
        if game.playerList[i].sevenDiamonds == True:
            game.playCard(game.playerList[i], "D", 7)

            if i == 0:
                game.playerTurn = 1
            else:
                game.playerTurn = 0

    counter=0
    while(counter<100):

        #Find who has 7 of diamonds they go first
        #Then toggle player turn and let the other player go randomly

        #print(game.playerTurn)

        print("Its ",game.playerTurn, " player turn")
        legalMoves = game.playerList[game.playerTurn].getLegalMoves(game.boardState) #TODO getlegalmoves is now in game class and not in playerclass

        legalMovesAsList = [(suit,value) for suit,values in legalMoves.items() for value in values]

        if(len(legalMovesAsList) > 0):

            #TODO: Implement Q-Learning for choosing a move which takes into account Winning but also how much you are winning/losing by
            #TODO: Get AI to play against itself and learn that way?
            #TODO: Setup a class with all the qlearning stuff
            #TODO: State has to take into account many variables such as board state, player hand, number of players, whos turn it is, etc.
            randomMove = random.choice(legalMovesAsList)

            print("Random move is ", randomMove)
            game.playCard(game.playerList[game.playerTurn],randomMove[0],randomMove[1])

        #PASS
        else:

            if game.playerTurn == 0:
                game.playerTurn = 1
            else:
                game.playerTurn = 0




        counter+=1
"""
def playHuman():
    """
    Play human player against the AI
    """

    #TODO: Deal cards to human and AI
    #TODO: Figure out who has 7 of dice and let them go first
    #TODO: After 7 dice has been played let the other person play
    #TODO: Take in human input to play a card
    #TODO: Play till someone wins
    #TODO: Calculate score

    game = Game()
    game.addPlayer()
    game.addHuman()

    game.distributeCards()








#playRandomGame()
#playHuman()


