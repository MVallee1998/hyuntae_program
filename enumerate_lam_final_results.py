import SimplicialComplex as sc
import json
import timeit
m = 10
n = 6

raw_results_path = 'raw_results/PLS_%d_%d' % (m, n)
final_results_path = 'final_results/PLS_%d_%d' % (m, n)

def read_file(filename):
    with open(filename, 'rb') as f:
        data = f.readlines()
    data = [x.strip() for x in data]
    return data


def text(result,path):
    t = open(path, mode='a', encoding='utf-8')
    for K in result:
        t.write(str(K) + '\n')
    t.close()


results = [json.loads(facets_bytes) for facets_bytes in read_file(raw_results_path)]
list_of_seeds = []
counter = 0
start_sub = timeit.default_timer()
start = timeit.default_timer()
for i in range(len(results)):
    counter+=1
    if counter % 1000 == 0:
        stop_sub = timeit.default_timer()
        print("time spent for 1000:", stop_sub - start_sub, " Percentage processed: ", counter / len(results) * 100, "%")
        start_sub = timeit.default_timer()
    facets = results[i]
    K = sc.PureSimplicialComplex(facets)
    if K.Pic == 4 and K.is_a_seed() and K not in list_of_seeds:
        list_of_seeds.append(facets)
    del K
stop = timeit.default_timer()
print("Seeds selected.", " Time spent:", stop - start)

list_of_good_seeds = []
counter = 0
start = timeit.default_timer()
start_sub = timeit.default_timer()
for i in range(len(list_of_seeds)):
    counter+=1
    if counter % 100 == 0:
        stop_sub = timeit.default_timer()
        print("time spent for 100:", stop_sub - start_sub, " Percentage processed: ", counter / len(list_of_seeds) * 100, "%")
        start_sub = timeit.default_timer()
    facets = list_of_seeds[i]
    K = sc.PureSimplicialComplex(facets)
    if K.Pic == 4 and K.is_promising() and K.is_Z2_homology_sphere() and K.is_closed():
        list_of_good_seeds.append(facets)
    del K
stop = timeit.default_timer()
print("Good seeds selected", " Time spent:", stop - start)

list_final = []
counter = 0
counter_PLS = 0
dictionary_ref = dict()
start = timeit.default_timer()
start_sub = timeit.default_timer()
for i in range(len(list_of_good_seeds)):
    counter+=1
    if counter % 100 == 0:
        stop_sub = timeit.default_timer()
        print("time spent for 100:", stop_sub - start_sub, " Percentage processed: ", counter / len(list_of_good_seeds) * 100, "%")
        start_sub = timeit.default_timer()
    facets = list_of_good_seeds[i]
    K = sc.PureSimplicialComplex(facets)
    K_mini_facets = K.find_minimal_lexico_order(dictionary_ref)
    if dictionary_ref[json.dumps(K_mini_facets)] == True:
        if K_mini_facets <= facets and K_mini_facets not in list_final:
            counter_PLS += 1
            print(K_mini_facets, counter_PLS)
            list_final.append(K_mini_facets)
    del K
stop = timeit.default_timer()
text(list_final,final_results_path)
print("Final result saved.", " Time spent:", stop - start)

