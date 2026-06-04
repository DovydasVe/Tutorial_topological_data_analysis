from itertools import combinations

TESTING_S = True
TESTING_SC = True

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
        return f"{self.vertices}"


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


        

