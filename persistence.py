from collections import defaultdict
from itertools import combinations
from scipy.spatial.distance import cdist
from topology import Simplex, SimplicialComplex


# F - filtration class, RF - rips filtration
TESTING_F = False
TESTING_RF = True


class Filtration:
    def __init__(self):
        self.filtration = dict()

    def add(self, simplex, value):
        if simplex in self.filtration:
            if value < self.filtration[simplex]:
                self.filtration[simplex] = value
        else:
            self.filtration[simplex] = value

    def sort(self):
        grouped_dict = defaultdict(list)

        for key, value in self.filtration.items():
            grouped_dict[value].append(key)

        grouped_dict = dict(grouped_dict)
        sorted_grouped_dict = dict(sorted(grouped_dict.items(), key=lambda item: item[0]))

        for key in sorted_grouped_dict.keys():
            sorted_values = sorted(sorted_grouped_dict[key], key=lambda x: x.dim())
            sorted_grouped_dict[key] = sorted_values

        sorted_dict = dict()
        for key, value in sorted_grouped_dict.items():
            for v in value:
                sorted_dict[v] = key
        
        self.filtration = sorted_dict

    def get_complex(self, k):
        simplices_list = list()

        for key, value in self.filtration.items():
            if value <= k:
                simplices_list.append(key)
        
        K = SimplicialComplex()
        K.add_simplices(simplices_list)

        return K

    def filtration_values(self):
        return sorted(list(set(v for v in self.filtration.values())))
    
    def is_valid(self):
        for simplex, value in self.filtration.items():
            faces = simplex.faces()
            for face in faces:
                if face not in self.filtration:
                    return False
                if self.filtration[face] > value:
                    return False
        return True



def rips_filtration(points):
    F = Filtration()
    distance_matrix = cdist(points, points, metric='euclidean')
    n = len(points)

    for i in range(n):
        F.add(Simplex([i]), 0.0)

    for i, j in combinations(range(n), 2):
        F.add(Simplex([i,j]), float(distance_matrix[i, j]))

    for i, j, k in combinations(range(n), 3):
        value = max(distance_matrix[i, j], distance_matrix[i, k], distance_matrix[j, k])
        F.add(Simplex([i,j,k]), float(value))

    return F
    


if __name__ == "__main__":
    if TESTING_F:
        s1 = Simplex([0,1])
        s2 = Simplex([1])
        s3 = Simplex([0])
        F = Filtration()
        F.add(s1, 0.4)
        F.add(s2, 0.3)
        F.add(s3, 0.2)
        print(F.filtration)
        F.sort()
        print(F.filtration)
        K = F.get_complex(0.3)
        print(K)
        print(F.filtration_values())
        print(F.is_valid())

    if TESTING_RF:
        points = [(0,0), (0,1), (1,0), (1,1)]
        rf = rips_filtration(points)
        print(rf.filtration)
        print(rf.is_valid())
    
