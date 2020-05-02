import numpy as np
import random
import math
import matplotlib.pyplot as plt

W = 0.7298
c1 = 1.49618
c2 = 1.49618

generation = 50
n_particles = 128
d = 2
mssv = 17520556
def fitness_function(position):
    return position[0]**2 + position[1]**2 + 1

class Particle():
    def __init__(self):
        self.particle_num = 10
        self.position = np.array([])
        for _ in range(self.particle_num):
            self.position = np.append(self.position,((-1) ** (bool(random.getrandbits(1))) * random.random()))
        #print("position", self.position)
        self.pbest_position = self.position
        self.neighbour = [self.pbest_position, self.pbest_position]
        self.pbest_value = float("inf")
        self.velocity = np.array([])
        for _ in range(self.particle_num):
            self.velocity = np.append(self.velocity, 0)
    
    def _str_(self):
        print("I am at ", self.position, "meu pbest is ", self.pbest_position)

    def set_particle_size(self, d):
        self.particle_num = d
    
    def move(self):
        self.position = self.position + self.velocity

    #use for ring topology
    #get the best position in 3 neighbour
    def neighbour_best(self):
        
        if max(self.neighbour_best) > self.pbest_position:
            return max(self.neighbour_best)
        else:
            return self.pbest_position


class Space():

    def __init__(self, target, fitness_func, n_particles, domain):
       self.target = target
       self.fitness = fitness_func
       self.n_particles = n_particles
       self.particles = []
       self.gbest_value = float("inf")
       self.gbest_position = np.array([random.random()*50, random.random()])
       self.gbest_position10 = np.array([])
       for _ in range(self.n_particles):
            self.gbest_position10 = np.append(self.gbest_position10, random.random()*50)
       self.search_domain = domain
       self.optimal = 0

    def print_particles(self):
        for particle in self.particles:
            particle._str_()

    def rastrigin(self, particle):
        for _ in range(self.n_particles):
            sum = (particle.position[0]**2 + particle.position[1]**2) - 10*math.cos(2*math.pi*particle.position[0])*math.cos(2*math.pi*particle.position[1])
        return 10*self.n_particles + sum
        #return particle.position[0] ** 2 + particle.position[1] ** 2 + 1
    
    def rastrigin_10(self, particle):
        sum = 0
        for _ in range(self.n_particles):
            sum1 = math.cos(2*math.pi*particle.position[0])
            for j in range(particle.particle_num - 1):
                sum += particle.position[j+1]**2
                sum1 = sum1* math.cos(2* math.pi*particle.position[j+1])
            sum1 = 10*sum1
            return 10*self.n_particles + (sum - sum1)
    def beale(self, particle):
        return (1.5 - particle.position[0] + particle.position[0]*particle.position[1])**2 + (2.25 - particle.position[0] + particle.position[0]*(particle.position[1]**2))**2 + (2.625 - particle.position[0] + particle.position[0]*(particle.position[1]**3))**2
    
    def himelblau (self, particle):
        return ((particle.position[0])**2+particle.position[1] - 11)**2 + (particle.position[0] + (particle.position[1])**2 -7)**2
    
    def cross_in_tray(self, particle):
        exp = math.exp(100 - math.sqrt(((particle.position[0])**2)+(particle.position[0])**2)/math.pi)
        sum = abs(math.sin(particle.position[0])*math.sin(particle.position[1])*exp + 1)
        return -0.0001 * math.pow(sum, 0.1)
        
    def set_pbest(self):
        for particle in self.particles:
            if self.fitness == "rastrigin":
                fitness_candidate = self.rastrigin(particle)
            if self.fitness == "beale":
                fitness_candidate = self.beale(particle)
            if self.fitness == "himelblau":
                fitness_candidate = self.himelblau(particle)
            if self.fitness == "cit":
                fitness_candidate = self.cross_in_tray(particle)
            if (particle.pbest_value > fitness_candidate):
                particle.pbest_value = fitness_candidate
                particle.pbest_position = particle.position

    def set_gbest(self):
        for particle in self.particles:
            if self.fitness == "rastrigin":
                best_fitness_candidate = self.rastrigin(particle)
            if self.fitness == "beale":
                best_fitness_candidate = self.beale(particle)
            if self.fitness == "himelblau":
                best_fitness_candidate = self.himelblau(particle)
            if self.fitness == "cit":
                best_fitness_candidate = self.cross_in_tray(particle)
            if (self.gbest_value > best_fitness_candidate):
                self.gbest_value = best_fitness_candidate
                self.gbest_position = particle.position

    def set_ringbest(self, j):
        i = j
        for particle in self.particles:
            best_fitness = self.rastrigin_10(particle)
            if (self.gbest_value > best_fitness):
                self.gbest_value = best_fitness
                self.gbest_position = particle.position
            i = i + 1
            if (i >= j+3): return i


    def move_particles(self):
        for particle in self.particles:
            global W
            r1 = random.random()
            r2 = random.random()
            new_velocity = (W*particle.velocity) + (c1*r1) * (particle.pbest_position - particle.position) + (r2*c2) * (self.gbest_position - particle.position)
            particle.velocity = new_velocity
            particle.move()

