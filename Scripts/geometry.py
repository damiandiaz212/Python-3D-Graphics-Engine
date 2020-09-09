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
        self.color = (0, 0, 0)
        self.midpoint = 0

    def to_string(self):
        print(
            '[(' + str(self.vects[0].x) + ', ' + str(self.vects[0].y) + ', ' + str(self.vects[0].z) + '), ' +
            '(' + str(self.vects[1].x) + ', ' + str(self.vects[1].y) + ', ' + str(self.vects[1].z) + '), ' +
            '(' + str(self.vects[2].x) + ', ' + str(self.vects[2].y) + ', ' + str(self.vects[2].z) + ')]'
            )
        
        

class Mesh:

    def __init__(self):
        # mesh stores an array of triangles
        self.tris = []


# create_mesh transforms raw coordinates into mesh objects
def create_cube(coordinates):

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
 
def load_from_obj(path):

        mesh = Mesh()

        file = open(path, 'r')
        lines = file.readlines()

        vectors = []
        obj_tris = []

        for i in lines:
            
            l = i.replace('\n', '')
            l = l.split(' ')
            
            if l[0] == 'v':
                vectors.append(Vector(float(l[1]), float(l[2]), float(l[3])))

            elif l[0] == 'f':
                tri = Triangle()
                tri.vects = [vectors[int(l[1]) - 1], vectors[int(l[2]) - 1], vectors[int(l[3]) - 1]]
                obj_tris.append(tri)
            

        mesh.tris = obj_tris
        return mesh