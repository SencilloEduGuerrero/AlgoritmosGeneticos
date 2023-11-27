from random import randint, random
from typing import List
from time import sleep
from tkinter import Canvas


# Creación de la clase algoritmo genetico llamada 'gene', con sus respectivos atributos.
class gene:
    def __init__(self):
        self.ft_total = 0                       # Fitness total de la población.
        self.chromosome: List[int] = []         # Cromosoma representaod por una lista de enteros.
        self.population: List[List[int]] = []   # Población representada como una lista de cromosomas.

    # Genera un cromosoma aleatorio de un tamaño establecido.
    def generate_chromosome(self, size: int) -> List[int]:
        return [randint(0, 175) for _ in range(size)]

    # Genera una población con un número específico de cromosomas, de un tamaño establecido.
    def generate_population(self, size: int, chromosome_length: int) -> List[List[int]]:
        return [self.generate_chromosome(chromosome_length) for _ in range(size)]

    # Convierte los cromosomas en String.
    def chromosome_to_str(self, chromosome: List[int]) -> str:
        return ",".join(map(str, chromosome))

    # Imrpime poblaciones en String.
    def population_to_str(self, population: List[List[int]]):
        print("Population: [%s]" % " <> ".join([self.chromosome_to_str(chromosome) for chromosome in population]))

    # Calcula el valor fitness (f_x) de un cromosoma.
    def calculate_fx(self, chromosome: List[int]) -> int:
        r, g, b = chromosome
        f_x = (r * g + 200 * b) # - abs(g - 100)
        return f_x

    # Calcula el valor fitness (f_x) para una población.
    def calculate_fx_population(self, population: List[List[int]]) -> List[int]:
        f_x_list = []
        for chromosome in population:
            f_x_list.append(self.calculate_fx(chromosome))
        return f_x_list

    # Calcula el puntaje fitness basado en los valores del fitness.
    def calc_fitness(self, f_x: List[int]) -> List[float]:
        return [(1 / (1 + fit)) for fit in f_x]

    # Calcula el total de la puntuación fitness para una población.
    def calc_fitness_total(self, f_x: List[int]):
        self.ft_total = sum(self.calc_fitness(f_x))

    # Calcula la probabilidad de selección por cada cromosoma basado en los valores fitness.
    def calc_probability(self, f_x: List[int]) -> List[float]:
        fitness = self.calc_fitness(f_x)
        return [fit / self.ft_total for fit in fitness]

    # Calcula la probabilidad acumulada de cada cromosoma.
    def calc_cum_probability(self, f_x: List[int]) -> List[float]:
        probability = self.calc_probability(f_x)
        cumulative = [sum(probability[:i + 1]) for i in range(len(probability))]
        return cumulative

    # Genera una lista de valores aleaotrios entre 0 y 1.
    def random(self, size: int) -> List[float]:
        return [random() for _ in range(size)]

    # Determina el rango del cromosoma por selección basada en la probabilidad acumulada.
    def range_max(self, cumulative: List[float], random_values: List[float]) -> List[int]:
        range_list = []
        for val in random_values:
            for i, cum_prob in enumerate(cumulative):
                if val <= cum_prob:
                    range_list.append(i + 1)
                    break
        return range_list

    # Cambia la población basada en la selección de los indices del cromosoma.
    def chromosome_change(self, population: List[List[int]], range_list: List[int]) -> List[List[int]]:
        return [population[pos - 1] for pos in range_list]

    # Selecciona cromosomas para el crossover basado en los valores aleatorios.
    def selected_crossover(self, random_values: List[float], numC: int) -> List[List[int]]:
        index_selec_cross = []
        index = []
        selec_cross = []
        max_val = numC - 1
        for i, val in enumerate(random_values):
            if val < 0.20:
                selec_cross.append([i + 1, randint(1, max_val)])
                index.append(i + 1)

        if selec_cross:
            temp = selec_cross.pop(0)
            selec_cross.append(temp)

        index_selec_cross.append(index)
        index_selec_cross.append(selec_cross)

        return index_selec_cross

    # Método crossover en la población, donde cambia cromosomas.
    def crossover(self, index_selecross: List, pop: List[List[int]]) -> List[List[int]]:
        pop_copy = pop.copy()
        index_list = index_selecross[0]
        selec_cross = index_selecross[1]

        for i, item in enumerate(index_list):
            item -= 1
            i_b = selec_cross[i]
            a = pop[item]
            b = pop[i_b[0] - 1]
            temp = a[0:i_b[1]] + b[i_b[1]:]
            pop_copy[item] = temp

        return pop_copy

    # Método de mutación en la población basada en el radio de mutación obtenido.
    def mutations(self, mutation_rate: float, total_gen: int, population: List[List[int]], random_limit: int) -> List[List[int]]:
        num_mutation = int(mutation_rate * total_gen)
        mutations = [randint(0, random_limit) for _ in range(num_mutation)]

        green_mutations = [randint(0, random_limit) for _ in range(num_mutation // 2)]
        mutations += green_mutations

        contador = 0

        for chrom in population:
            for index, _ in enumerate(chrom):
                if contador in mutations:
                    if contador in green_mutations:
                        chrom[index] = 0 if index != 1 else 175
                    else:
                        chrom[index] = randint(0, 175)
                contador += 1

        return population

    # Dibuja y muestra los cromosomas en el canvas como rectangulos de diferente colores.
    def draw_chromosomes_on_canvas(self, canvas: Canvas, population: List[List[int]]):
        canvas.delete("all")
        x_offset, y_offset = 0, 0
        rect_size = 10

        for i, chromosome in enumerate(population):
            x = x_offset + i % 40 * rect_size
            y = y_offset + i // 40 * rect_size
            fill_color = "#{:02X}{:02X}{:02X}".format(*tuple(chromosome))
            canvas.create_rectangle(x, y, x + rect_size, y + rect_size, fill=fill_color, outline="")

    # Visualiza el proceso del algoritmo genético en los canvas utilizando 100 generaciones.
    def visualize_genetic_algorithm(self, canvas_orig: Canvas, canvas_mid: Canvas, canvas_ag: Canvas, num_chrom: int, num_pop: int):
        initial_population = self.generate_population(num_pop, num_chrom)
        self.draw_chromosomes_on_canvas(canvas_orig, initial_population)
        self.draw_chromosomes_on_canvas(canvas_mid, initial_population)
        canvas_ag.update()
        sleep(0.25)

        for generation in range(1, 101):
            population = self.generar_generacion_population(num_chrom, num_pop, initial_population)
            self.draw_chromosomes_on_canvas(canvas_mid, population)
            canvas_mid.update()
            sleep(0.25)

            if generation == 100:
                final_population = self.generar_generacion_population(num_chrom, num_pop, population)
                self.draw_chromosomes_on_canvas(canvas_ag, final_population)
                f_x_final = self.calculate_fx_population(final_population)
                print("Final Fitness Values:", f_x_final)
                canvas_ag.update()

    # Visualiza la población en el canvas.
    def visualize_population(self, canvas: Canvas, population: List[List[int]], num_chrom: int, num_pop: int, label_text: str):
        canvas.delete("all")
        rect_size = 10

        for i, chrom in enumerate(population):
            x = (i % 3) * rect_size
            y = (i // 3) * rect_size
            color_value = self.calculate_fx(chrom)

            normalized_color = int((color_value / 175))
            color_hex = "#{:02X}{:02X}{:02X}".format(normalized_color, 175 - normalized_color, 0)

            canvas.create_rectangle(x, y, x + rect_size, y + rect_size, fill=color_hex, outline="")

    # Genera una nueva población basada en las operaciones de algoritmos genéticos.
    def generar_generacion(self, numChrom:int, numPop:int) -> List[int]:
            self.num_chromo = numChrom
            self.num_popul = numPop
            totalGen = numChrom * numPop
            population = self.generate_population(numPop,numChrom)
            print(self.population_to_str(population))
            f_x = self.calculate_fx_population(population)
            print(f_x)
            self.calc_fitness_total(f_x)
            print("total", self.ft_total)
            probability = self.calc_probability(f_x)
            print("Probabilidades", probability)
            cumu_prob = self.calc_cum_probability(f_x)
            print("Probabilidades Acumulads", cumu_prob)
            randoms = self.random(numPop)
            print("Randoms", randoms)
            range_list = self.range_max(cumu_prob, randoms)
            print("rangos ", range_list)
            population = self.chromosome_change(population, range_list)
            print("gene cambio ", population)
            randoms_2 = self.random(numPop)
            print("Randoms", randoms_2)
            crossing = self.selected_crossover(randoms_2, numChrom)
            print("selec cross", crossing)
            cambio = self.crossover(crossing, population)
            print("crossover", cambio)
            gen2 = self.mutations(.20, totalGen, cambio, 175)

            return gen2

    # Genera una población basada en una población y algoritmo genético ya existente o declarado.
    def generar_generacion_population(self, numChrom:int, numPop:int, pop:List[List[int]]) -> List[int]:
            self.num_chromo = numChrom
            self.num_popul = numPop
            totalGen = numChrom * numPop
            population = pop
            print(self.population_to_str(population))
            f_x = self.calculate_fx_population(population)
            print(f_x)
            self.calc_fitness_total(f_x)
            print("total", self.ft_total)
            probability = self.calc_probability(f_x)
            print("Probabilidades", probability)
            cumu_prob = self.calc_cum_probability(f_x)
            print("Probabilidades Acumulads", cumu_prob)
            randoms = self.random(numPop)
            print("Randoms", randoms)
            range_list = self.range_max(cumu_prob,randoms)
            print("rangos ",range_list)
            population = self.chromosome_change(population, range_list)
            print("gene cambio ", population)
            randoms_2 = self.random(numPop)
            print("Randoms", randoms_2)
            crossing = self.selected_crossover(randoms_2, numChrom)
            print("selec cross", crossing)
            cambio = self.crossover(crossing, population)
            print("crossover", cambio)
            gen2 = self.mutations(.20, totalGen, cambio, 175)
            return gen2
