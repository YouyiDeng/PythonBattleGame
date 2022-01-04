"""
The Skill classes for A2.

See a2_characters.py for how these are used.
For any skills you make, you're responsible for making sure their style adheres
to PythonTA and that you include all documentation for it.
"""


class Skill:
    """
    An abstract superclass for all Skills.
    """

    def __init__(self, cost: int, damage: int) -> None:
        """
        Initialize this Skill such that it costs cost SP and deals damage
        damage.
        """
        self._cost = cost
        self._damage = damage

    def get_sp_cost(self) -> int:
        """
        Return the SP cost of this Skill.
        """
        return self._cost

    def use(self, caster: 'Character', target: 'Character') -> None:
        """
        Makes caster use this Skill on target.
        """
        raise NotImplementedError

    def _deal_damage(self, caster: 'Character', target: 'Character') -> None:
        """
        Reduces the SP of caster and inflicts damage on target.
        """
        caster.reduce_sp(self._cost)
        target.apply_damage(self._damage)


class NormalAttack(Skill):
    """
    A class representing a NormalAttack.
    Not to be instantiated.
    """

    def use(self, caster: 'Character', target: 'Character') -> None:
        """
        Makes caster use this Skill on target.
        """
        self._deal_damage(caster, target)
        caster.battle_queue.add(caster)


class MageAttack(NormalAttack):
    """
    A class representing a Mage's Attack.
    """

    def __init__(self) -> None:
        """
        Initialize this MageAttack.

        >>> m = MageAttack()
        >>> m.get_sp_cost()
        5
        """
        super().__init__(5, 20)


class MageSpecial(Skill):
    """
    A class representing a Mage's Special Attack.
    """

    def __init__(self) -> None:
        """
        Initialize this MageAttack.

        >>> m = MageSpecial()
        >>> m.get_sp_cost()
        30
        """
        super().__init__(30, 40)

    def use(self, caster: 'Character', target: 'Character') -> None:
        """
        Makes caster use a Mage's SpecialAttack on target.

        >>> from a2_playstyle import ManualPlaystyle
        >>> from a2_battle_queue import BattleQueue
        >>> from a2_characters import Rogue, Mage
        >>> bq = BattleQueue()
        >>> r = Rogue("r", bq, ManualPlaystyle(bq))
        >>> m = Mage("m", bq, ManualPlaystyle(bq))
        >>> r.enemy = m
        >>> m.enemy = r
        >>> m.special_attack()
        >>> m.get_sp()
        70
        >>> r.get_hp()
        70
        """
        self._deal_damage(caster, target)
        caster.battle_queue.add(target)
        caster.battle_queue.add(caster)


class RogueAttack(NormalAttack):
    """
    A class representing a Rogue's Attack.
    """

    def __init__(self) -> None:
        """
        Initialize this RogueAttack.

        >>> r = RogueAttack()
        >>> r.get_sp_cost()
        3
        """
        super().__init__(3, 15)


class RogueSpecial(Skill):
    """
    A class representing a Rogue's Special Attack.
    """

    def __init__(self) -> None:
        """
        Initialize this RogueSpecial.

        >>> r = RogueSpecial()
        >>> r.get_sp_cost()
        10
        """
        super().__init__(10, 20)

    def use(self, caster: 'Character', target: 'Character') -> None:
        """
        Makes caster use a Rogue's SpecialAttack on target.

        >>> from a2_playstyle import ManualPlaystyle
        >>> from a2_battle_queue import BattleQueue
        >>> from a2_characters import Rogue, Mage
        >>> bq = BattleQueue()
        >>> r = Rogue("r", bq, ManualPlaystyle(bq))
        >>> m = Mage("m", bq, ManualPlaystyle(bq))
        >>> r.enemy = m
        >>> m.enemy = r
        >>> r.special_attack()
        >>> r.get_sp()
        90
        >>> m.get_hp()
        88
        """
        self._deal_damage(caster, target)
        caster.battle_queue.add(caster)
        caster.battle_queue.add(caster)


