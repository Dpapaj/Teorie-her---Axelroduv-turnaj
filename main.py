import random


class Player:
    def __init__(self,strategy):
        self.strategy = strategy
        self.last_move = None

    def play(self):
        return self.strategy (self.last_move)

    def update_last_move(self,move):
        self.last_move = move


def tit_for_tat(last_move):
    if last_move is None:
        return True
    return last_move


def always_cooperate(last_move):
    return True


def always_defect(last_move):
    return False


def periodically_ddc(last_move):
    if last_move is None:
        return True
    return False if random.random () < 0.1 else last_move


def periodically_ccd(last_move):
    if last_move is None:
        return False
    return True if random.random () < 0.1 else last_move


def custom_strategy(last_move):
    if last_move is None:
        return True
    elif last_move:
        return random.random () < 0.8
    else:
        return random.random () < 0.2


players = [
    Player (tit_for_tat),
    Player (always_cooperate),
    Player (always_defect),
    Player (periodically_ddc),
    Player (periodically_ccd),
    Player (custom_strategy)
]

payoff_matrix = {
    (True,True):(3,3),
    (True,False):(0,5),
    (False,True):(5,0),
    (False,False):(1,1)
}


def play_round(player1,player2):
    p1_move = player1.play ()
    p2_move = player2.play ()
    p1_payoff,p2_payoff = payoff_matrix[(p1_move,p2_move)]
    player1.update_last_move (p2_move)
    player2.update_last_move (p1_move)
    return p1_payoff,p2_payoff


def play_tournament(players,rounds=200):
    scores = {p:0 for p in players}
    for i,p1 in enumerate (players):
        for p2 in players[i:]:
            for _ in range (rounds):
                p1_payoff,p2_payoff = play_round (p1,p2)
                scores[p1] += p1_payoff
                scores[p2] += p2_payoff
    return scores


results = play_tournament (players)

for player,score in sorted (results.items (),key=lambda x:-x[1]):
    print (f"{player.strategy.__name__}: {score / 1200:.2f} years")
