from random import randint, random
from typing import List
from time import sleep
from tkinter import Canvas


class gene:
    def __init__(self):
        self.ft_total = 0
        self.chromosome: List[int] = []
        self.population: List[List[int]] = []
        # population = List[chromosome]
        self.ft_total = 0
        self.num_chromo = int
        self.num_popul = int

    def generate_chromosome(self, size: int) -> List[int]:
        return [randint(0, 255) for _ in range(size)]

    def generate_population(self, size: int, chromosome_length: int) -> List[List[int]]:
        return [self.generate_chromosome(chromosome_length) for _ in range(size)]

    def chromosome_to_str(self, chromosome: List[int]) -> str:
        return ",".join(map(str, chromosome))

    def population_to_str(self, population: List[List[int]]):
        print("Population: [%s]" % " <> ".join([self.chromosome_to_str(chromosome) for chromosome in population]))

    def calculate_fx(self, chromosome: List[int]) -> int:
        a, b, c = chromosome
        f_x = (a + 2 * b + 3 * c + 4) - 20
        return f_x

    def calculate_fx_population(self, population: List[List[int]]) -> List[int]:
        f_x_list = []
        for chromosome in population:
            f_x_list.append(self.calculate_fx(chromosome))
        return f_x_list

    def calc_fitness(self, f_x: List[int]) -> List[float]:
        return [(1 / (1 + fit)) for fit in f_x]

    def calc_fitness_total(self, f_x: List[int]):
        self.ft_total = sum(self.calc_fitness(f_x))

    def calc_probability(self, f_x: List[int]) -> List[float]:
        fitness = self.calc_fitness(f_x)
        return [fit / self.ft_total for fit in fitness]

    def calc_cum_probability(self, f_x: List[int]) -> List[float]:
        probability = self.calc_probability(f_x)
        cumulative = [sum(probability[:i + 1]) for i in range(len(probability))]
        return cumulative

    def random(self, size: int) -> List[float]:
        return [random() for _ in range(size)]

    def range_max(self, cumulative: List[float], random_values: List[float]) -> List[int]:
        range_list = []
        for val in random_values:
            for i, cum_prob in enumerate(cumulative):
                if val <= cum_prob:
                    range_list.append(i + 1)
                    break
        return range_list

    def chromosome_change(self, population: List[List[int]], range_list: List[int]) -> List[List[int]]:
        return [population[pos - 1] for pos in range_list]

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

    def mutations(self, mutation_rate: float, total_gen: int, population: List[List[int]], random_limit: int) -> List[List[int]]:
        num_mutation = int(mutation_rate * total_gen)
        mutations = [randint(0, random_limit) for _ in range(num_mutation)]
        contador = 0

        for chrom in population:
            for index, _ in enumerate(chrom):
                if contador in mutations:
                    chrom[index] = randint(0, 255)
                contador += 1

        return population

    def draw_chromosomes_on_canvas(self, canvas: Canvas, population: List[List[int]]):
        canvas.delete("all")
        x_offset, y_offset = 0, 0
        rect_size = 40

        for i, chromosome in enumerate(population):
            x = x_offset + i % 10 * rect_size
            y = y_offset + i // 10 * rect_size
            canvas.create_rectangle(x, y, x + rect_size, y + rect_size, fill=f"#{chromosome[0]:02X}{chromosome[1]:02X}{chromosome[2]:02X}")

    def visualize_genetic_algorithm(self, canvas_orig: Canvas, canvas_mid: Canvas, canvas_ag: Canvas, num_chrom: int,
                                    num_pop: int):
        initial_population = self.generate_population(num_pop, num_chrom)
        self.draw_chromosomes_on_canvas(canvas_orig, initial_population)
        canvas_ag.update()
        sleep(1)

        for generation in range(1, 4):
            population = self.generar_generacion_population(num_chrom, num_pop, initial_population)
            self.draw_chromosomes_on_canvas(canvas_mid, population)
            canvas_mid.update()
            sleep(1)

            if generation == 3:
                final_population = self.generar_generacion_population(num_chrom, num_pop, population)
                self.draw_chromosomes_on_canvas(canvas_ag, final_population)
                canvas_ag.update()
                sleep(1)

    def visualize_population(self, canvas: Canvas, population: List[List[int]], num_chrom: int, num_pop: int, label_text: str):
        canvas.delete("all")
        rect_size = 50

        for i, chrom in enumerate(population):
            x = (i % 3) * rect_size
            y = (i // 3) * rect_size
            color_value = self.calculate_fx(chrom)

            normalized_color = int((color_value / 255))
            color_hex = "#{:02X}{:02X}{:02X}".format(normalized_color, 255 - normalized_color, 0)

            rectangle_id = canvas.create_rectangle(x, y, x + rect_size, y + rect_size, fill=color_hex)

    def generar_generacion(self,numChrom:int,numPop:int)->List[int]:
            self.num_chromo = numChrom
            self.num_popul = numPop
            totalGen = numChrom * numPop
            population = self.generate_population(numPop,numChrom)
            print(self.population_to_str(population))
            f_x =self.calculate_fx_population(population)
            print(f_x)
            self.calc_fitness_total(f_x)
            print("total" , self.ft_total)
            probability = self.calc_probability(f_x)
            print("Probabilidades" ,probability)
            cumu_prob = self.calc_cum_probability(f_x)
            print("Probabilidades Acumulads", cumu_prob )
            randoms = self.random(numPop)
            print("Randoms", randoms)
            range_list = self.range_max(cumu_prob,randoms)
            print("rangos ",range_list)
            population = self.chromosome_change(population,range_list)
            print("gene cambio ",population)
            randoms_2 = self.random(numPop)
            print("Randoms", randoms_2)
            crossing = self.selected_crossover(randoms_2, numChrom)
            print("selec cross",crossing )
            cambio = self.crossover(crossing,population)
            print("crossover",cambio)
            gen2 = self.mutations(.10,totalGen,cambio,30)

            return gen2
    
    def generar_generacion_population(self,numChrom:int,numPop:int,pop:List[List[int]])->List[int]:
            self.num_chromo = numChrom
            self.num_popul = numPop
            totalGen = numChrom * numPop
            population = pop
            print(self.population_to_str(population))
            f_x =self.calculate_fx_population(population)
            print(f_x)
            self.calc_fitness_total(f_x)
            print("total" , self.ft_total)
            probability = self.calc_probability(f_x)
            print("Probabilidades" ,probability)
            cumu_prob = self.calc_cum_probability(f_x)
            print("Probabilidades Acumulads", cumu_prob )
            randoms = self.random(numPop)
            print("Randoms", randoms)
            range_list = self.range_max(cumu_prob,randoms)
            print("rangos ",range_list)
            population = self.chromosome_change(population,range_list)
            print("gene cambio ",population)
            randoms_2 = self.random(numPop)
            print("Randoms", randoms_2)
            crossing = self.selected_crossover(randoms_2, numChrom)
            print("selec cross",crossing )
            cambio = self.crossover(crossing,population)
            print("crossover",cambio)
            gen2 = self.mutations(.10,totalGen,cambio,30)

            return gen2
           

#gen = gene()
#gene1=gen.generar_generacion(4,6)
#gen.generar_generacion_population(4,6,gene1)