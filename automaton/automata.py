"""module for discrete evolving automata"""

from math import sqrt, floor
import random
from automaton.cell import Cell, Plant, Organism, Wall


class Automata:
    def __init__(self, cell, env, genome=None) -> None:
        self.GENOME_SIZE = 8

        # self.genome = (
        #     "".join([random.choice(["0", "1"]) for _ in range(2 * self.GENOME_SIZE)])
        #     if genome == None
        #     else genome
        # )
        self.genome = (
            "".join([random.choice(["0", "1"]) for _ in range(2 * self.GENOME_SIZE)])
            if genome == None
            else genome
        )
        self.age = 0

        self.energy = 20
        self.cell = cell
        self.x = self.cell.x
        self.y = self.cell.y
        self.env = env

    def __str__(self) -> str:
        return f"{self.get_genome()} - {self.x}, {self.y}"

    def make_move(self):
        if self.energy < 0:
            self.cell = Cell(self.x, self.y, "empty", self.cell.light)
            self.env.set_cell(self.x, self.y, self.cell)
        self._behavior_decider()
        self.age += 1
        # just for living
        self.energy -= 2

    def _abilities_decider(self) -> None:
        abilities_namings = [
            self.see_ability,
            self.move_ability,
            self.eat_ability,
            self.kill_ability,
            self.cross_ability,
            self.photosynth_ability,
            self.produce_ability,
            self.hybernate_ability,
        ]
        abilities_strength = list(
            map(
                lambda x: int(self.genome[x : x + 2], 2),
                range(0, self.GENOME_SIZE * 2, 2),
            )
        )
        abilities = {
            abilities_namings[i]: abilities_strength[i]
            for i in range(len(abilities_namings))
        }
        return abilities

    def _behavior_decider(self) -> None:
        abilities = self._abilities_decider()
        completed_action = False
        for ability in abilities:
            if abilities[ability] > 0:
                if ability.__name__ != "see_ability":
                    completed_action = ability(abilities[ability])
            if completed_action:
                break

    def move_ability(self, strength) -> None:
        surr = self.see_ability(self._abilities_decider()[self.see_ability])

        def move_away():
            self.env[self.cell.x][self.cell.y] = Cell(
                self.x, self.y, "empty", self.cell.light
            )
            self.cell = self.env.get_cell(self.x, self.y)
            self.env[self.x][self.y] = Organism(self.x, self.y, self.cell.light)
            self.env[self.x][self.y].set_organism(self)
            self.energy -= 4

        def get_possible_moves():
            possible_moves = []
            # розраховує всі можливі рухи для автомата. Можливим рухом вважають такий, який може привести нас на пустий селл до якого ми можемо дійти за один хід.
            for i in range(-strength, strength + 1):
                for j in range(-strength, strength + 1):
                    if (
                        abs(i) + abs(j) <= strength
                        and self.x + i >= 0
                        and self.y + j >= 0
                        and self.x + i <= self.env.get_width()
                        and self.y + j <= self.env.get_height()
                    ):
                        try:
                            if (
                                self.env.get_cell(self.x + i, self.y + j).get_type()
                                == "empty"
                            ):
                                possible_moves.append((self.x + i, self.y + j))
                        except IndexError:
                            print("something went wrong")
            return possible_moves

        def get_all_ranges(
            possible_moves, track_list
        ):  # розраховує відстань до кожного об'єкту зі списку track_list, яка буде між автоматом і об'єктом якщо він переміститься на якийсь з можливих селлів. Формат аутпуту функції : "x_possible_to_go y_possible_to_go" : [(Cell(x_possible_to_go, y_possible_to_go), range_to_an object1), ...]
            ranges = []
            for i in track_list:
                ranges.append(
                    [
                        (cell, sqrt(abs(cell.x - i.x) + abs(cell.y - i.y)))
                        for cell in possible_moves
                    ]
                )
            possible_move_dict = {}
            for i in ranges:
                for j in i:
                    if f"{j[0].x} {j[0].y}" not in possible_move_dict:
                        possible_move_dict[f"{j[0].x} {j[0].y}"] = []
                    possible_move_dict[f"{j[0].x} {j[0].y}"].append(j[1])
            return possible_move_dict

        def escape(
            danger_cells,
        ):  # визначає найкращі за векторним добутком координати для ВТЕЧІ і повертає їх у формі ("x", "y")
            possible_moves = get_possible_moves()
            possible_move_dict = get_all_ranges(possible_moves, danger_cells)
            try:
                return max(
                    possible_move_dict.items(),
                    key=lambda x: sum(possible_move_dict[x[0]]),
                )[0]
            except ValueError:
                print("something went wrong")

        def move_towards(
            pray_cells,
        ):  # визначає найкращі за векторним добутком координати для ПОГОНІ і повертає їх у формі ("x", "y")
            possible_moves = get_possible_moves()
            possible_move_dict = get_all_ranges(possible_moves, pray_cells)
            try:
                return min(
                    possible_move_dict.items(),
                    key=lambda x: sum(possible_move_dict[x[0]]),
                )[0]
            except ValueError:
                pass

        def look_for_danger():
            return [x for x in surr if x.organism != None]

        def look_for_pray():
            return [
                x
                for x in look_for_danger()
                if x.organism._abilities_decider()[x.organism.kill_ability]
                <= self._abilities_decider()[self.kill_ability]
            ]

        def look_for_food():
            return [x for x in surr if x.cell_type == "plant"]

        danger_cells = look_for_danger()
        pray_cells = look_for_pray()
        food_cells = look_for_food()

        # Логіка - у пріоритеті напад на когось. Відразу ж за нападом йде втеча від небезпечного автоматона (напад на слабкого все одно вважається пріоритетом).
        # Не бачимо ворогів узагалі? Йдемо до їжі. Якщо ж навколо узагалі нічого немає - мігруємо у випадковому напрямку на випадкову відстань.
        try:
            if len(pray_cells) > 0:
                self.x, self.y = (int(x) for x in move_towards(pray_cells).split(" "))
                move_away()

            elif len(danger_cells) > 0:
                self.x, self.y = (int(x) for x in escape(danger_cells).split(" "))
                move_away()

            elif len(food_cells) > 0:
                self.x, self.y = (int(x) for x in move_towards(food_cells).split(" "))
                move_away()

            else:
                try:
                    cell_to_migrate = random.choice(get_possible_moves())
                    self.x, self.y = cell_to_migrate[0], cell_to_migrate[1]
                    move_away()
                except IndexError:
                    pass
        except AttributeError:
            pass  # немає куди тікати

    def see_ability(self, strength) -> None:
        return self.env.get_neighbors(self.x, self.y, strength)

    def eat_ability(
        self, strength
    ) -> None:  # їсть якщо стоїть на клітинці з їжею або їжа є на сусідніх клітинках. cell_type клітинки змінюється на "empty" і автомату додається енергія.
        to_eat = [x for x in self.see_ability(1) if x.get_type() == "plant"]
        if self.cell.get_type() == "plant":
            to_eat.append(self.cell)
        if len(to_eat) > 0:
            eaten_plant = random.choice(to_eat)
            self.env[eaten_plant.x][eaten_plant.y] = Cell(
                eaten_plant.x, eaten_plant.y, "empty", eaten_plant.light
            )
            self.energy += (
                strength * 5 if self.energy + strength * 5 <= 50 else 50 - self.energy
            )
            return True
        else:
            return False

    def cross_ability(self, strength) -> None:
        """changed to cross_ability"""
        chosen_cell = None
        if strength > 0 and self.energy > 30:
            nearest_cells = [
                cell
                for cell in self.env.get_neighbors(self.x, self.y)
                if cell.organism != None
            ]
            for cell in nearest_cells:
                if strength == 1 or strength == 2:
                    if abs(self.x - cell.x) == 1 and abs(self.y - cell.y) == 1:
                        chosen_cell = cell
                        break
                elif (self.x - cell.x) == 0 or (self.y - cell.y) == 0:
                    chosen_cell = cell
                    break
                else:
                    return False
            if not chosen_cell:
                return False
            self, chosen_cell.organism = self.crossover(chosen_cell.organism)
            self.energy -= 30
            if strength >= 2:
                self.mutate()
            return True
        return False

    def kill_ability(self, strength) -> None:
        """
        can kill if other.kill_ability < strength
        """
        if strength == 0 or self.energy < 10:
            return False
        else:
            if self._abilities_decider()[self.see_ability] > 0:
                nearest_cells = self.env.get_neighbors(self.x, self.y, 1)
            else:
                nearest_cells = []
            for cell in nearest_cells:
                enemy = cell.organism
                if enemy:
                    if enemy._abilities_decider()[enemy.see_ability] == strength:
                        kill_probability = 0.5
                        self.energy -= 10
                    elif enemy._abilities_decider()[enemy.see_ability] < strength:
                        kill_probability = 1
                        self.energy -= 10
                    else:
                        kill_probability = -1
                    if kill_probability == 1:
                        self.energy += 5 if self.energy <= 30 else 50 - self.energy

                        cell = Cell(self.x, self.y, "empty", self.cell.light)
                        return True
                    elif kill_probability == 0:
                        return True
                    elif kill_probability != -1:
                        break
            return False

    def photosynth_ability(self, strength) -> None:
        lightning = self.env.lighting(self.y)
        if lightning > 5:
            self.energy += (
                (strength * lightning) // 4
                if self.energy + floor(strength * 1.5) <= 50
                else 50 - self.energy
            )
            return True
        return False

    def produce_ability(self, strength) -> None:
        diff_energy = self.energy - 35
        if diff_energy < 5:
            return False
        number_of_child = 0
        # number_of_plants = 0
        if strength <= 1:
            number_of_plants = diff_energy // 10
        elif strength == 2:
            if diff_energy >= 10:
                number_of_child = 1
                number_of_plants = 0
            else:
                number_of_plants = diff_energy // 5
        else:
            if diff_energy >= 10:
                number_of_child = 1
                diff_energy -= 10
            number_of_plants = diff_energy // 5
        nearest_cells = self.env.get_neighbors(self.x, self.y)
        if number_of_child == 0 and number_of_plants == 0:
            return False
        check = False
        for cell in nearest_cells:
            if cell.cell_type != "empty":
                continue
            if number_of_child != 0:
                cell = Organism(cell.x, cell.y, cell.light)
                cell.organism = Automata(cell, self.env, self.genome)
                if random.random() < 0.1:
                    cell.organism.mutate()
                number_of_child -= 1
                self.energy -= 20
                check = True
            if number_of_plants > 0:
                self.env[cell.x][cell.y] = Plant(cell.x, cell.y, cell.light)
                number_of_plants -= 1
                check = True
            if number_of_plants == 0 and number_of_plants == 0:
                self.energy = min(35, self.energy)
                return True
        else:
            if check:
                return True
            return False

    def hybernate_ability(self, strength) -> None:
        if self.energy < 5:
            self.energy += (
                strength if self.energy + strength <= 50 else 50 - self.energy
            )
            return True
        return False

    def mutate(self) -> None:
        mutation_position = random.randint(0, self.GENOME_SIZE)
        self.genome = (
            self.genome[:mutation_position]
            + str(int(self.genome[mutation_position]) ^ 1)
            + self.genome[mutation_position + 1 :]
        )

    def crossover(self, other) -> None:
        if not isinstance(other, Automata):
            raise TypeError("other must be an Automata")
        if self.GENOME_SIZE != other.GENOME_SIZE:
            raise ValueError("other must have the same genome size")
        crossing = random.randint(0, self.GENOME_SIZE)
        self.genome, other.genome = (
            self.genome[0:crossing] + other.genome[crossing:],
            other.genome[0:crossing] + self.genome[crossing:],
        )
        return self, other

    def get_genome(self) -> list:
        return self.genome

    def get_health(self) -> int:
        return self.health

    def get_age(self) -> int:
        return self.age

    def get_energy(self) -> int:
        return self.energy