class VampireAttack(Skill):
    """
    A class representing a Vampire's Attack.
    """

    def __init__(self) -> None:
        """
        Initialize this VampireAttack.

        >>> v = VampireAttack()
        >>> v.get_sp_cost()
        15
        """
        super().__init__(15, 20)

    def use(self, caster: 'Character', target: 'Character') -> None:
        """
        Makes caster use a Vampire's Attack on target.

        >>> from a2_playstyle import ManualPlaystyle
        >>> from a2_battle_queue import BattleQueue
        >>> from a2_characters import Rogue, Vampire
        >>> bq = BattleQueue()
        >>> v = Vampire("v", bq, ManualPlaystyle(bq))
        >>> r = Rogue("r", bq, ManualPlaystyle(bq))
        >>> v.enemy = r
        >>> r.enemy = v
        >>> v.attack()
        >>> v.get_sp()
        85
        >>> r.get_hp()
        90
        >>> v.get_hp()
        110
        """
        target_hp = target.get_hp()
        self._deal_damage(caster, target)
        target_new_hp = target.get_hp()
        caster.set_hp(caster.get_hp() + target_hp - target_new_hp)

        caster.battle_queue.add(caster)


class VampireSpecial(Skill):
    """
    A class representing a Vampire's Special Attack.
    """

    def __init__(self) -> None:
        """
        Initialize this RogueSpecial.

        >>> v = VampireSpecial()
        >>> v.get_sp_cost()
        20
        """
        super().__init__(20, 30)

    def use(self, caster: 'Character', target: 'Character') -> None:
        """
        Makes caster use a Vampire's SpecialAttack on target.

        >>> from a2_playstyle import ManualPlaystyle
        >>> from a2_battle_queue import BattleQueue
        >>> from a2_characters import Rogue, Vampire
        >>> bq = BattleQueue()
        >>> v = Vampire("v", bq, ManualPlaystyle(bq))
        >>> r = Rogue("r", bq, ManualPlaystyle(bq))
        >>> v.enemy = r
        >>> r.enemy = v
        >>> v.special_attack()
        >>> v.get_sp()
        80
        >>> r.get_hp()
        80
        >>> v.get_hp()
        120
        """
        target_hp = target.get_hp()
        self._deal_damage(caster, target)
        target_new_hp = target.get_hp()
        caster.set_hp(caster.get_hp() + target_hp - target_new_hp)

        caster.battle_queue.add(caster)
        caster.battle_queue.add(caster)
        caster.battle_queue.add(target)


