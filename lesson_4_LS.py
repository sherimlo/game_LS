from random import randint, choice


class GameEntity:
    def __init__(self, name, health, damage):
        self.__name = name
        self.__health = health
        self.__damage = damage

    @property
    def name(self):
        return self.__name

    @property
    def health(self):
        return self.__health

    @health.setter
    def health(self, value):
        if value < 0:
            self.__health = 0
        else:
            self.__health = value

    @property
    def damage(self):
        return self.__damage

    @damage.setter
    def damage(self, value):
        self.__damage = value

    def __str__(self):
        return f'{self.__name} health: {self.health} damage: {self.damage}'


class Boss(GameEntity):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage)
        self.__defence = None
        self.__stunned = False

    def choose_defence(self, heroes):
        hero = choice(heroes)
        self.__defence = hero.ability

    def attack(self, heroes):
        if not self.__stunned:
            for hero in heroes:
                if hero.health > 0:
                    if type(hero) == Berserk and self.__defence != hero.ability:
                        hero.blocked_damage = choice([5, 10])
                        hero.health -= (self.damage - hero.blocked_damage)
                    else:
                        hero.health -= self.damage
        else:
            print("Boss is stunned and misses this round.")
            self.__stunned = False

    @property
    def defence(self):
        return self.__defence

    def stun(self):
        self.__stunned = True

    def __str__(self):
        return 'BOSS ' + super().__str__() + f' defence: {self.__defence}'


class Hero(GameEntity):
    def __init__(self, name, health, damage, ability):
        super().__init__(name, health, damage)
        self.__ability = ability

    @property
    def ability(self):
        return self.__ability

    def attack(self, boss):
        boss.health -= self.damage

    def apply_super_power(self, boss, heroes):
        pass


class Warrior(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, 'CRITICAL_DAMAGE')

    def apply_super_power(self, boss, heroes):
        crit = self.damage * randint(2, 5)
        boss.health -= crit
        print(f'Warrior {self.name} hit critically {crit} to boss.')


class Magic(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, 'BOOST')

    def apply_super_power(self, boss, heroes):
        for hero in heroes:
            if hero.health > 0:
                hero.damage += 5
        print(f'Magic {self.name} boosted the damage of all heroes.')


class Berserk(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, 'BLOCK_DAMAGE_AND_REVERT')
        self.__blocked_damage = 0

    @property
    def blocked_damage(self):
        return self.__blocked_damage

    @blocked_damage.setter
    def blocked_damage(self, value):
        self.__blocked_damage = value

    def apply_super_power(self, boss, heroes):
        boss.health -= self.__blocked_damage
        print(f'Berserk {self.name} reverted {self.__blocked_damage} to boss.')


class Medic(Hero):
    def __init__(self, name, health, damage, heal_points):
        super().__init__(name, health, damage, 'HEAL')
        self.__heal_points = heal_points

    def apply_super_power(self, boss, heroes):
        for hero in heroes:
            if hero.health > 0 and self != hero:
                hero.health += self.__heal_points


class Witcher(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, 'REVIVE')

    def apply_super_power(self, boss, heroes):
        self.health -= boss.damage
        print(f'Witcher {self.name} received {boss.damage} damage from the boss.')
        for hero in heroes:
            if hero.health == 0:
                hero.health = self.health
                self.health = 0
                print(f'Witcher {self.name} revived {hero.name} at the cost of his life.')
                break


class Hacker(Hero):
    def __init__(self, name, health, damage, steal_amount):
        super().__init__(name, health, damage, 'STEAL')
        self.__steal_amount = steal_amount

    @property
    def steal_amount(self):
        return self.__steal_amount

    def apply_super_power(self, boss, heroes):
        if boss.health > 0:
            stolen_health = min(self.__steal_amount, boss.health)
            boss.health -= stolen_health
            target_hero = choice([hero for hero in heroes if hero.health > 0])
            target_hero.health += stolen_health
            print(f'Hacker {self.name} stole {stolen_health} health from the boss and gave it to {target_hero.name}.')


class Avrora(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, 'INVISIBILITY')
        self.__invisibility_used = False
        self.__invisibility_turns = 0
        self.__damage_return = 0

    def apply_super_power(self, boss, heroes):
        if not self.__invisibility_used:
            self.__invisibility_used = True
            self.__invisibility_turns = 2
            self.__damage_return = 0
            print(f'Avrora {self.name} activated invisibility for 2 turns.')
        elif self.__invisibility_turns > 0:
            self.__invisibility_turns -= 1
            self.__damage_return += boss.damage
            print(f'Avrora {self.name} is invisible, damage is stored.')
        else:
            boss.health -= self.__damage_return
            print(f'Avrora {self.name} returned {self.__damage_return} damage to the boss.')
            self.__damage_return = 0


class Thor(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, 'STUN')

    def apply_super_power(self, boss, heroes):
        if randint(1, 100) <= 30:
            boss.stun()
            print(f'Thor {self.name} stunned the boss! The boss skips the next round.')
        else:
            print(f'Thor {self.name} missed the stun chance.')


# Основная игра

round_number = 0


def show_statistics(boss, heroes):
    print(f'ROUND - {round_number} ------------')
    print(boss)
    for hero in heroes:
        print(hero)


def play_round(boss, heroes):
    global round_number
    round_number += 1
    boss.choose_defence(heroes)
    boss.attack(heroes)
    for hero in heroes:
        if hero.health > 0 and boss.health > 0 and boss.defence != hero.ability:
            hero.attack(boss)
            hero.apply_super_power(boss, heroes)
    show_statistics(boss, heroes)


def is_game_over(boss, heroes):
    if boss.health <= 0:
        print('Heroes won!!!')
        return True
    all_heroes_dead = True
    for hero in heroes:
        if hero.health > 0:
            all_heroes_dead = False
            break
    if all_heroes_dead:
        print('Boss won!!!')
        return True
    return False


def start_game():
    boss = Boss(name='Dragon', health=1000, damage=50)
    warrior_1 = Warrior(name='Mario', health=270, damage=10)
    warrior_2 = Warrior(name='Ben', health=280, damage=15)
    magic = Magic(name='Merlin', health=290, damage=10)
    berserk = Berserk(name='Guts', health=260, damage=5)
    doc = Medic(name='Aibolit', health=250, damage=5, heal_points=15)
    assistant = Medic(name='Kristin', health=300, damage=5, heal_points=5)
    witcher = Witcher(name='Geralt', health=300, damage=0)
    hacker = Hacker(name='Neo', health=250, damage=5, steal_amount=40)
    avrora = Avrora(name='Avrora', health=260, damage=8)
    thor = Thor(name='Thor', health=300, damage=20)

    heroes_list = [warrior_1, doc, warrior_2, magic, berserk, assistant, witcher, hacker, avrora, thor]

    show_statistics(boss, heroes_list)
    while not is_game_over(boss, heroes_list):
        play_round(boss, heroes_list)


start_game()
