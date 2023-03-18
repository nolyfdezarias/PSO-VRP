from more_itertools import random_permutation
import numpy as np
import random
import math
import time
import json

random.seed(3000)


#--------------------------------------[Reading data set values through function]------------------------------------------------------------------------
def readdata(name_of_file):
    a1=open(name_of_file,'r')
    #reading content of a1 and storing in a2
    a2=a1.read()
    #splitting contents in a2 into list from where newline is started
    a2=a2.split('\n')
    #For reading number of customers, splitting values in third index of a2 list into new list
    temp_customer=a2[3].split()
    #converting a list value to integer which gives total customers 
    no_of_customers=int(temp_customer[2])
    #reading vehicle capacity which is in five index of list b2
    temp_capacity=a2[5].split()
    vehicle_total_capacity=int(temp_capacity[2])

    a1.close()
    length = no_of_customers
    #initializing array matrices of demand of customers, X coordinate , Y coordinate using compact for loop
    x=[0 for j in range(no_of_customers)]
    y=[0 for j in range(no_of_customers)]
    customer_demand = [0 for j in range(length)]
    #-----------reading values of x,y nodes of customers as well as their demand by splitting into lists from the respective indices of their start-----
    for j in range(0, length):
        x_y_values = a2[j+7].split()
        customer_demand[j] = int(float( a2[no_of_customers + 8 + j].split()[1] ))
        x[j] = int(float(x_y_values[1]))
        y[j] = int(float(x_y_values[2]))

    #------------------------------[calculating distance between nodes and computing the distance matrix]--------------------------------------------
        
    #initializing 2-d distance matrix that computes distance between customers and customer & depot
    matrix_distance=[[0 for i in range(no_of_customers)] for j in range(no_of_customers)]
    for i in range(no_of_customers):
        for j in range(no_of_customers):
            if i==j:
                matrix_distance[i][j]=0
            elif i>j:     #since this matrix is symmetrical
                matrix_distance[i][j]=matrix_distance[j][i]
            else:
                matrix_distance[i][j]=math.sqrt((x[j]-x[i])**2+(y[j]-y[i])**2)

    return vehicle_total_capacity, no_of_customers-1, matrix_distance,customer_demand, x, y

def mutate_particle(particle):
    _toChange = []
    while len(_toChange) < len(particle)/4:
        _rnd = random.randrange(0,len(particle))
        if _rnd not in _toChange:
            _toChange.append(_rnd)
    if len(_toChange) % 2 != 0:
        _toChange = _toChange[:-1]
    
    i = 0
    while i < len(_toChange):
        aux = particle[i]
        particle[i] = particle[i+1]
        particle[i+1] = aux
        i += 2

    return list(particle)

def eval_sol(trucks,distance_matrix):
    vals = []
    _val = 0
    for i in range(len(trucks)):
        _x = 0
        for j in range(len(trucks[i])):
            if j == 0:
                _val += distance_matrix[0][trucks[i][j]-1]
                _x += distance_matrix[0][trucks[i][j]-1]
            else:
               _val += distance_matrix[trucks[i][j-1]-1][trucks[i][j]-1]
               _x += distance_matrix[trucks[i][j-1]-1][trucks[i][j]-1]
               if j == len(trucks[i]) - 1:
                    _val += distance_matrix[trucks[i][j]-1][0]
                    _x += distance_matrix[trucks[i][j]-1][0]
               #print(f'{trucks[i][j-1]} -> {trucks[i][j]}')
        vals.append(_x)    
    #print(vals)
    #print(sum(vals))    
    return _val

def get_velocity(particle,pb_particle,v_particles,gb_particles):
    #W is inertia constant
    W = 1.2
    #C1 is cognitive acceleration constant
    C1 = 2.05
    #C2 is social acceleration constant
    C2 = 2.05
    _velocity = 0
    #_v_particle = []
    for i in range(len(particle)):
        #_velocity = W*v_particles[i] + (C1*random.random()) * (pb_particle[i] - particle[i]) + (C2*random.random()) * (gb_particles[i]- particle[i])
        _velocity += W*v_particles + (C1*random.random()) * (pb_particle[i] - particle[i]) + (C2*random.random()) * (gb_particles[i]- particle[i])
    _velocity = _velocity if _velocity > 0 and _velocity < 30 else 30 if _velocity > 30 else 0
        #_v_particle.append(_velocity)
    
    #_velocity = W*v_particles + (C1*random.random()) * (pb_particle - particle) + (C2*random.random()) * (gb_particles- particle)
    #_velocity = _velocity if _velocity > 0 and _velocity < 30 else 30 if _velocity > 30 else 0
    
    return _velocity#_v_particle

