import numpy as np
import random
from numba import jit
from matplotlib import pyplot as plt



d = 10 #size of chromesome
n = 2**5 #size of population
mssv = 17520556
def generate_rand_value():
    return random.randint(0, 1)
@jit
def create_individual(d):
    return [random.randint(0, 1) for _ in range(d)]
@jit
def create_population(d,n):
    return [create_individual(d) for _ in range(n)]

#crossover one point
@jit
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

#POPOP for sGA
# Trap function
@jit
def trap_function(X):
    d = len(X)
    fitness_value = 0
    X = np.array(X)  
    fitness_value = 0
    for i in range(0, d, 5):
        tmp = np.sum(X[i: 5 + i], axis=0)
        if (tmp < 5):
            tmp = 5 - 1 - tmp
        #tmp[np.where(tmp < 5).nonzero()] = 5 - 1 - tmp[np.where(tmp < 5).nonzero()]
        fitness_value += tmp
    return fitness_value
@jit
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
sum1 = 0

def compute_fitness(individual):
    return sum(gene1 for gene1 in individual)
fitness_eval = 0

#POPOP for sGA
@jit
def POPOP(old_population, fitness_eval, crossover):
    #Parents-Offspring Pool
    pool = []
    #create new individuals
    for i in range(len(old_population)-1):
        if crossover == "dx":
            individual_o1, individual_o2 = crossover_dx(old_population[i], old_population[i + 1])
        if crossover == "1x":
            individual_o1, individual_o2 = crossover_1x(old_population[i], old_population[i + 1])
        #add Offsprings to Pool
        pool.append(individual_o1)
        pool.append(individual_o2)
        #add old population to Pool
    pool.append(old_population)
    new_population = [] *len(old_population)
    for i in range(len(old_population)):
    #new_population.append(tournament_selection(pool, i*4, i*4+4))
        pop, fitness_eval = end(pool, 4, fitness_eval)
        new_population.append(pop)
    for j in range(len(new_population)-1):
        while(trap_function(new_population[j]) != trap_function(new_population[j+1])):#condition to stop
            POPOP(new_population, fitness_eval, crossover)
            fitness_eval += 2
    print(",,")
    return new_population, fitness_eval
@jit
def end(pool, k, fitness_eval):
    best = []
    fitness_eval = fitness_eval
    for i in range(len(pool)-1):
        if(best == 'None') or trap_function(pool[i]) > trap_function(best):
            best  = pool[i]
            fitness_eval += 2
        if (trap_function(pool[i]) < trap_function(best)):
            pool[i] = best
            fitness_eval += 2
        return best, fitness_eval
n_upper = 4
#Bisection phase 1
@jit
def Bisection1(seed, d, n_upper, fitness_eval, crossover):
    success = 0
    while (success == 0):
        n_upper = n_upper * 2
        for i in range(10):
            random.seed(seed + i)
            pop = create_population(d, n_upper)
            final, fitness_eval = POPOP(pop, fitness_eval, crossover)
            if compute_fitness(final[0]) == n_upper * 1:
                success = 1
                fitness_eval += 1
    return n_upper, fitness_eval

#Bisection phase 2
@jit
def Bisection2(seed, d, n_upper, fitness_eval, crossover):
    success = 0
    n_lower = n_upper / 2
    while (n_upper - n_lower)/n_upper > 0.1:
        pop_size = (int)((n_upper + n_lower) /2)
        for j in range(10):
            random.seed(seed + j)
            pop = create_population(d, pop_size)
            final, eval = POPOP(pop, fitness_eval, crossover)
            fitness_eval = fitness_eval + eval
            if compute_fitness(final[0]) == n_upper * 1:
                success = 1
                fitness_eval += 1
        if (success == 1):
            n_upper = pop_size
        else:
            n_lower = pop_size
        if (n_upper - n_lower) <= 2:
            break
    return n_upper, fitness_eval



