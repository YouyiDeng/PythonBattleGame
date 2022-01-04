"""
The BattleQueue classes for A2.

A BattleQueue is a queue that lets our game know in what order various
characters are going to attack.

BattleQueue has been completed for you, and the class header for
RestrictedBattleQueue has been provided. You must implement
RestrictedBattleQueue and document it accordingly.
"""
from typing import Union


class BattleQueue:
    """
    A class representing a BattleQueue.
    """

    def __init__(self) -> None:
        """
        Initialize this BattleQueue.

        >>> bq = BattleQueue()
        >>> bq.is_empty()
        True
        """
        self._content = []
        self._p1 = None
        self._p2 = None

    def _clean_queue(self) -> None:
        """
        Remove all characters from the front of the Queue that don't have
        any actions available to them.

        >>> bq = BattleQueue()
        >>> from a2_characters import Rogue
        >>> from a2_playstyle import ManualPlaystyle
        >>> c = Rogue("Sophia", bq, ManualPlaystyle(bq))
        >>> c2 = Rogue("Sophia", bq, ManualPlaystyle(bq))
        >>> c.enemy = c2
        >>> c2.enemy = c
        >>> bq.add(c)
        >>> bq.add(c2)
        >>> bq.is_empty()
        False
        """
        while self._content and self._content[0].get_available_actions() == []:
            self._content.pop(0)

    def add(self, character: 'Character') -> None:
        """
        Add character to this BattleQueue.

        >>> bq = BattleQueue()
        >>> from a2_characters import Rogue
        >>> from a2_playstyle import ManualPlaystyle
        >>> c = Rogue("Sophia", bq, ManualPlaystyle(bq))
        >>> c2 = Rogue("Sophia", bq, ManualPlaystyle(bq))
        >>> c.enemy = c2
        >>> c2.enemy = c
        >>> bq.add(c)
        >>> bq.is_empty()
        False
        """
        self._content.append(character)

        if not self._p1:
            self._p1 = character
            self._p2 = character.enemy

    def remove(self) -> 'Character':
        """
        Remove and return the character at the front of this BattleQueue.

        >>> bq = BattleQueue()
        >>> from a2_characters import Rogue
        >>> from a2_playstyle import ManualPlaystyle
        >>> c = Rogue("Sophia", bq, ManualPlaystyle(bq))
        >>> c2 = Rogue("Sophia", bq, ManualPlaystyle(bq))
        >>> c.enemy = c2
        >>> c2.enemy = c
        >>> bq.add(c)
        >>> bq.remove()
        Sophia (Rogue): 100/100
        >>> bq.is_empty()
        True
        """
        self._clean_queue()

        return self._content.pop(0)

    def is_empty(self) -> bool:
        """
        Return whether this BattleQueue is empty (i.e. has no players or
        has no players that can perform any actions).

        >>> bq = BattleQueue()
        >>> bq.is_empty()
        True
        """
        self._clean_queue()

        return self._content == []

    def peek(self) -> 'Character':
        """
        Return the character at the front of this BattleQueue but does not
        remove them.

        If this BattleQueue is empty, returns the first player who was added
        to this BattleQueue.

        >>> bq = BattleQueue()
        >>> from a2_characters import Rogue
        >>> from a2_playstyle import ManualPlaystyle
        >>> c = Rogue("Sophia", bq, ManualPlaystyle(bq))
        >>> c2 = Rogue("Sophia", bq, ManualPlaystyle(bq))
        >>> c.enemy = c2
        >>> c2.enemy = c
        >>> bq.add(c)
        >>> bq.peek()
        Sophia (Rogue): 100/100
        >>> bq.is_empty()
        False
        """
        self._clean_queue()

        if self._content:
            return self._content[0]

        return self._p1

    def is_over(self) -> bool:
        """
        Return whether the game being carried out in this BattleQueue is over
        or not.

        A game is considered over if:
            - Both players have no skills that they can use.
            - One player has 0 HP
            or
            - The BattleQueue is empty.

        >>> bq = BattleQueue()
        >>> bq.is_over()
        True

        >>> from a2_characters import Rogue
        >>> from a2_playstyle import ManualPlaystyle
        >>> c = Rogue("Sophia", bq, ManualPlaystyle(bq))
        >>> c2 = Rogue("Sophia", bq, ManualPlaystyle(bq))
        >>> c.enemy = c2
        >>> c2.enemy = c
        >>> bq.add(c)
        >>> bq.is_over()
        False
        """
        if self.is_empty():
            return True

        if self._p1.get_hp() == 0 or self._p2.get_hp() == 0:
            return True

        return False

    def get_winner(self) -> Union['Character', None]:
        """
        Return the winner of the game being carried out in this BattleQueue
        if the game is over. Otherwise, return None.

        >>> bq = BattleQueue()
        >>> from a2_characters import Rogue
        >>> from a2_playstyle import ManualPlaystyle
        >>> c = Rogue("Sophia", bq, ManualPlaystyle(bq))
        >>> c2 = Rogue("Sophia", bq, ManualPlaystyle(bq))
        >>> c.enemy = c2
        >>> c2.enemy = c
        >>> bq.add(c)
        >>> bq.get_winner()
        """
        if not self.is_over():
            return None

        if self._p1.get_hp() == 0:
            return self._p2
        elif self._p2.get_hp() == 0:
            return self._p1

        return None

    def copy(self) -> 'BattleQueue':
        """
        Return a copy of this BattleQueue. The copy contains copies of the
        characters inside this BattleQueue, so any changes that rely on
        the copy do not affect this BattleQueue.

        >>> bq = BattleQueue()
        >>> from a2_characters import Rogue
        >>> from a2_playstyle import ManualPlaystyle
        >>> c = Rogue("r", bq, ManualPlaystyle(bq))
        >>> c2 = Rogue("r2", bq, ManualPlaystyle(bq))
        >>> c.enemy = c2
        >>> c2.enemy = c
        >>> bq.add(c)
        >>> bq.add(c2)
        >>> new_bq = bq.copy()
        >>> new_bq.peek().attack()
        >>> new_bq
        r (Rogue): 100/97 -> r2 (Rogue): 95/100 -> r (Rogue): 100/97
        >>> bq
        r (Rogue): 100/100 -> r2 (Rogue): 100/100
        """
        new_battle_queue = BattleQueue()

        p1_copy = self._p1.copy(new_battle_queue)
        p2_copy = self._p2.copy(new_battle_queue)
        p1_copy.enemy = p2_copy
        p2_copy.enemy = p1_copy

        new_battle_queue.add(p1_copy)
        if not new_battle_queue.is_empty():
            new_battle_queue.remove()

        for character in self._content:
            if character == self._p1:
                new_battle_queue.add(p1_copy)
            else:
                new_battle_queue.add(p2_copy)

        return new_battle_queue

    def __repr__(self) -> str:
        """
        Return a representation of this BattleQueue.

        >>> bq = BattleQueue()
        >>> from a2_characters import Rogue
        >>> from a2_playstyle import ManualPlaystyle
        >>> c = Rogue("r", bq, ManualPlaystyle(bq))
        >>> c2 = Rogue("r2", bq, ManualPlaystyle(bq))
        >>> c.enemy = c2
        >>> c2.enemy = c
        >>> bq.add(c)
        >>> bq.add(c2)
        >>> bq
        r (Rogue): 100/100 -> r2 (Rogue): 100/100
        """
        return " -> ".join([repr(character) for character in self._content])


