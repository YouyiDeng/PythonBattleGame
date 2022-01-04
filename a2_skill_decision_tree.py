"""
The SkillDecisionTree class for A2.

You are to implement the pick_skill() method in SkillDecisionTree, as well as
implement create_default_tree() such that it returns the example tree used in
a2.pdf.

This tree will be used during the gameplay of a2_game, but we may test your
SkillDecisionTree with other examples.
"""
from typing import Callable, List, Union
from a2_skills import MageAttack, MageSpecial, RogueAttack, RogueSpecial


class SkillDecisionTree:
    """
    A class representing the SkillDecisionTree used by Sorcerer's in A2.

    value - the skill that this SkillDecisionTree contains.
    condition - the function that this SkillDecisionTree will check.
    priority - the priority number of this SkillDecisionTree.
               You may assume priority numbers are unique (i.e. no two
               SkillDecisionTrees will have the same number.)
    children - the subtrees of this SkillDecisionTree.
    """
    value: 'Skill'
    condition: Callable[['Character', 'Character'], bool]
    priority: int
    children: List['SkillDecisionTree']

    def __init__(self, value: 'Skill',
                 condition: Callable[['Character', 'Character'], bool],
                 priority: int,
                 children: List['SkillDecisionTree'] = None):
        """
        Initialize this SkillDecisionTree with the value value, condition
        function condition, priority number priority, and the children in
        children, if provided.

        >>> from a2_skills import MageAttack
        >>> def f(caster, _):
        ...     return caster.hp > 50
        >>> t = SkillDecisionTree(MageAttack(), f, 1)
        >>> t.priority
        1
        >>> type(t.value) == MageAttack
        True
        """
        self.value = value
        self.condition = condition
        self.priority = priority
        self.children = children[:] if children else []

    def pick_skill(self, caster: 'Character',
                   target: 'Character') -> Union['Skill', None]:
        """
        Return a Skill according to self SkillDecisionTree, of which condition
        takes in caster and target as parameters.  The chosen Skill has the
        highest priority and fulfills all conditions in any trees above it, but
        fails on the tree's own condition if they're not a leaf.

        Precondition: caster and target are not None

        >>> from a2_battle_queue import BattleQueue
        >>> from a2_playstyle import ManualPlaystyle
        >>> from a2_characters import Vampire
        >>> bq = BattleQueue()
        >>> caster = Vampire("Caster", bq, ManualPlaystyle(bq))
        >>> target = Vampire("Target", bq, ManualPlaystyle(bq))
        >>> caster.set_sp(30)
        >>> target.set_hp(20)
        >>> sd_tree = create_default_tree()
        >>> ret_skill = sd_tree.pick_skill(caster, target)
        >>> type(ret_skill).__name__
        'RogueAttack'
        """
        possible_skills = self.get_possible_skills(caster, target)
        if not possible_skills:
            return None
        highest_priority_node = possible_skills[0]
        for i in range(len(possible_skills)):
            if possible_skills[i].priority < highest_priority_node.priority:
                highest_priority_node = possible_skills[i]

        return highest_priority_node.value

    def get_possible_skills(self, caster: 'Character',
                            target: 'Character') -> List['SkillDecisionTree']:
        """
        Return a list of SkillDecisionTree, of which condition takes in
        the Character caster and target as parameters.  The returned list
        contains trees fulfilling all conditions in any trees above it, but
        failing on the tree's own condition if they're not a leaf.
        Returns the list containing only self if self is a leaf.

        precondition: caster and target are not None

        >>> from a2_battle_queue import BattleQueue
        >>> from a2_playstyle import ManualPlaystyle
        >>> from a2_characters import Vampire
        >>> bq = BattleQueue()
        >>> caster = Vampire("Caster", bq, ManualPlaystyle(bq))
        >>> target = Vampire("Target", bq, ManualPlaystyle(bq))
        >>> caster.set_sp(30)
        >>> target.set_hp(20)
        >>> sd_tree = create_default_tree()
        >>> ret_list = sd_tree.get_possible_skills(caster, target)
        >>> [item.priority for item in ret_list]
        [6, 8, 7]
        """
        if self is None:
            return []
        if not self.condition(caster, target) or self.children is None:
            return [self]

        return sum([child.get_possible_skills(caster, target)
                    for child in self.children], [])


