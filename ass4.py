# enter your names and student numbers below
# name1 (s0123456)
# name2 (s6543210)

import exceptions
from pacman import agents, gamestate, util


class BetterReflexAgent(agents.ReflexAgent):
    def evaluate(self, gstate, move):
        dots = gstate.dots.list()
        gstate.apply_move(0,move)

        if gstate.win:
            return float("inf")
        if gstate.loss:
            return float("-inf")
        eval = 0
        pacpos = gstate.pacman
        if move != util.Move.stop:
            if pacpos in gstate.ghosts:
                eval -= 1500
            if pacpos != None:
                for ghost in gstate.ghosts:
                    if gstate.timers[0]>15:
                        if util.manhattan(pacpos, ghost) < 3:
                            eval += 100
                        if pacpos == gstate.ghosts:
                            eval += 200
                    else:
                        if util.manhattan(pacpos, ghost) > 2:
                             eval += 700
            if pacpos == gstate.pellets:
                eval += 500
            if pacpos != None:
                for dot in dots:
                    if util.manhattan(pacpos, dot) < 2:
                        eval += 100
                    if pacpos == dot:
                        eval += 150
            return eval
        else:
            eval -= 500
            return eval

class MinimaxAgent(agents.AdversarialAgent):
    def move(self, gstate):
        eval = []
        player = False
        depth = self.depth
        possMoves = list(gstate.legal_moves_id(0))
        for move in possMoves:
            if move == util.Move.stop:
                possMoves.remove(move)
        for successor in possMoves:
            if(successor != None):
                eval.append(self.miniMax(depth, gstate, player))
        for i in range(0, len(possMoves)):
            if eval[1] == max(eval):
                return possMoves[i]

    def miniMax(self, depth, gstate, player):
        if depth == 0 | gstate.gameover:
            best_value = self.evaluate(gstate)
            return best_value
        if player:
            best_value = float("-inf")
            successors = gstate.successors(1)
            for successor in successors:
                if(successor != None):
                    v = self.miniMax(depth-1, successor, False)
                    best_value = max(v, best_value)
        else:
            best_value = float("inf")
            successors = gstate.successors(0)
            for successor in successors:
                if(successor != None):
                    v = self.miniMax(depth, successor, True)
                    best_value = min(best_value, v)
        return best_value




class AlphabetaAgent(agents.AdversarialAgent):
    def move(self, gstate):
        raise exceptions.EmptyAssignmentError


def better_evaluate(gstate):
    dots = gstate.dots.list()
    successors = gstate.successors(0)
    for node in successors:
        gstate.apply_move(0,node)
        if gstate.win:
            return 500000000000000
        if gstate.loss:
            return -500000000000000

        eval = 0
        pacpos = gstate.pacman
        if pacpos in gstate.ghosts:
            eval -= 1500
        if pacpos != None:
            for ghost in gstate.ghosts:
                if util.manhattan(pacpos, ghost) > 2:
                     eval += 700
        if pacpos == gstate.pellets:
            eval += 200
            if gstate.timers>5:
                if pacpos == gstate.ghosts:
                    eval += 200
        if pacpos != None:
            for dot in dots:
                if util.manhattan(pacpos, dot) < 2:
                    eval += 100
                if pacpos == dot:
                    eval += 150
        return eval

class MultiAlphabetaAgent(agents.AdversarialAgent):
    def move(self, gstate):
        raise exceptions.EmptyBonusAssignmentError