def get_velocit1(particle,pb_particle,v_particles,gb_particles):
    #W is inertia constant
    W = 1.2
    #C1 is cognitive acceleration constant
    C1 = 2.05
    #C2 is social acceleration constant
    C2 = 2.05
    _velocity = 0
    #_v_particle = []
    for i in range(len(particle)):
        #_velocity = W*v_particles[i] + (C1*random.random()) * (pb_particle[i] - particle[i]) + (C2*random.random()) * (gb_particles[i]- particle[i])
        _velocity += W*v_particles + (C1*random.random()) * (pb_particle[i] - particle[i]) + (C2*random.random()) * (gb_particles[i]- particle[i])
    #_velocity = _velocity if _velocity > 0 and _velocity < 30 else 30 if _velocity > 30 else 0
        #_v_particle.append(_velocity)
    _velocity %= 30
    #_velocity = W*v_particles + (C1*random.random()) * (pb_particle - particle) + (C2*random.random()) * (gb_particles- particle)
    #_velocity = _velocity if _velocity > 0 and _velocity < 30 else 30 if _velocity > 30 else 0
    
    return _velocity#_v_particle


def move_particle(particle,v_particle,target,alt_target = None):
    _newParticle = []
    #k = 0
    #for i in range(len(particle)):
    #    if particle[i] == target[i]:
    #        #toAnother = False
    #        k += 1
    #        break

    #toAnother =  False if k == len(particle) else True 
    toAnother = True
    if toAnother:
        for i in range(len(particle)):
            #_val = particle[i]
            if particle[i] != target[i]:
                #print("intente")
                if v_particle > 20:
                    if random.random() > 0.5:
                        _pos = particle.index(target[i])
                        _aux = particle[i]
                        particle[i] = target[i]
                        particle[_pos] = _aux
                else:
                    toAnother = True
                    break
            
    #if toAnother and alt_target != None and random.random() > 0.5:
    #    for i in range(len(particle)):
    #        if particle[i] != alt_target[i]:
    #            if random.random() > 0.5:
    #                _pos = particle.index(alt_target[i])
    #                _aux = particle[i]
    #                particle[i] = alt_target[i]
    #                particle[_pos] = _aux

                   
    return list(particle)


def move_particle1(particle,v_particle,target,alt_target = None):
    _newParticle = []
    k = 0
    #for i in range(len(particle)):
    #    if particle[i] == target[i]:
    #        #toAnother = False
    #        k += 1
    #        break

    toAnother =  False if k == len(particle) else True 
    #toAnother = True
    if not toAnother:
        for i in range(len(particle)):
            #_val = particle[i]
            if particle[i] != target[i]:
                #print("intente")
                if v_particle > 20:
                    if random.random() > 0.5:
                        _pos = particle.index(target[i])
                        _aux = particle[i]
                        particle[i] = target[i]
                        particle[_pos] = _aux
                else:
                    toAnother = True
                    break
            
    if toAnother and alt_target != None and random.random() > 0.5:
        #print('Tengo posibilidad de moverme')
        for i in range(len(particle)):
            if particle[i] != alt_target[i]:
                if random.random() > 0.5:
                    _pos = particle.index(alt_target[i])
                    _aux = particle[i]
                    particle[i] = alt_target[i]
                    particle[_pos] = _aux

                   
    return list(particle)

def move_particle2(particle,v_particle,target,alt_target = None):
    _newParticle = []
    k = 0
    for i in range(len(particle)):
        if particle[i] == target[i]:
            #toAnother = False
            k += 1
            break

    toAnother =  False if k == len(particle) else True 
    #toAnother = True
    if not toAnother:
        for i in range(len(particle)):
            #_val = particle[i]
            if particle[i] != target[i]:
                #print("intente")
                if v_particle > 20:
                    if random.random() > 0.5:
                        _pos = particle.index(target[i])
                        _aux = particle[i]
                        particle[i] = target[i]
                        particle[_pos] = _aux
                else:
                    toAnother = True
                    break
            
    if toAnother and alt_target != None and random.random() > 0.5:
        #print('Tengo posibilidad de moverme')
        for i in range(len(particle)):
            if particle[i] != alt_target[i]:
                if random.random() > 0.5:
                    _pos = particle.index(alt_target[i])
                    _aux = particle[i]
                    particle[i] = alt_target[i]
                    particle[_pos] = _aux

                   
    return list(particle)