###main program###
mssv = 17520556
eval = 0
list_rslt_trap_1x = []
list_eval_trap_1x = []
list_rslt_trap_dx = []
list_eval_trap_dx = []
mean_eval_1x = []
mean_bound_1x = []
d = 10
x_vis = []
for _ in range(5):
    sum_rslt = 0
    sum_eval = 0
    eval = 0
    n_upper = 4
    for i in range(10):
        print(".")
        n_upper, eval = Bisection1(mssv, d, n_upper, eval, "1x")
        result, eval = Bisection2(mssv, d, n_upper, eval, "1x")
        list_rslt_trap_1x.append(result)
        list_eval_trap_1x.append(eval)
        if i == 0:
            with open(("log_1x__trap_{0}.txt").format(d), "w") as f:
                f.write("\n MSSV:")
                f.write("".join('%a' % mssv))
                f.write('\n Upper Bound: ')
                f.write("".join('%d' % result))
                f.write('\n Fitness eval: ')
                f.write("".join('%d' % eval))
        else:
            with open(("log_1x__trap_{0}.txt").format(d), "a") as f:
                f.write("\n MSSV:")
                f.write("".join('%a' % mssv))
                f.write('\n Upper Bound: ')
                f.write("".join('%d' % result))
                f.write('\n Fitness eval: ')
                f.write("".join('%d' % eval))
        mssv += 10
    for i in range(len(list_rslt_trap_1x)):
        sum_rslt += list_rslt_trap_1x[i]
    mean_bound_1x.append(sum_rslt/10)
    for i in range(len(list_eval_trap_1x)):
        sum_eval += list_eval_trap_1x[i]
    mean_eval_1x.append(sum_eval/10)
    with open(("log_1x_trap_{0}.txt").format(d), "a") as f:
        f.write("Mean result")
        f.write("".join('%a' % (sum_rslt/10)))
        f.write("Mean result")
        f.write("".join('%a' % (sum_eval/10)))
    print(d)
    x_vis.append(d)
    d = d*2
print("Mean eval", mean_eval_1x)
print("\n Mean Bound", mean_bound_1x)
y_vis1 = mean_eval_1x


################
mean_eval_dx = []
mean_bound_dx = []

for _ in range(5):
    sum_rslt = 0
    sum_eval = 0
    eval = 0
    n_upper = 4
    for i in range(10):
        print(".")
        n_upper, eval = Bisection1(mssv, d, n_upper, eval, "1x")
        result, eval = Bisection2(mssv, d, n_upper, eval, "1x")
        list_rslt_trap_dx.append(result)
        list_eval_trap_dx.append(eval)
        if i == 0:
            with open(("log_dx__trap_{0}.txt").format(d), "w") as f:
                f.write("\n MSSV:")
                f.write("".join('%a' % mssv))
                f.write('\n Upper Bound: ')
                f.write("".join('%d' % result))
                f.write('\n Fitness eval: ')
                f.write("".join('%d' % eval))
        else:
            with open(("log_dx__trap_{0}.txt").format(d), "a") as f:
                f.write("\n MSSV:")
                f.write("".join('%a' % mssv))
                f.write('\n Upper Bound: ')
                f.write("".join('%d' % result))
                f.write('\n Fitness eval: ')
                f.write("".join('%d' % eval))
        mssv += 10
    for i in range(len(list_rslt_trap_1x)):
        sum_rslt += list_rslt_trap_1x[i]
    mean_bound_dx.append(sum_rslt/10)
    for i in range(len(list_eval_trap_1x)):
        sum_eval += list_eval_trap_1x[i]
    mean_eval_dx.append(sum_eval/10)
    with open(("log_dx_trap_{0}.txt").format(d), "a") as f:
        f.write("Mean result")
        f.write("".join('%a' % (sum_rslt/10)))
        f.write("Mean result")
        f.write("".join('%a' % (sum_eval/10)))
    print(d)
    d = d*2
print("Mean eval", mean_eval_dx)
print("\n Mean Bound", mean_bound_dx)
y_vis2 = mean_eval_dx
plt.plot(x_vis, y_vis2)
plt.plot(x_vis, y_vis1)
plt.show()
plt.clf()


