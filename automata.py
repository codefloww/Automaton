"""module for discrete evolving automata"""
from math import sqrt, floor
import random
from environment import Environment
from cell import Cell


class Automata:
    def __init__(self, cell, env) -> None:
        self.GENOME_SIZE = 8

        self.genome = "0" * (2 * self.GENOME_SIZE)
        # self.health = 10

        self.age = 0
        self.energy = 50
        self.cell = cell
        self.x = self.cell.x
        self.y = self.cell.y
        self.env = env

    def __str__(self) -> str:
        return f"{self.get_genome()} - {self.x}, {self.y}"

    def make_move(self):
        self._behavior_decider()

    def _abilities_decider(self) -> None:
        abilities_namings = [
            self.see_ability,
            self.move_ability,
            self.eat_ability,
            self.kill_ability,
            self.photosynth_ability,
            self.hybernate_ability,
            self.reproduce_ability,
            self.produce_ability,
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
        del abilities[self.see_ability]
        completed_action = False
        for ability in abilities:
            if abilities[ability] > 0:
                completed_action = ability(abilities[ability], self.env)
            if completed_action:
                break

    def move_ability(self, strength) -> None:
        surr = self.see_ability(self._abilities_decider()[self.see_ability])

        def move_away():  # змушує автомат лівнути зі своєї клітинки і перейти в іншу, і, відповідно, глобально змінює грід.
            self.cell.organism = None
            self.cell = self.env.get_cell(self.x, self.y)
            self.env.get_cell(self.x, self.y).organism = self
            self.energy -= 1

        def get_possible_moves():
            possible_moves = []
            # розраховує всі можливі рухи для автомата. Можливим рухом вважають такий, який може привести нас на пустий селл до якого ми можемо дійти за один хід.
            for i in range(-strength, strength + 1):
                for j in range(-strength, strength + 1):
                    if (
                        abs(i) + abs(j) <= strength
                        and self.x + i >= 0
                        and self.y + j >= 0
                    ):
                        try:
                            possible_moves.append(
                                self.env.get_cell(self.x + i, self.y + j)
                            ) if self.env.get_cell(
                                self.x + i, self.y + j
                            ).organism == None else 1
                        except IndexError:
                            pass
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

            if len(possible_move_dict) == 0:
                print(possible_moves, track_list)
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
                pass

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
                x for x in look_for_danger() if x.organism.energy <= self.energy
            ]  # замість self.energy підбиратимемо по силі бою, але зараз йой най буде

        def look_for_food():
            return [x for x in surr if x.cell_type == "plant"]

        danger_cells = look_for_danger()
        pray_cells = look_for_pray()
        food_cells = look_for_food()

        # Логіка - у пріоритеті напад на когось. Відразу ж за нападом йде втеча від небезпечного автоматона (напад на слабкого все одно вважається пріоритетом).
        # Не бачимо ворогів узагалі? Йдемо до їжі. Якщо ж навколо узагалі нічого немає - мігруємо у випадковому напрямку на випадкову відстань.
        # По факту - логіка агресора, але можна легко поміняти і взагалі ввести типи клітин по агресивності.
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
                    self.x, self.y = cell_to_migrate.x, cell_to_migrate.y
                    move_away()
                except IndexError:
                    pass
        except AttributeError:
            pass  # немає куди тікати

    def see_ability(self, strength) -> list:
        return self.env.get_neighbors(self.x, self.y, strength)

    def eat_ability(
        self, strength
    ) -> None:  # їсть якщо стоїть на клітинці з їжею або їжа є на сусідніх клітинках. cell_type клітинки змінюється на "empty" і автомату додається енергія.
        to_eat = [x for x in self.see_ability(1) if x.cell_type == "plant"]
        to_eat.append(self.cell) if self.cell.cell_type == "plant" else 1
        if len(to_eat) > 0:
            random.choice(to_eat).cell_type = "empty"
            self.energy += (
                strength * 5 if self.energy + strength * 5 <= 50 else 50 - self.energy
            )

            return True
        else:
            return False

    def reproduce_ability(self, strength) -> bool:
        """changed to cross_ability"""
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
                        kill_probability = random.randint(0, 1)
                        self.energy -= 10
                    elif enemy._abilities_decider()[enemy.see_ability] < strength:
                        kill_probability = 1
                        self.energy -= 10
                    else:
                        kill_probability = -1
                    if kill_probability == 1:
                        self.env.killed_before.append(enemy)
                        self.energy += 20 if self.energy <= 30 else 50 - self.energy

                        enemy.cell.organism = None
                        return True
                    if kill_probability != -1:
                        break
            else:
                return False

    def photosynth_ability(self, strength) -> None:
        self.energy += (
            floor(strength * 1.5)
            if self.energy + floor(strength * 1.5) <= 50
            else 50 - self.energy
        )
        return True

    def produce_ability(self, strength) -> bool:
        diff_energy = self.energy - 40
        if diff_energy < 5:
            return False
        if strength <= 1:
            number_of_plants = diff_energy // 10
        else:
            number_of_plants = diff_energy // 5
        nearest_cells = self.env.get_neighbors(self.x, self.y)
        for cell in nearest_cells:
            if number_of_plants > 0:
                if cell.cell_type == "empty":
                    self.env.grid[cell.x][cell.y](Cell(cell.x, cell.y, "plant"))
                    number_of_plants -= 1
                if number_of_plants == 0:
                    break
            else:
                break
        else:
            return False
        self.energy = 50
        return True

    def hybernate_ability(self, strength) -> None:

        if random.randint(0, 100) > strength * 10:
            return self.photosynth_ability(
                self._abilities_decider()[self.photosynth_ability]
            )
        else:
            self.energy += (
                strength if self.energy + strength <= 50 else 50 - self.energy
            )
            return True

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

    def get_genome(self) -> str:
        return self.genome

    def get_age(self) -> int:
        return self.age

    def get_energy(self) -> int:
        return self.energy


if __name__ == "__main__":
    # Змінив метод __str__ класу Cell на оцей рядок : return "M" if self.organism != None else "_" для кращих результатів.
    env = Environment(10, 10)
    my_cell = env.get_cell(0, 0)
    authomatas = []

    for i in range(50):
        _cell = Cell(random.randint(0, 8), random.randint(0, 8))
        _cell.organism = Automata(_cell, env)
        env.set_cell(_cell.x, _cell.y, _cell)
        authomatas.append(_cell.organism)
    for i in range(50):
        env.get_cell(random.randint(0, 9), random.randint(0, 9)).cell_type = "plant"
    print(env)
    for i in range(10):
        for j in authomatas:
            j.make_move()
        print(env)
        print()
    print(env.killed_before)
