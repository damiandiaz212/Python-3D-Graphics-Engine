"""

geometry.py
author: Damian Diaz

Defines our fundemental geometry objects. 

"""

class Vector:
    
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def to_string(self) -> str:
        print('(' + str(self.x) + ', ' + str(self.y) + ', ' + str(self.z) + ')')


class Triangle:
   
    def __init__(self):
        # triangle store 3 vectors
        self.vects = [Vector(0.0, 0.0, 0.0), Vector(0.0, 0.0, 0.0), Vector(0.0, 0.0, 0.0)]
        
        

class Mesh:

    def __init__(self):
        # mesh stores an array of triangles
        self.tris = []

    def load_from_obj(self, file):

        return True


# create_mesh transforms raw coordinates into mesh objects
def create_mesh(coordinates):

    tris = []
    
    for tri in coordinates:
        vectors = []
        c = 0
        while c < 9:
            t = []
            for i in range(3):
                t.append(tri[c])
                c+=1
            v = Vector(t[0], t[1], t[2])
            vectors.append(v)
        
        new_tri = Triangle()
        new_tri.vects = vectors

        tris.append(new_tri)

    mesh = Mesh()
    mesh.tris = tris

    return mesh

        