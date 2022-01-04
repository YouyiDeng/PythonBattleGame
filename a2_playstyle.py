"""
The Playstyle classes for A2.
Docstring examples are not required for Playstyles.

You are responsible for implementing the get_state_score function, as well as
creating classes for both Iterative Minimax and Recursive Minimax.
"""
import sys
from typing import Any, List
import random


class Playstyle:
    """
    The Playstyle superclass.

    is_manual - Whether the class is a manual Playstyle or not.
    battle_queue - The BattleQueue corresponding to the game this Playstyle is
                   being used in.
    """
    is_manual: bool
    battle_queue: 'BattleQueue'

    def __init__(self, battle_queue: 'BattleQueue') -> None:
        """
        Initialize this Playstyle with BattleQueue as its battle queue.
        """
        self.battle_queue = battle_queue
        self.is_manual = True

    def select_attack(self, parameter: Any = None) -> str:
        """
        Return the attack for the next character in this Playstyle's
        battle_queue to perform.

        Return 'X' if a valid move cannot be found.
        """
        raise NotImplementedError

    def copy(self, new_battle_queue: 'BattleQueue') -> 'Playstyle':
        """
        Return a copy of this Playstyle which uses the BattleQueue
        new_battle_queue.
        """
        raise NotImplementedError


class ManualPlaystyle(Playstyle):
    """
    The ManualPlaystyle. Inherits from Playstyle.
    """

    def select_attack(self, parameter: Any = None) -> str:
        """
        Return the attack for the next character in this Playstyle's
        battle_queue to perform.

        parameter represents a key pressed by a player.

        Return 'X' if a valid move cannot be found.
        """
        if parameter in ['A', 'S']:
            return parameter

        return 'X'

    def copy(self, new_battle_queue: 'BattleQueue') -> 'Playstyle':
        """
        Return a copy of this ManualPlaystyle which uses the
        BattleQueue new_battle_queue.
        """
        return ManualPlaystyle(new_battle_queue)


class RandomPlaystyle(Playstyle):
    """
    The Random playstyle. Inherits from Playstyle.
    """
    def __init__(self, battle_queue: 'BattleQueue') -> None:
        """
        Initialize this RandomPlaystyle with BattleQueue as its battle queue.
        """
        super().__init__(battle_queue)
        self.is_manual = False

    def select_attack(self, parameter: Any = None) -> str:
        """
        Return the attack for the next character in this Playstyle's
        battle_queue to perform.

        Return 'X' if a valid move cannot be found.
        """
        actions = self.battle_queue.peek().get_available_actions()

        if not actions:
            return 'X'

        return random.choice(actions)

    def copy(self, new_battle_queue: 'BattleQueue') -> 'Playstyle':
        """
        Return a copy of this RandomPlaystyle which uses the
        BattleQueue new_battle_queue.
        """
        return RandomPlaystyle(new_battle_queue)


def get_state_score(battle_queue: 'BattleQueue') -> int:
    """
    Return an int corresponding to the highest score that the next player in
    battle_queue can guarantee.

    For a state that's over, the score is the HP of the character who still has
    HP if the next player who was supposed to act is the winner. If the next
    player who was supposed to act is the loser, then the score is -1 * the
    HP of the character who still has HP. If there is no winner (i.e. there's
    a tie) then the score is 0.

    >>> from a2_battle_queue import BattleQueue
    >>> from a2_characters import Rogue, Mage
    >>> bq = BattleQueue()
    >>> r = Rogue("r", bq, ManualPlaystyle(bq))
    >>> m = Mage("m", bq, ManualPlaystyle(bq))
    >>> r.enemy = m
    >>> m.enemy = r
    >>> bq.add(r)
    >>> bq.add(m)
    >>> m.set_hp(3)
    >>> get_state_score(bq)
    100
    >>> r.set_hp(40)
    >>> get_state_score(bq)
    40
    >>> bq.remove()
    r (Rogue): 40/100
    >>> bq.add(r)
    >>> get_state_score(bq)
    -10
    """
    new_bq = battle_queue.copy()
    player = new_bq.peek()
    return get_state_score_player(player, new_bq)