def get_sol(particle,demand,vehicle_capacity,n_vehicles = 5):
    trucks = []
    _capacity = 0
    _clients = []
    #print(n_vehicles)
    for i in range(len(particle)):
        #if len(trucks) >= n_vehicles:
        #    return trucks 
        if _capacity + demand[particle[i]-1] <= vehicle_capacity:
            _capacity += demand[particle[i]-1]
        #if _capacity + demand[particle[i]] <= vehicle_capacity:
        #    _capacity += demand[particle[i]]
            _clients.append(particle[i])
        else:
            trucks.append(list(_clients))
            _clients = [particle[i]]
            _capacity = demand[particle[i]-1]
            
            #_capacity = demand[particle[i]]
            #if len(trucks) == n_vehicles:
            #    return trucks 

    if len(_clients)>0:
        trucks.append(list(_clients))

    return trucks

def init_particles(n_particles,n_clients):
    _particles = []
    _v_particles = []
    #clusters = {}
    #clusters_mins = {}
    #clusters_mins[0] = (2000000000,None)
    #clusters_mins[1] = (2000000000,None)
    #clusters_mins[2] = (2000000000,None)
    #clusters_mins[3] = (2000000000,None)
    #clusters_mins[4] = (2000000000,None)

    #_vparticles = []
    for _ in range(0,n_particles):
        #_particles.append(random_permutation([x for x in range(1,n_clients+1)]))
        _particles.append(random_permutation([x for x in range(2,n_clients+2)]))
        #clusters[_particles[len(_particles)-1]] = random.randrange(0,5)
    
    for _ in range(n_particles):
        #for _ in range(n_particles):
        _v_particles.append(random.random()*random.randrange(0,30))
        #_vparticles.append(list(_v_particles))
        #_v_particles = []
    
    return _particles , _particles , _v_particles

def run_pso(clients_demands,distance_matrix,n_vehicles,
                n_particles = 100000,
                n_clients = 32,
                vehicle_capacity = 100, 
                n_exp = 30,
                n_iterations = 30):

    min_val = 2000000000
    min_val_particle = []
    _avgSol = 0
    _avgTime = 0
    _dic = {}
    ctest = 0
    coptimo = 0
    all_gb_best_vals = []
    m_15 = 0
    m_20 = 0
    m_c = 0
    for x in range(n_exp):
        all_gb_best_vals.append([])
        gb_particles = [] #[2,3,1,4,5]
        gb_particles_eval = 2000000000
        pb_particles_eval = [2000000000]* n_particles
        particles, pb_particles ,v_particles  = init_particles(n_particles,n_clients)
        #same_sol = X
        init_time = time.time()
        for i in range(n_iterations):
            #print(particles)
            
            for j in range(len(particles)):
                trucks = list(get_sol(particles[j],clients_demands,vehicle_capacity,n_vehicles))
                _val = eval_sol(trucks,distance_matrix)

                #n_cluster = cluster[particles[j]]
                #cluster_min_val,_ = clusters_mins[n_cluster]

                #print(f'val particle {j} en la iteracion {i} : {_val}')
                if _val < gb_particles_eval:
                    gb_particles_eval = _val
                    pb_particles_eval[j] = _val
                    pb_particles[j] = list(particles[j])
                    gb_particles = list(particles[j])
                    #clusters_mins[n_cluster] = (_val,list(particles[j]))
                
                #elif _val < cluster_min_val:
                #    clusters_mins[n_cluster] = (_val,list(particles[j]))
                #    pb_particles_eval[j] = _val
                #    pb_particles[j] = list(particles[j])
                
                elif _val < pb_particles_eval[j]:
                    pb_particles_eval[j] = _val
                    pb_particles[j] = list(particles[j])

            for j in range(len(particles)):
                rndPermutation = list(random_permutation([x for x in range(2,n_clients+2)]))

                v_particles[j] = get_velocity(particles[j],pb_particles[j],v_particles[j],gb_particles)
                _x1 = get_velocit1(particles[j],pb_particles[j],v_particles[j],gb_particles)
                
                #print(_x1)
                if _x1 < 6 :
                    m_15 += 1
                if  _x1 > 6:
                    m_20 += 1
                m_c += 1
                particles[j] = list(move_particle(particles[j],v_particles[j],gb_particles,rndPermutation))

                #n_cluster = random.randrange(0,5)
                #_,gb_cluster = clusters_mins[n_cluster] 
                #v_particles[j] = get_velocity(particles[j],pb_particles[j],v_particles[j],gb_cluster)
                #particles[j] = list(move_particle(particles[j],v_particles[j],gb_cluster,rndPermutation))

            #print(f'best val de la iteracion {i} Exp {x} : {gb_particles_eval}')
            
            try:
                _dic[gb_particles_eval] += 1
            except:
                _dic[gb_particles_eval] = 1


            if _dic[gb_particles_eval] > 5:
                coptimo += 1
                _toChange = list(gb_particles)
                for i in range(50):
                    _new_particle = mutate_particle(_toChange)#np.random.permutation(gb_particles).tolist()#random_permutation(gb_particles)
                    trucks1= list(get_sol(_new_particle,clients_demands,vehicle_capacity,n_vehicles))
                    _val1 = eval_sol(trucks1,distance_matrix)
                    _toChange = list(_new_particle)
                

                    if _val1 < gb_particles_eval:
                        #print("cambie")
                        ctest += 1
                        gb_particles_eval = _val1
                        gb_particles = list(_new_particle)
                        break
            
            all_gb_best_vals[x].append(gb_particles_eval)
        #print(f'cambie {ctest} veces')
        if gb_particles_eval < min_val:
            min_val = gb_particles_eval
            min_val_particle = list(gb_particles)
        
        end_time = time.time()
        
        _avgTime += end_time - init_time
        _avgSol += gb_particles_eval
    return min_val,min_val_particle , _avgSol/n_exp , _avgTime/n_exp,ctest,coptimo,all_gb_best_vals,m_15,m_20,m_c


