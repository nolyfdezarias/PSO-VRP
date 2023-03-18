import os 
import pandas
import json
import matplotlib.pyplot as plt 
optimos = [784,742,937,1177,1764]

def get_rows(files):
    rows = []
    for file in files:
        f = open(file)
        data = json.load(f)
        n_iterations = 30
        if file.__contains__('Iteraciones'):
            n_iterations = int(file.split('Iteraciones')[1].split('.')[0].replace('-',''))

        rows.append([data['filename'],n_iterations,data['numero_de_particulas'],data['valor_minimo'],data['valor medio'],data['tiempo medio']])

    rows.sort()
    return rows

def get_plot_row(file):
       
    f = open(file)
    data = json.load(f)
    _min = data['valor_minimo']
    _best = data['todos_best']
    _x = [x for x in _best if x[len(x)-1] == _min][0]
    #print(len(_x))
    #input()
    return _x

def _plot(files,names,_min,name,_len):
    rows = []
    for file in files:
        _row = get_plot_row(file)
        if len(_row) != _len:
            _row += [_row[len(_row)-1]] * (_len - len(_row) + 1)
        rows.append(_row)    
    
    _min_row = [_min] * _len

    plt.clf()
    plt.plot(_min_row,'r--',rows[0],'y',rows[1],'b',rows[2],'g')
    plt.legend(names, loc ="upper right")
    plt.title(name)
    plt.xlabel("Número de Iteraciones")
    plt.ylabel("Valor de evaluación")
    plt.savefig(name)


files = [ f for f in os.listdir( os.curdir ) if os.path.isfile(f) ]
files = [ f for f in files if f.__contains__('.txt')]


versions = ['V1','V2.1','V0']

files_v0 = [f for f in files if f.__contains__(versions[2]) ]
files_v1 = [f for f in files if f.__contains__(versions[0])]
files_v2 = [f for f in files if f.__contains__(versions[1])]

rows = get_rows(files_v0)
df = pandas.DataFrame(rows, columns =['FName', 'NIteraciones', 'NParticulas','ValorMin','ValorMed','TiempoMed'], dtype = float)
df.to_csv(f'Output-V0.csv')

rows1 = get_rows(files_v1)
df = pandas.DataFrame(rows1, columns =['FName', 'NIteraciones', 'NParticulas','ValorMin','ValorMed','TiempoMed'], dtype = float)
df.to_csv(f'Output-V1.csv')

rows2 = get_rows(files_v2)
df = pandas.DataFrame(rows2, columns =['FName', 'NIteraciones', 'NParticulas','ValorMin','ValorMed','TiempoMed'], dtype = float)
df.to_csv(f'Output-V2.csv')


files0 = (['V0-A-n32-k5-SolInfo-100-Iteraciones-30.txt','V0-A-n32-k5-SolInfo-1000-Iteraciones-30.txt','V0-A-n32-k5-SolInfo-100000-Iteraciones-30.txt'],['min','P100','P1000','P100000'],"Mayor cantidad de particulas V0 , 32 C",784,30)
files_01 = (['V0-A-n32-k5-SolInfo-10-Iteraciones-30.txt','V0-A-n32-k5-SolInfo-10-Iteraciones-100.txt','V0-A-n32-k5-SolInfo-10-Iteraciones-1000.txt'],['min','P10-30Iter','P10-100Iter','P10-1000Iter'],"Mayor cantidad de iteraciones V0",784,1000)
files1 = (['V1-A-n65-k9-SolInfo-100-Iteraciones-30.txt','V0-A-n65-k9-SolInfo-100-Iteraciones-100.txt','V0-A-n65-k9-SolInfo-100-Iteraciones-1000.txt'],['min','P100-30Iter','P100-100Iter','P100-1000Iter'],"Mayor cantidad de iteraciones V1 ,65 C",1177,1000)
files2 = (['V0-A-n32-k5-SolInfo-1000-Iteraciones-1000.txt','V1-A-n32-k5-SolInfo-1000-Iteraciones-1000.txt','V2.1-A-n32-k5-SolInfo-1000-Iteraciones-1000.txt'],['min','V1','V2','V3'],"Comparando entre versiones 1 (1000P-1000I) , 32 C",784,1000)
files3 = (['V0-A-n44-k6-SolInfo-1000-Iteraciones-1000.txt','V1-A-n44-k6-SolInfo-1000-Iteraciones-1000.txt','V2.1-A-n44-k6-SolInfo-1000-Iteraciones-1000.txt'],['min','V1','V2','V3'],"Comparando entre versiones 2 (1000P-1000I) , 44 C ", 937,1000)
files4 = (['V0-A-n80-k10-SolInfo-1000-Iteraciones-1000.txt','V1-A-n80-k10-SolInfo-1000-Iteraciones-1000.txt','V2.1-A-n80-k10-SolInfo-1000-Iteraciones-1000.txt'],['min','V1','V2','V3'],"Comparando entre versiones 3 (1000P-1000I) , 80 C",1764,1000)

files_list = [files0,files_01,files1,files2,files3,files4]
for files,names,title,_min,_len in files_list:
    _plot(files,names,_min,title,_len)