def get_state_score_player(orignal_player: 'Character',
                           battle_queue: 'BattleQueue') -> int:
    """
    Return an int corresponding to the highest score that the current_player in
    battle_queue can guarantee.

    >>> from a2_battle_queue import BattleQueue
    >>> from a2_characters import Rogue, Mage
    >>> bq = BattleQueue()
    >>> r = Rogue("r", bq, ManualPlaystyle(bq))
    >>> m = Mage("m", bq, ManualPlaystyle(bq))
    >>> r.enemy = m
    >>> m.enemy = r
    >>> bq.add(r)
    >>> bq.add(m)
    >>> m.set_hp(3)
    >>> get_state_score_player(r, bq)
    100
    >>> r.set_hp(40)
    >>> get_state_score_player(r, bq)
    40
    >>> bq.remove()
    r (Rogue): 40/100
    >>> bq.add(r)
    >>> get_state_score_player(m, bq)
    -10
    """
    if battle_queue.is_over():
        winner = battle_queue.get_winner()
        if winner:
            if orignal_player == winner:
                return winner.get_hp()
            return -winner.get_hp()
        return 0
    actions = battle_queue.peek().get_available_actions()
    scores = []
    for action in actions:
        temp_bq = battle_queue.copy()
        current_player = temp_bq.peek()
        # find the same player in battle queue copy
        if orignal_player == battle_queue.peek():
            player = current_player
        else:
            player = current_player.enemy
        if action == 'A':
            current_player.attack()
        else:
            current_player.special_attack()
        if current_player.get_available_actions() != []:
            temp_bq.remove()
        scores.append(get_state_score_player(player, temp_bq))

    return max(scores)


# TODO: Implement classes for Recursive Minimax and Iterative Minimax
class MinimaxRecursivePlaystyle(Playstyle):
    """
    The MinimaxRecursive playstyle. Inherits from Playstyle.
    """
    def __init__(self, battle_queue: 'BattleQueue') -> None:
        """
        Initialize this MinimaxRecursivePlaystyle with BattleQueue as its
        battle queue.
        """
        super().__init__(battle_queue)
        self.is_manual = False

    def select_attack(self, parameter: Any = None) -> str:
        """
        Return the attack for the next character in this Playstyle's
        battle_queue to perform.

        Return 'X' if a valid move cannot be found.

        >>> from a2_battle_queue import BattleQueue
        >>> from a2_characters import Rogue, Mage
        >>> bq = BattleQueue()
        >>> r = Rogue("r", bq, MinimaxRecursivePlaystyle(bq))
        >>> m = Mage("m", bq, MinimaxRecursivePlaystyle(bq))
        >>> r.enemy = m
        >>> m.enemy = r
        >>> bq.add(r)
        >>> bq.add(m)
        >>> m.set_hp(3)
        >>> r.playstyle.select_attack()
        'A'
        >>> r.set_hp(40)
        >>> r.playstyle.select_attack()
        'A'
        >>> bq.remove()
        r (Rogue): 40/100
        >>> bq.add(r)
        >>> m.playstyle.select_attack()
        'S'
        """
        actions = self.battle_queue.peek().get_available_actions()

        if not actions:
            return 'X'

        highest_score = -sys.maxsize
        score_attack = -sys.maxsize
        score_special_attack = -sys.maxsize

        for action in actions:
            temp_bq = self.battle_queue.copy()
            highest_score = get_state_score(temp_bq)
            current_player = temp_bq.peek()
            if action == 'A':
                current_player.attack()
                if current_player.get_available_actions() != []:
                    temp_bq.remove()
                score_attack = get_state_score_player(current_player, temp_bq)
            else:
                current_player.special_attack()
                if current_player.get_available_actions() != []:
                    temp_bq.remove()
                score_special_attack = get_state_score_player(current_player,
                                                              temp_bq)
        if highest_score == score_attack:
            return 'A'
        if highest_score == score_special_attack:
            return 'S'
        return 'X'

    def copy(self, new_battle_queue: 'BattleQueue') -> 'Playstyle':
        """
        Return a copy of this MinimaxRecursivePlaystyle which uses the
        BattleQueue new_battle_queue.
        """
        return MinimaxRecursivePlaystyle(new_battle_queue)


