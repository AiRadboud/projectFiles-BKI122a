# enter your names and student numbers below
# name1 (s0123456)
# name2 (s6543210)

import exceptions
import numbers
import random
from pacman import agents, gamestate, util


class ContestAgent(agents.PacmanAgent):
    """
    The code below specifies a totally moronic ContestAgent.
    It just moves to the neighbouring cell with the highest game score.
    It does not look ahead and does not even try to avoid ghosts.
    You can do far better!
    """   
    def prepare(self, gstate):
        """
        Use this method for initializing tour ContestAgent.
        The provided stump only calls the prepare of the mother class.
        You might want to add other things, for instance
        calling the precompute_distances() method of the Distancer class
        """
        super().prepare(gstate)

    def move(self, gstate: gamestate.Gamestate) -> util.Move:
        """
        This method gets called every turn, asking the agent
        what move they want to make based on the current gamestate.
        """
        moves = gstate.legal_moves_vector(gstate.agents[self.id])
        scores = {move: self.evaluate(gstate.copy, move) for move in moves}
        max_score = max(scores.values())
        max_moves = [move for move in moves if scores[move] == max_score]
        return random.choice(max_moves)

    def evaluate(self, gstate: gamestate.Gamestate, move: util.Move):
        """
        This method is used by the reflex agent to determine
        the value of a given move if it would be used in a given gamestate.
        """
        closed_set = []
        open_set = [gstate]
        came_from = parent
        gScore = float("inf")
        gScore[0] = 0
        fScore = float("inf")
        fScore[0] = heurtistic(gstate.pacman, gstate.win)
        while open_set:
            current = min(fScore)
            if current == gstate.win:
                return path(came_from, current)

            open_set.remove(current)
            closed_set.append(current)
            for neighbor in current:
                if neighbor in closed_set:
                    continue
                if neighbor not in open_set:
                    open_set.append(neighbor)
                tentative_gScore = gScore[current] + util.manhattan(current, neighbor)
                if tentative_gScore >= gScore[neighbor]:
                    continue
                came_from[neighbor] = current
                gScore[neighbor] = tentative_gScore
                fScore[neighbor] = gScore[neighbor] + heuristic(neighbor, goal)
        return failure