def run_test():
    files = [('A-n32-k5.vrp',5,True),('A-n33-k6.vrp',6,True), ('A-n44-k6.vrp',6,True), ('A-n65-k9.vrp',9,True) , ('A-n80-k10.vrp',10,True)]
    #files = [('A-n32-k5.vrp',5,True)]
    
    l_n_particles = [10]#[100000]#[10,100,1000,100000]#[100000]#[10,100,1000]#[10,100,1000]
    l_n_iterations = [30]#[30,100,1000]#[30]# 
    
    #n_particles = 1000#100000
    n_experimentos = 30
    n_iterations = 1000#30
    for n_particles in l_n_particles:
        for n_iterations in l_n_iterations:
            if n_particles == 100000 and n_iterations != 30:
                continue
            for file,n_vehicle,_do in files:
                if _do:
                    capacity_of_vehicle, total_customers, distance_matrix, demand_matrix, _, _ = readdata(file)

                    minval , min_val_particle, avg , avgTime ,ctest, coptimo,all_gb_best_vals, m_15,m_20,m_c = run_pso(demand_matrix,distance_matrix,n_vehicle,
                            n_particles = n_particles,
                            n_clients = total_customers,
                            vehicle_capacity = capacity_of_vehicle, 
                            n_exp = n_experimentos,
                            n_iterations = n_iterations)

                    print("final sol")
                    print(f'filename : {file}')
                    print(f'numero de particulas {n_particles}')
                    print(f'numero de experimentos {n_experimentos}')
                    print(f'valor minimo {minval}')
                    print(f'solucion : {min_val_particle}')
                    print(f'valor medio {avg}')
                    print(f'tiempo medio  {avgTime}')
                    print(f'cambie {ctest} veces')
                    print(f'cai en un optimo local {coptimo} veces')
                    
                    # dictionary = {
                    #     "filename": file,
                    #     "numero_de_particulas": n_particles,
                    #     "numero_de_experimentos": n_experimentos,
                    #     "valor_minimo": minval,
                    #     "solucion" : min_val_particle,
                    #     "valor medio" : avg,
                    #     "tiempo medio" : avgTime,
                    #     "cambios" : ctest,
                    #     "optimos_locales" : coptimo,
                    #     "todos_best" : all_gb_best_vals

                    # }
                    dictionary = {
                        "filename": file,
                        "m_15" : m_15,
                        "m_20" : m_20,
                        "m_c" : m_c
                    }
                    json_object = json.dumps(dictionary, indent=4)
                    with open(f'VX-{file[:-4]}-SolInfo-{n_particles}-Iteraciones-{n_iterations}.txt', "w") as outfile:
                        outfile.write(json_object)
                    
                    print(f'Termine {file[:-4]}-SolInfo-{n_particles}-Iteraciones-{n_iterations}')

#file = 'A-n32-k5.vrp'
#capacity_of_vehicle, total_customers, distance_matrix, demand_matrix, _, _ = readdata(file)
# t = get_sol([26, 31, 28, 32, 25, 29, 3, 1, 21, 16, 10, 4, 5, 11, 2, 8, 20, 7, 19, 12, 18, 13, 22, 15, 14, 6, 23, 27, 9, 24, 17, 30],demand_matrix,100,6)
# print(t)
# print(eval_sol(t,distance_matrix))



run_test()

