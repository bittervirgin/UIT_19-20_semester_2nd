import random



d = 40 #size of chromesome
n = 2**5 #size of population
mssv = 17520556
class Init():
    def _init_(self, problem_size, pop_size):
        self.ind_size = problem_size
        self.pop_size = pop_size

    def generate_rand_value(self):
        return random.randint(0, 1)

    def create_individual(self):
        return [self.generate_rand_value for _ in range(self.ind_size)]

    def create_population(self):
        return [self.create_individual() for _ in range(self.pop_size)]

#crossover one point
def crossover_1x(individual1, individual2):
    individual1_new = individual1.copy()
    individual2_new = individual2.copy()
    #print("Parents 1: ", individual1)
    #print("Parents 2: ", individual2)
    d = len(individual1)
    i = random.randint(0, d)
    for i in range(d):
      individual1_new[i] = individual2[i]
      individual2_new[i] = individual1[i]
    #print("Offspring 1: ", individual1_new)
    #print("Offspring 2: ", individual2_new)
    return individual1_new, individual2_new

#crossover
def crossover_dx(individual1, individual2):
    crossover_rate = 1.0
    individual1_new = individual1.copy()
    individual2_new = individual2.copy()
    d = len(individual1)
    for i in range(d):
        if random.random() < crossover_rate:
            individual1_new[i] = individual2[i]
            individual2_new[i] = individual1[i]
        
    return individual1_new, individual2_new

#calculate fitness of one individual
def compute_fitness(individual):
    return sum(gen for gen in individual)

#POPOP for sGA
#best = [] #save the highest fitness individual



def trap_fucn():
    return

class MPRS():
    def _init_(self):
        self.seed = 17520556
        self.n_upper = 4
        self.n_lower = self.n_upper/2
        self.pop_size = (int)((self.n_upper + self.n_lower)/2)
        self.fitness = 0
        self.avg_fitness_eval = 0
        self.success = 0
        self.population = []
    
    def set_size(self, size):
        self.pop_size = size

    def set_seed(self, seed):
        self.seed = seed

    def crossover_1x(self, individual1, individual2):
        individual1_new = individual1.copy()
        individual2_new = individual2.copy()
        #print("Parents 1: ", individual1)
        #print("Parents 2: ", individual2)
        d = len(individual1)
        i = random.randint(0, d)
        for i in range(d):
            individual1_new[i] = individual2[i]
            individual2_new[i] = individual1[i]
        return individual1_new, individual2_new
    def get_attri(self):
        return self.pop_size
    #crossover
    def crossover_dx(self, individual1, individual2):
        crossover_rate = 1.0
        individual1_new = individual1.copy()
        individual2_new = individual2.copy()
        d = len(individual1)
        for i in range(d):
            if random.random() < crossover_rate:
                individual1_new[i] = individual2[i]
                individual2_new[i] = individual1[i]
        
        return individual1_new, individual2_new

    #calculate fitness of one individual
    def compute_fitness(self, individual):
        self.avg_fitness_eval += 1
        return sum(gen for gen in individual)

    #POPOP for sGA
    def POPOP(self, old_population):
        #Parents-Offspring Pool
        pool = []
        #create new individuals
        for i in range(len(old_population)-1):
            individual_o1, individual_o2 = crossover_1x(old_population[i], old_population[i + 1])
            #add Offsprings to Pool
            pool.append(individual_o1)
            pool.append(individual_o2)
        #add old population to Pool
        pool.append(old_population)
        new_population = [] *len(old_population)
        for i in range(len(old_population)):
        #new_population.append(tournament_selection(pool, i*4, i*4+4))
            new_population.append(self.end(pool, 4))
        for j in range(len(new_population)-1):
            while(compute_fitness(new_population[j]) != compute_fitness(new_population[j+1])):#condition to stop
                self.POPOP(new_population)
        return new_population

    def end(self, pool, k):
        best = []
    
        for i in range(len(pool)-1):
            if(best == 'None') or compute_fitness(pool[i]) > compute_fitness(best):
                best  = pool[i]
            if (compute_fitness(pool[i]) < compute_fitness(best)):
                pool[i] = best
            
        return best

    def set_success(self):
        self.success = 0
    def Bisection1(self, seed):
        self.set_success()
        self.set_seed(seed)
        while (self.success == 0):
            self.n_upper = 4
            self.n_upper = self.n_upper * 2
            upper = self.n_upper
            for i in range(10):
                random.seed(self.seed + i)
                init = Init()
                pop = init.create_population()
                final = self.POPOP(pop)
                if compute_fitness(final[0]) == self.n_upper * 1:
                    self.success = 1
    def Bisection2(self, seed):
        self.set_seed(seed)
        self.set_success()
        self.n_lower = self.n_upper / 2
        while (self.n_upper - self.n_lower)/self.n_upper > 0.1:
            self.pop_size = (int)((self.n_upper + self.n_lower) /2)
            pop_size = self.pop_size
            for j in range(10):
                random.seed(self.seed + j)
                pop = Init(10, pop_size).create_population()
                final = self.POPOP(pop)
                if compute_fitness(final[0]) == self.n_upper * 1:
                    self.fitness += compute_fitness(final[0])
                    self.success = 1
            if (self.success == 1):
                self.n_upper = self.pop_size
            else:
                self.n_lower = self.pop_size
            if (self.n_upper - self.n_lower) <= 2:
                break
    def get_n_upper(self):
        print(self.n_upper)
        #return self.n_upper
    
    def get_avg_fitness(self):
        self.avg_fitness = self.fitness / 10
        return self.avg_fitness
init = MPRS()
mssv = 17520556
for i in range(10):
    init.Bisection1(mssv)
    init.Bisection2(mssv)
    init.set_seed(mssv + 10)
    init.get_n_upper()