class RestrictedBattleQueue(BattleQueue):
    """
    A class representing a RestrictedBattleQueue.

    Rules for a RestrictedBattleQueue:
    - The first time each character is added to the RestrictedBattleQueue,
      they're able to add.

    For the below, you may assume that the character at the front of the
    RestrictedBattleQueue is the one adding:
    - Characters that are added to the RestrictedBattleQueue by a character
      other than themselves cannot add.
      i.e. if the RestrictedBattleQueue looks like:
      Character order: A -> B
      Able to add:     Y    Y

      Then if A tried to add B to the RestrictedBattleQueue, it would look like:
      Character order: A -> B -> B
      Able to add:     Y    Y    N
    - Characters that have 2 copies of themselves in the RestrictedBattleQueue
      already that can add cannot add.
      i.e. if the RestrictedBattleQueue looks like:
      Character order: A -> A -> B
      Able to add:     Y    Y    Y

      Then if A tried to add themselves in, the RestrictedBattleQueue would
      look like:
      Character order: A -> A -> B -> A
      Able to add:     Y    Y    Y    N

      If we removed from the RestrictedBattleQueue and tried to add A in again,
      then it would look like:
      Character order: A -> B -> A -> A
      Able to add:     Y    Y    N    Y
    """

    def __init__(self) -> None:
        """
        Initialize this RestrictedBattleQueue.

        >>> rbq = RestrictedBattleQueue()
        >>> rbq.is_empty()
        True
        """
        super().__init__()
        self._add_status = []

    def copy(self) -> 'RestrictedBattleQueue':
        """
        Return a copy of this RestrictedBattleQueue. The copy contains copies
        of the characters inside this RestrictedBattleQueue and their abiliies
        to add to this RestrictedBattleQueue, so any changes that rely on
        the copy do not affect this RestrictedBattleQueue.

        >>> rbq = RestrictedBattleQueue()
        >>> from a2_characters import Rogue
        >>> from a2_playstyle import ManualPlaystyle
        >>> c = Rogue("r", rbq, ManualPlaystyle(rbq))
        >>> c2 = Rogue("r2", rbq, ManualPlaystyle(rbq))
        >>> c.enemy = c2
        >>> c2.enemy = c
        >>> rbq.add(c)
        >>> rbq.add(c2)
        >>> new_rbq = rbq.copy()
        >>> new_rbq.peek().attack()
        >>> new_rbq
        r (Rogue): 100/97 -> r2 (Rogue): 95/100 -> r (Rogue): 100/97
        >>> rbq
        r (Rogue): 100/100 -> r2 (Rogue): 100/100
        """
        new_r_battle_queue = RestrictedBattleQueue()

        p1_copy = self._p1.copy(new_r_battle_queue)
        p2_copy = self._p2.copy(new_r_battle_queue)
        p1_copy.enemy = p2_copy
        p2_copy.enemy = p1_copy

        new_r_battle_queue.add(p1_copy)
        if not new_r_battle_queue.is_empty():
            new_r_battle_queue.remove()

        for i in range(len(self._content)):
            if self._content[i] == self._p1:
                new_r_battle_queue.add(p1_copy)
            else:
                new_r_battle_queue.add(p2_copy)

        return new_r_battle_queue

    def add(self, character: 'Character') -> None:
        """
        Add character to this RestrictedBattleQueue.

        >>> rbq = RestrictedBattleQueue()
        >>> from a2_characters import Rogue
        >>> from a2_playstyle import ManualPlaystyle
        >>> c = Rogue("Sophia", rbq, ManualPlaystyle(rbq))
        >>> c2 = Rogue("Sophia", rbq, ManualPlaystyle(rbq))
        >>> c.enemy = c2
        >>> c2.enemy = c
        >>> rbq.add(c)
        >>> rbq.is_empty()
        False
        >>> rbq
        Sophia (Rogue): 100/100
        >>> rbq.add(c2)
        >>> rbq
        Sophia (Rogue): 100/100 -> Sophia (Rogue): 100/100
        """
        if not self._p1:
            self._p1 = character
            self._p2 = character.enemy

        exist_count = 0
        for c in self._content:
            if c == character:
                exist_count += 1
        if exist_count == 0:
            # first time character is added to the RestrictedBattleQueue
            self._content.append(character)
            self._add_status.append(True)
            return
        front_c = self._content[0]
        front_c_add_status = self._add_status[0]

        if front_c_add_status:
            if front_c == character:
                add_ability_count = self.get_add_ability_count(front_c)
                if add_ability_count >= 2:
                    self._content.append(character)
                    self._add_status.append(False)
                else:
                    self._content.append(character)
                    self._add_status.append(True)
            else:
                self._content.append(character)
                self._add_status.append(False)

    def get_add_ability_count(self, character: 'Character') -> int:
        """
        Return how many instances of Character characters with the ability to
        add to the RestrictedBattleQueue.

        >>> rbq = RestrictedBattleQueue()
        >>> from a2_characters import Rogue
        >>> from a2_playstyle import ManualPlaystyle
        >>> c = Rogue("Sophia", rbq, ManualPlaystyle(rbq))
        >>> c2 = Rogue("Sophia", rbq, ManualPlaystyle(rbq))
        >>> c.enemy = c2
        >>> c2.enemy = c
        >>> rbq.add(c)
        >>> rbq.get_add_ability_count(c)
        1
        >>> rbq.get_add_ability_count(c2)
        0
        """
        count = 0
        for i in range(len(self._content)):
            if self._content[i] == character:
                if self._add_status[i]:
                    count += 1
        return count

    def _clean_queue(self) -> None:
        """
        Remove all characters from the front of the Queue that don't have
        any actions available to them.

        >>> rbq = RestrictedBattleQueue()
        >>> from a2_characters import Rogue
        >>> from a2_playstyle import ManualPlaystyle
        >>> c = Rogue("Sophia 1", rbq, ManualPlaystyle(rbq))
        >>> c2 = Rogue("Sophia 2", rbq, ManualPlaystyle(rbq))
        >>> c.enemy = c2
        >>> c2.enemy = c
        >>> rbq.add(c)
        >>> rbq.add(c2)
        >>> rbq.peek()
        Sophia 1 (Rogue): 100/100
        >>> c.set_sp(2)
        >>> rbq.peek()
        Sophia 2 (Rogue): 100/100
        """
        super()._clean_queue()
        if not self._content:
            self._add_status = []
        else:
            self._add_status = self._add_status[-len(self._content):]

    def remove(self) -> 'Character':
        """
        Remove and return the character at the front of this BattleQueue.

        >>> rbq = RestrictedBattleQueue()
        >>> from a2_characters import Rogue
        >>> from a2_playstyle import ManualPlaystyle
        >>> c = Rogue("Sophia 1", rbq, ManualPlaystyle(rbq))
        >>> c2 = Rogue("Sophia 2", rbq, ManualPlaystyle(rbq))
        >>> c.enemy = c2
        >>> c2.enemy = c
        >>> rbq.add(c)
        >>> rbq.remove()
        Sophia 1 (Rogue): 100/100
        >>> rbq.is_empty()
        True
        """
        self._clean_queue()
        self._add_status.pop(0)
        return self._content.pop(0)


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config='a2_pyta.txt')

    import doctest
    doctest.testmod()