def create_default_tree() -> SkillDecisionTree:
    """
    Return a SkillDecisionTree that matches the one described in a2.pdf.

    >>> def get_priorities_in_order(t: SkillDecisionTree) -> list:
    ...     result = [t.priority]
    ...     result += sum([get_priorities_in_order(c) for c in t.children], [])
    ...     return result
    >>> sd_tree = create_default_tree()
    >>> get_priorities_in_order(sd_tree)
    [5, 3, 4, 6, 2, 8, 1, 7]
    """
    sdt6 = SkillDecisionTree(RogueAttack(), f_false, 6)
    sdt4 = SkillDecisionTree(RogueSpecial(), f_target_hp_lt_30, 4, [sdt6])
    sdt3 = SkillDecisionTree(MageAttack(), f_caster_sp_gt_20, 3, [sdt4])

    sdt8 = SkillDecisionTree(RogueAttack(), f_false, 8)
    sdt2 = SkillDecisionTree(MageSpecial(), f_target_sp_gt_40, 2, [sdt8])

    sdt7 = SkillDecisionTree(RogueSpecial(), f_false, 7)
    sdt1 = SkillDecisionTree(RogueAttack(), f_caster_hp_gt_90, 1, [sdt7])

    sdt5 = SkillDecisionTree(MageAttack(), f_caster_hp_gt_50, 5,
                             [sdt3, sdt2, sdt1])
    return sdt5


def f_false(_, __) -> bool:
    """
    Return False

    >>> f_false(_, _)
    False
    """
    return False


def f_target_hp_lt_30(_, target: 'Character') -> bool:
    """
    Return True if target hp is less than 30.

    >>> from a2_battle_queue import BattleQueue
    >>> from a2_playstyle import ManualPlaystyle
    >>> from a2_characters import Vampire
    >>> bq = BattleQueue()
    >>> caster = Vampire("Caster", bq, ManualPlaystyle(bq))
    >>> target = Vampire("Target", bq, ManualPlaystyle(bq))
    >>> target.set_hp(20)
    >>> f_target_hp_lt_30(_, target)
    True
    """
    return target.get_hp() < 30


def f_caster_sp_gt_20(caster: 'Character', _) -> bool:
    """
    Return True if caster sp is greater than 20.

    >>> from a2_battle_queue import BattleQueue
    >>> from a2_playstyle import ManualPlaystyle
    >>> from a2_characters import Vampire
    >>> bq = BattleQueue()
    >>> caster = Vampire("Caster", bq, ManualPlaystyle(bq))
    >>> target = Vampire("Target", bq, ManualPlaystyle(bq))
    >>> caster.set_sp(50)
    >>> f_caster_sp_gt_20(caster, target)
    True
    """
    return caster.get_sp() > 20


def f_target_sp_gt_40(_, target: 'Character') -> bool:
    """
    Return True if target sp is greater than 40.

    >>> from a2_battle_queue import BattleQueue
    >>> from a2_playstyle import ManualPlaystyle
    >>> from a2_characters import Vampire
    >>> bq = BattleQueue()
    >>> caster = Vampire("Caster", bq, ManualPlaystyle(bq))
    >>> target = Vampire("Target", bq, ManualPlaystyle(bq))
    >>> target.set_sp(30)
    >>> f_target_sp_gt_40(caster, target)
    False
    """
    return target.get_sp() > 40


def f_caster_hp_gt_90(caster: 'Character', _) -> bool:
    """
    Return True if caster hp is greater than 90.

    >>> from a2_battle_queue import BattleQueue
    >>> from a2_playstyle import ManualPlaystyle
    >>> from a2_characters import Vampire
    >>> bq = BattleQueue()
    >>> caster = Vampire("Caster", bq, ManualPlaystyle(bq))
    >>> target = Vampire("Target", bq, ManualPlaystyle(bq))
    >>> caster.set_hp(30)
    >>> f_caster_hp_gt_90(caster, target)
    False
    """
    return caster.get_hp() > 90


def f_caster_hp_gt_50(caster: 'Character', _) -> bool:
    """
    Return True if caster hp is greater than 50.

    >>> from a2_battle_queue import BattleQueue
    >>> from a2_playstyle import ManualPlaystyle
    >>> from a2_characters import Vampire
    >>> bq = BattleQueue()
    >>> caster = Vampire("Caster", bq, ManualPlaystyle(bq))
    >>> target = Vampire("Target", bq, ManualPlaystyle(bq))
    >>> caster.set_hp(70)
    >>> f_caster_hp_gt_50(caster, target)
    True
    """
    return caster.get_hp() > 50


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config='a2_pyta.txt')

    import doctest
    doctest.testmod()