def star_topology(fitness_func, mssv):
    random.seed(mssv)
    topology = "star"
    d = n_particles
    if fitness_func == "rastrigin":
        search_domain = [-5.12, 5.12]
    if fitness_func == "beale":
        search_domain = [-4.5, 4.5]
    if fitness_func == "himelblau":
        search_domain = [-5., 5.]
    if fitness_func == "cit":
        search_domain = [-10., 10.]
    search_space = Space(1, fitness_func, generation,search_domain)
    particles_vector = [Particle() for _ in range(search_space.n_particles)]
    search_space.particles = particles_vector
    search_space.print_particles()
    x_vis = np.array(search_space.gbest_position[0])
    y_vis = np.array(search_space.gbest_position[1])
    iteration = 0
    while (iteration < generation):
        search_space.set_pbest()
        search_space.set_gbest()

        if(search_space.gbest_value == search_space.optimal):
            break
        #print("Hello")
        search_space.move_particles()
        iteration += 1
        x_vis = np.array(search_space.gbest_position[0])
        y_vis = np.array(search_space.gbest_position[1])
        xmin,ymin = search_space.search_domain[0], search_space.search_domain[0]
        xmax, ymax = search_space.search_domain[1], search_space.search_domain[1]
        plt.axis([xmin,xmax, ymin, ymax])
        particles_vector1 = search_space.particles
        for particle in particles_vector1:
        
            x_vis = np.append(x_vis, particle.position[0])
            y_vis = np.append(y_vis, particle.position[1])
            #h_vis = np.append(h_vis, particle.pbest_position)
        plt.plot(x_vis, y_vis,'ro')
        plt.title("Generation " +  str(iteration))
        plt.pause(0.5)
        plt.clf()
        #print("iter", iteration)
    with open(("{0}_{1}_{2}.txt").format(mssv, topology, d), "w") as f:
        f.write("The best solution is: \n")
        f.write("".join('%a' % search_space.gbest_position))
        f.write('\n Differences between best position and global minimum \n')
        f.write("".join('%d' % abs(search_space.gbest_value - search_space.optimal)))
    print("The best solution is: ", search_space.gbest_position, "in generation: ", iteration)
    print("Best fitness value", abs(search_space.gbest_value - search_space.optimal))

def ring_topology(fitness_func, mssv):
    random.seed(mssv)
    topology = "ring"
    
    if fitness_func == "rastrigin":
        search_domain = [-5.12, 5.12]
    if fitness_func == "beale":
        search_domain = [-4.5, 4.5]
    if fitness_func == "himelblau":
        search_domain = [-5., 5.]
    if fitness_func == "cit":
        search_domain = [-10., 10.]
    search_space = Space(1, fitness_func, n_particles, search_domain)
    particles_vector = [Particle() for _ in range(search_space.n_particles)]
    search_space.particles = particles_vector
    search_space.print_particles()
    d = n_particles
    x_vis = np.array(search_space.gbest_position[0])
    y_vis = np.array(search_space.gbest_position[1])
    ####################################################
    iteration = 0
    j = 0
    while (iteration < generation):
        search_space.set_pbest()    
        j = search_space.set_ringbest(j)
        if(search_space.gbest_value == search_space.optimal):
            break
        if (j >= search_space.n_particles - 2):
            search_space.move_particles()
            j = 0
        else:
            j = search_space.set_ringbest(j) 
        iteration += 1
        x_vis = np.array(search_space.gbest_position[0])
        y_vis = np.array(search_space.gbest_position[1])
        xmin,ymin = search_space.search_domain[0], search_space.search_domain[0]
        xmax, ymax = search_space.search_domain[1], search_space.search_domain[1]
        plt.axis([xmin,xmax, ymin, ymax])
        particles_vector1 = search_space.particles
        for particle in particles_vector1:
        
            x_vis = np.append(x_vis, particle.position[0])
            y_vis = np.append(y_vis, particle.position[1])
            #h_vis = np.append(h_vis, particle.pbest_position)
        plt.plot(x_vis, y_vis,'ro')
        plt.title("Generation " +  str(iteration))
        plt.pause(0.5)
        plt.clf()
    with open(("{0}_{1}_{2}.txt").format(mssv, topology, d), "w") as f:
        
        f.write("The best solution is: \n")
        f.write("".join('%a' % search_space.gbest_position))
        f.write('\n Differences between best position and global minimum \n')
        f.write("".join('%d' % abs(search_space.gbest_value - search_space.optimal)))
    print("The best solution is: ", search_space.gbest_position, "in n_iteration: ", iteration)
    print("Best fitness value", abs(search_space.gbest_value - search_space.optimal))       

#star_topology("rastrigin")
#star_topology("beale")
#star_topology("rastrigin")
for i in range(10): 
    star_topology("rastrigin", mssv)
    ring_topology("rastrigin", mssv)
    
    mssv += 1