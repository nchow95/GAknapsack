import random

def to_binary(num, bit_size):
    out_bits = []
    power = bit_size
    while power >= 0:
        if 2**power <= num:
            num -= 2**power
            out_bits.append(1)
        else:
            out_bits.append(0)
        power -= 1
    return out_bits

def populate(items, size, max):
    population = []
    for i in range(size):
        population.append(Genetic_Species(items, max))
    return population

def crossover(parent1, parent2, items):
    max = parent1.max_weight
    child = Genetic_Species(items, max)
    while True:
        child.weight = 0
        child.fitness = 0
        for i in range(len(items)):
            child.chromosome[i] = random.choice([parent1.chromosome[i], parent2.chromosome[i]])
            child.weight += child.chromosome[i]*items[i][0]
            child.fitness += child.chromosome[i]*items[i][1]
        if child.weight <= max:
            break
    return child

def lottery(population, items):
    size = len(population)
    coeff = float(1.0/size)
    ind = int(0.1*size)
    population = sorted(population, key=lambda x: x.fitness, reverse=True)
    for i in range(0,size):
        prob = coeff*(1.0-coeff)**(i+1)
        population[i].score = prob*100.0
    population = sorted(population, key=lambda x:x.score, reverse=True)
    population = population[:-ind]
    for i in range(0,size):
        if i in range(0, int(0.5*ind)):
            population.append(crossover(population[i], population[random.randint(0, i)],items))
        elif i in range(int(9.5*ind), size):
            population.append(Genetic_Species(items, population[0].max_weight))
    return population

class Genetic_Species:

    def __init__(self, items, max):
        self.chromosome = to_binary(random.randint(1, 2**len(items)), len(items))
        self.weight = 0
        self.fitness = 0
        self.max_weight = max
        self.calc(items)
        self.score = 0

    def __str__(self):
        return "Chromosome: {}\nWeight: {}\nScore: {}\nFitness: {}".format(
            self.chromosome, self.weight,self.score,self.fitness)

    #calculates both weight and fitness
    def calc(self, items):
        while True:
            self.weight = 0
            self.fitness = 0
            for i in range(len(items)):
                self.weight += self.chromosome[i] * items[i][0]
                self.fitness += self.chromosome[i]*items[i][1]
            if self.weight > self.max_weight:
                self.mutate()
            else:
                break

    def mutate(self):
        while True:
            point = random.randint(0, len(self.chromosome)-1)
            if self.chromosome[point] == 1:
                self.chromosome[point] = 0
                break

if __name__ == "__main__":
    items = [[5,8],[4,7],[3,5],[7,18], [20, 70], [5, 10], [11, 17], [2,3], [19,23], [7,18], [33, 80], [24,100], [6,9],
             [31,40], [60,30], [18,34]]
    population = populate(items, 20, 85)
    for i in range(0,1000000):
        population = lottery(population,items)
        if i%20000 == 0:
            print("Alpha: {}".format(population[0]))
            avg = 0
            for x in range(len(population)):
                avg += population[x].fitness
            avg = float(avg/len(population))
            print("Average Fitness: {}".format(avg))
    print("Alpha: {}".format(population[0]))
