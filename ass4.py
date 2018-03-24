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
                             eval += 1000
            if pacpos == gstate.pellets:
                eval += 1500
            if pacpos != None:
                for dot in dots:
                    if util.manhattan(pacpos, dot) < 3:
                        eval += 500
                        if util.manhattan(pacpos, dot) < 2:
                            eval += 300
                            if util.manhattan(pacpos, dot) < 1:
                                eval += 100
                    if pacpos == dot:
                        eval += 900
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
        for move in possMoves:
            if(move != None):
                eval.append(self.miniMax(depth, gstate, player))
        for i in range(0, len(possMoves)):
            if eval[i] == max(eval):
                return possMoves[i]

    def miniMax(self, depth, gstate, player):
        if depth == 0 or gstate.gameover:
            best_value = self.evaluate(gstate)
            return best_value
        if player:
            best_value = float("-inf")
            successors = gstate.successors(1)
            for successor in successors:
                v = self.miniMax(depth-1, successor, False)
                best_value = max(v, best_value)
        else:
            best_value = float("inf")
            successors = gstate.successors(0)
            for successor in successors:
                v = self.miniMax(depth, successor, True)
                best_value = min(best_value, v)
        return best_value




class AlphabetaAgent(agents.AdversarialAgent):
    def move(self, gstate):
        eval = []
        player = False
        depth = self.depth
        poss_moves = list(gstate.legal_moves_id(0))
        alpha = float("-inf")
        beta = float("inf")
        for move in poss_moves:
            if move == util.Move.stop:
                poss_moves.remove(move)
        for move in poss_moves:
            if(move != None):
                eval.append(self.Alphabeta(depth, gstate, player, alpha, beta))
        for i in range(0, len(poss_moves)):
            if eval[i] == max(eval):
                return poss_moves[i]

    def Alphabeta(self, depth, gstate, player, alpha, beta):
        if depth == 0 or gstate.gameover:
            best_value = MinimaxAgent.miniMax(self, depth, gstate, player)
            return best_value
        if player:
            v = float("-inf")
            successors = gstate.successors(1)
            for successor in successors:
                v = max(v, self.Alphabeta(depth-1, successor, False, alpha, beta))
                alpha = max(alpha, v)
                if alpha >= beta:
                    break
        else:
            v = float("inf")
            successors = gstate.successors(0)
            for successor in successors:
                v = self.Alphabeta(depth, successor, True, alpha, beta)
                beta = min(beta, v)
                if alpha >= beta:
                    break
        return v


def better_evaluate(gstate):
    evaluate = 0
    if gstate.win:
        evaluate = float("inf")
    if gstate.loss:
        evaluate = float("-inf")

    dist_dots = 0
    for dot in gstate.dots:
        dist_dots += util.manhattan(dot, gstate.pacman)
    evaluate += dist_dots*5
    dist_pellets = 0
    for pellet in gstate.pellets:
        dist_pellets += util.manhattan(pellet, gstate.pacman)
    evaluate += dist_pellets*8
    dist_ghosts = 0
    for ghost in gstate.ghosts:
        dist_ghosts += util.manhattan(ghost, gstate.pacman)
    evaluate -= dist_ghosts*10
    return evaluate


class MultiAlphabetaAgent(agents.AdversarialAgent):
    def move(self, gstate):
        raise exceptions.EmptyBonusAssignmentError
