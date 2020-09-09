import math


def multiply_matrix_vector(i, o, m):

    o.x = i.x * m[0][0] + i.y * m[1][0] + i.z * m[2][0] + m[3][0]
    o.y = i.x * m[0][1] + i.y * m[1][1] + i.z * m[2][1] + m[3][1]
    o.z = i.x * m[0][2] + i.y * m[1][2] + i.z * m[2][2] + m[3][2]

    w = i.x * m[0][3] + i.y * m[1][3] + i.z * m[2][3] + m[3][3]

    if w != 0.0:
        o.x /= w
        o.y /= w
        o.z /= w


def mat_4x4():
    t = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]
    return t


def normalize(vector3d):

    l = float(math.sqrt(vector3d.x * vector3d.x + vector3d.y * vector3d.y + vector3d.z * vector3d.z))

    if l != 0:
        vector3d.x /= l
        vector3d.y /= l
        vector3d.z /= l
    else:
        vector3d.x = 0 
        vector3d.y = 0
        vector3d.z = 0


# dot product with camera
def dot_product(vector3d, tri_translated, camera):
    return (
            vector3d.x * (tri_translated.vectors[0].x - camera.x) +
            vector3d.y * (tri_translated.vectors[0].y - camera.y) +
            vector3d.z * (tri_translated.vectors[0].z - camera.z)
        )


# add two vectors together
def vector_add(v1, v2):
    return v1.x + v2.x, v1.y + v2.y, v1.z + v2.z


# subtract two vectors together
def vector_sub(v1, v2):
    return v1.x - v2.x, v1.y - v2.y, v1.z - v2.z


# multiply two vectors together
def vector_multiply(v1, k):
    return v1.x * k, v1.y * k, v1.z * k


# add two vectors together
def vector_divide(v1, k):
    return v1.x / k, v1.y / k, v1.z / k


# dot product of two vectors
def vector_dot_product(v1, v2):
    return v1.x * v2.x + v1.y * v2.y + v1.z * v2.z


# vector length of vector
def vector_length(v):
    return math.sqrt(vector_dot_product(v, v))


# normalize vector
def vector_normalize(v):
    l = vector_length(v)
    return v.x / l, v.y / l, v.z / l