class SorcererAttack(Skill):
    """
    A class representing a Sorcerer's Attack.
    """

    def __init__(self) -> None:
        """
        Initialize this SorcererAttack.

        >>> s = SorcererAttack()
        >>> s.get_sp_cost()
        15
        """
        super().__init__(15, 0)
        self._chosen_skill = None
        self._decision_tree = None

    def set_chosen_skill(self, caster: "Character",
                         target: "Character") -> None:
        """
        Set skill based on caster and target of decision_tree.

        >>> from a2_playstyle import ManualPlaystyle
        >>> from a2_battle_queue import BattleQueue
        >>> from a2_characters import Rogue, Sorcerer
        >>> from a2_skill_decision_tree import create_default_tree
        >>> bq = BattleQueue()
        >>> s = Sorcerer("s", bq, ManualPlaystyle(bq))
        >>> r = Rogue("r", bq, ManualPlaystyle(bq))
        >>> s.enemy = r
        >>> r.enemy = s
        >>> s.set_sp(40)
        >>> r.set_hp(50)
        >>> r.set_sp(30)
        >>> s_attack = SorcererAttack()
        >>> s_attack.set_decision_tree(create_default_tree())
        >>> s_attack.set_chosen_skill(s, r)
        >>> s_attack.get_sp_cost()
        15
        """
        skill = self._decision_tree.pick_skill(caster, target)
        self._chosen_skill = skill

    def set_decision_tree(self, sdt: 'SkillDecisionTree') -> None:
        """
        Set attribute _decision_tree tp sdt.
        """
        self._decision_tree = sdt

    def use(self, caster: 'Character', target: 'Character') -> None:
        """
        Makes caster use a Sorcerer's Attack on target.

        >>> from a2_playstyle import ManualPlaystyle
        >>> from a2_battle_queue import BattleQueue
        >>> from a2_characters import Rogue, Sorcerer
        >>> from a2_skill_decision_tree import create_default_tree
        >>> bq = BattleQueue()
        >>> s = Sorcerer("s", bq, ManualPlaystyle(bq))
        >>> r = Rogue("r", bq, ManualPlaystyle(bq))
        >>> s.enemy = r
        >>> r.enemy = s
        >>> s.set_skill_decision_tree(create_default_tree())
        >>> s.attack()
        >>> s.get_sp()
        85
        >>> r.get_hp()
        90
        >>> s.get_hp()
        100
        """
        self.set_chosen_skill(caster, target)
        if self._chosen_skill is not None:
            self._chosen_skill.use(caster, target)
            # adjust sp after doing the attack, as Sorcerer's Attack takes
            # 15 SP regardless of what skill was used
            caster.set_sp(caster.get_sp() +
                          self._chosen_skill.get_sp_cost() - self.get_sp_cost())


class SorcererSpecial(Skill):
    """
    A class representing a Sorcerer's Special Attack.
    """

    def __init__(self) -> None:
        """
        Initialize this SorcererSpecial.

        >>> s = SorcererSpecial()
        >>> s.get_sp_cost()
        20
        """
        super().__init__(20, 25)

    def use(self, caster: 'Character', target: 'Character') -> None:
        """
        Makes caster use a Sorcerer's SpecialAttack on target.

        >>> from a2_playstyle import ManualPlaystyle
        >>> from a2_battle_queue import BattleQueue
        >>> from a2_characters import Rogue, Sorcerer
        >>> from a2_skill_decision_tree import create_default_tree
        >>> bq = BattleQueue()
        >>> s = Sorcerer("s", bq, ManualPlaystyle(bq))
        >>> r = Rogue("r", bq, ManualPlaystyle(bq))
        >>> s.enemy = r
        >>> r.enemy = s
        >>> s.set_skill_decision_tree(create_default_tree())
        >>> s.battle_queue.is_empty()
        True
        >>> s.special_attack()
        >>> s.battle_queue.is_empty()
        False
        >>> s.get_sp()
        80
        >>> r.get_hp()
        85
        >>> s.get_hp()
        100
        >>> s.battle_queue.add(r)
        >>> s.battle_queue.add(r)
        >>> s.battle_queue.add(s)
        >>> s.battle_queue.add(r)
        >>> queue_order = []
        >>> bq_copy = s.battle_queue.copy()
        >>> while not bq_copy.is_empty():
        ...     queue_order.append(bq_copy.remove().get_name())
        >>> queue_order
        ['s', 'r', 'r', 's', 'r']
        >>> s.special_attack()
        >>> queue_order = []
        >>> bq_copy = s.battle_queue.copy()
        >>> while not bq_copy.is_empty():
        ...     queue_order.append(bq_copy.remove().get_name())
        >>> queue_order
        ['s', 'r', 's']
        """
        temp_list = []
        while not caster.battle_queue.is_empty():
            c = caster.battle_queue.remove()
            if c not in temp_list:
                temp_list.append(c)

        while temp_list:
            caster.battle_queue.add(temp_list.pop(0))

        caster.battle_queue.add(caster)
        self._deal_damage(caster, target)


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config='a2_pyta.txt')

    import doctest
    doctest.testmod()
