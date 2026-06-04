from itertools import combinations
import numpy as np
from scipy.spatial.distance import cdist

# S - simplex, SC - simplicial complex, C - specific complexes
TESTING_S = False
TESTING_SC = False
TESTING_C = True


class Simplex:
    """
    Represents a simplex as a finite set of vertices.

    Vertices are stored as a sorted tuple of unique labels to ensure a canonical form
    for equality and hashing. The simplex dimension is defined as (number of vertices - 1).

    Provides functionality to compute all non-empty faces of the simplex and to check
    set-based equality and membership relationships between simplices.

    Method __contains__ is slow in big datasets.
    """
    def __init__(self, vertices):
        vertices_copy = list(vertices).copy()
        self.vertices = tuple(sorted(set(vertices_copy)))

    def dim(self):
        return len(self.vertices) - 1

    def faces(self):
        v = self.vertices
        return [Simplex(combo) for r in range(1, len(v) + 1) for combo in combinations(v, r)]
    
    def __eq__(self, other):
        return self.vertices == other.vertices
    
    def __hash__(self):
        return hash(self.vertices)
    
    def __contains__(self, other):
        return other in self.faces()
    
    def __repr__(self):
        return f"{self.vertices}"


class SimplicialComplex:
    """
    Represents a simplicial complex as a collection of simplices closed under taking faces.

    Internally stores all simplices in a set and enforces the closure property by automatically
    adding all faces of any inserted simplex. Optionally maintains a dimension-indexed dictionary
    for efficient access to simplices by dimension.

    Provides utility methods to add simplices, compute the overall dimension, extract k-skeletons,
    and verify the closure condition (validity) of the complex.
    """
    def __init__(self):
        self.simplices = set()
        self.by_dim = dict()

    def add_simplex(self, simplex):
        faces = simplex.faces()
        self.simplices.update(faces)
        for face in faces:
            key = face.dim()
            if key not in self.by_dim:
                self.by_dim[key] = set()
            self.by_dim[key].add(face)
                

    def add_simplices(self, list_of_simplices):
        for simplex in list_of_simplices:
            self.add_simplex(simplex)

    def dim(self):
        return max(self.by_dim.keys()) if self.by_dim else 0
    
    def is_valid(self):
        for simplex in self.simplices:
            faces = simplex.faces()
            for face in faces:
                if face not in self.simplices:
                    return False
        return True
    
    def skeleton(self, k):
        skeleton_set = set()
        for i in range(k+1):
            skeleton_set.update(self.by_dim[i])
        return skeleton_set
    
    def __repr__(self):
        return f"{self.simplices}"
    
    def rips_complex(self, points, eps):
        """ Uses Euclidean norm """
        distance_matrix = cdist(points, points, metric='euclidean')
        adjacency_matrix = (distance_matrix <= eps).astype(int)
        np.fill_diagonal(adjacency_matrix, 0)
        n = len(points)

        edges = []
        for i, j in combinations(range(n), 2):
            if adjacency_matrix[i, j]:
                edges.append(Simplex((i, j)))
        triangles = []
        for i, j, k in combinations(range(n), 3):
            if adjacency_matrix[i, j] and adjacency_matrix[i, k] and adjacency_matrix[j, k]:
                triangles.append(Simplex((i, j, k)))
        tetras = []
        for i, j, k, l in combinations(range(n), 4):
            if (adjacency_matrix[i, j] and adjacency_matrix[i, k] and adjacency_matrix[i, l] and
                adjacency_matrix[j, k] and adjacency_matrix[j, l] and adjacency_matrix[k, l]):
                tetras.append(Simplex((i, j, k, l)))

        self.add_simplices(edges + triangles + tetras)
        return self
    
    def nerve_complex(self, sets):
        n = len(sets)

        edges = []
        for i, j in combinations(range(n), 2):
            if sets[i] & sets[j]:
                edges.append(Simplex((i, j)))
        triangles = []
        for i, j, k in combinations(range(n), 3):
            if sets[i] & sets[j] & sets[k]:
                triangles.append(Simplex((i, j, k)))
        tetras = []
        for i, j, k, l in combinations(range(n), 4):
            if sets[i] & sets[j] & sets[k] & sets[l]:
                tetras.append(Simplex((i, j, k, l)))

        self.add_simplices(edges + triangles + tetras)
        return self
        

if __name__ == "__main__":
    if TESTING_S:
        my_list = [0,1,2]
        my_other_list = [0,0,1,2,3]
        my_simplex = Simplex(my_list)
        my_other_simplex = Simplex(my_other_list)
        print(my_simplex.vertices)
        print(my_simplex.dim())
        print(my_simplex.faces())
        print(my_simplex == my_other_simplex)
        print(hash(my_simplex))
        print(my_simplex in my_other_simplex)


    if TESTING_SC:
        my_sc = SimplicialComplex()
        my_list = [0,1,2,3]
        my_simplex = Simplex(my_list)
        my_list_2 = [0,1]
        my_simplex_2 = Simplex(my_list_2)
        simplex_list = [my_simplex, my_simplex_2]
        my_sc.add_simplices(simplex_list)
        print(my_sc.dim())
        print(my_sc.is_valid())
        print(my_sc.skeleton(1))


    if TESTING_C:
        complex = SimplicialComplex()
        rips = complex.rips_complex([(0,0), (1,0), (0,1), (1,1)], 2)
        print(rips.by_dim)
        print(rips.is_valid())
        complex = SimplicialComplex()
        nerve = complex.nerve_complex([{0,1}, {1,2}, {2,3}, {3,0}])
        print(nerve.by_dim)
        print(nerve.is_valid())





        