class MinimaxIterativePlaystyle(Playstyle):
    """
    The Minimax Iterative playstyle. Inherits from Playstyle.
    """
    def __init__(self, battle_queue: 'BattleQueue') -> None:
        """
        Initialize this MinimaxIterativePlaystyle with BattleQueue as its
        battle queue.
        """
        super().__init__(battle_queue)
        self.is_manual = False

    def select_attack(self, parameter: Any = None) -> str:
        """
        Return the attack for the next character in this Playstyle's
        battle_queue to perform.

        Return 'X' if a valid move cannot be found.

        >>> from a2_battle_queue import BattleQueue
        >>> from a2_characters import Rogue, Mage
        >>> bq = BattleQueue()
        >>> r = Rogue("r", bq, MinimaxIterativePlaystyle(bq))
        >>> m = Mage("m", bq, MinimaxIterativePlaystyle(bq))
        >>> r.enemy = m
        >>> m.enemy = r
        >>> bq.add(r)
        >>> bq.add(m)
        >>> m.set_hp(3)
        >>> r.playstyle.select_attack()
        'A'
        >>> r.set_hp(40)
        >>> r.playstyle.select_attack()
        'A'
        >>> bq.remove()
        r (Rogue): 40/100
        >>> bq.add(r)
        >>> m.playstyle.select_attack()
        'S'
        """
        actions = self.battle_queue.peek().get_available_actions()

        if not actions:
            return 'X'

        stack = []
        bq_copy = self.battle_queue.copy()

        root_node = GameStateNode(bq_copy, bq_copy.peek())
        stack.append(root_node)
        count = len(stack)
        while count > 0:
            node = stack.pop()
            if not node.battle_queue.is_over() and node.children is None:
                children_nodes = self.get_children_nodes(node)
                node.children = children_nodes
                stack.append(node)
                for child in children_nodes:
                    stack.append(child)
            elif not node.battle_queue.is_over() and node.children:
                node.highest_score = max([child.highest_score for child in
                                          node.children])
            else:
                winner = node.battle_queue.get_winner()
                if winner and node.current_player == winner:
                    node.highest_score = winner.get_hp()
                elif winner:
                    node.highest_score = -winner.get_hp()
                else:
                    node.highest_score = 0
            count = len(stack)

        highest_score_root = root_node.highest_score
        for child in root_node.children:
            if child.highest_score == highest_score_root:
                return child.action_taken
        return root_node.action_taken

    def get_children_nodes(
            self, parent_node: 'GameStateNode') -> List['GameStateNode']:
        """
        Return a list of subsequent GamStateNode as performing all available
        actions for parent_node.

        >>> from a2_battle_queue import BattleQueue
        >>> from a2_characters import Rogue, Mage
        >>> bq = BattleQueue()
        >>> r = Rogue("r", bq, MinimaxIterativePlaystyle(bq))
        >>> m = Mage("m", bq, MinimaxIterativePlaystyle(bq))
        >>> r.enemy = m
        >>> m.enemy = r
        >>> bq.add(r)
        >>> bq.add(m)
        >>> parent_node = GameStateNode(bq, r)
        >>> c_nodes = r.playstyle.get_children_nodes(parent_node)
        >>> for x in c_nodes:
        ...     print(x.battle_queue)
        m (Mage): 93/100 -> r (Rogue): 100/97
        m (Mage): 88/100 -> r (Rogue): 100/90 -> r (Rogue): 100/90
        """
        children_nodes = []
        bq_copy = parent_node.battle_queue.copy()
        for action in bq_copy.peek().get_available_actions():
            temp_bq = bq_copy.copy()
            current_player = temp_bq.peek()
            # find the same player in battle queue copy
            if parent_node.current_player == parent_node.battle_queue.peek():
                original_player = current_player
            else:
                original_player = current_player.enemy

            if action == 'A':
                current_player.attack()
                if current_player.get_available_actions() != []:
                    temp_bq.remove()
                attack_node = GameStateNode(temp_bq, original_player,
                                            'A')
                children_nodes.append(attack_node)
            else:
                current_player.special_attack()
                if current_player.get_available_actions() != []:
                    temp_bq.remove()
                special_attack_node = GameStateNode(
                    temp_bq, original_player, 'S')
                children_nodes.append(special_attack_node)
        return children_nodes

    def copy(self, new_battle_queue: 'BattleQueue') -> 'Playstyle':
        """
        Return a copy of this MinimaxIterativePlaystyle which uses the
        BattleQueue new_battle_queue.
        """
        return MinimaxIterativePlaystyle(new_battle_queue)


class GameStateNode:
    """
     A class with the tree-node-like structure representing the game state.

     battle_queue - at the point of the game (i.e. the 'state' of the game).
     children - the subtrees reachable from this state.
     highest_score - hithest uaranteed score reachable from this state.
     action_taken - action being taken to get to this state.
     current_player - equivalent current player at this copy of battle_queue.
    """
    battle_queue: 'BattleQueue'
    children: List['GameStateNode']
    highest_score: int
    action_taken: str
    current_player: 'Character'

    def __init__(self, bq: 'BattleQueue', player: 'Character',
                 action: str = 'X',
                 children: List['GameStateNode'] = None) -> None:
        """
        Initialize this SkillDecisionTree with the value value, condition
        function condition, priority number priority, and the children in
        children, if provided.

        >>> from a2_battle_queue import BattleQueue
        >>> from a2_characters import Rogue, Mage
        >>> bq = BattleQueue()
        >>> r = Rogue("r", bq, MinimaxIterativePlaystyle(bq))
        >>> m = Mage("m", bq, MinimaxIterativePlaystyle(bq))
        >>> r.enemy = m
        >>> m.enemy = r
        >>> bq.add(r)
        >>> bq.add(m)
        >>> state_node = GameStateNode(bq, r)
        >>> state_node.children is None
        True
        """
        self.battle_queue = bq
        self.current_player = player
        self.action_taken = action
        self.highest_score = None
        self.children = children[:] if children else None


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config='a2_pyta.txt')

    import doctest
    doctest.testmod()
