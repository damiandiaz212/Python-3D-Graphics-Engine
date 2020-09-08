import math

"""

projection.py
author: Damian Diaz

helper functions for the graphics engine

"""

def multiply_matrix_vector(i, o, m):

    o.x = i.x * m[0][0] + i.y * m[1][0] + i.z * m[2][0] + m[3][0]
    o.y = i.x * m[0][1] + i.y * m[1][1] + i.z * m[2][1] + m[3][1]
    o.z = i.x * m[0][2] + i.y * m[1][2] + i.z * m[2][2] + m[3][2]

    w = i.x * m[0][3] + i.y * m[1][3] + i.z * m[2][3] + m[3][3]

    if w != 0.0:
        o.x /= w
        o.y /= w
        o.z /= w

def mat4x4():
    t = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]
    return t

def normalize(vector3d):
    l = math.sqrt(vector3d.x * vector3d.x + vector3d.y * vector3d.y + vector3d.z * vector3d.z)
    vector3d.x /= l
    vector3d.y /= l
    vector3d.z /= l

def dot_product(vector3d, triTranslated, camera):
    return (
        vector3d.x * (triTranslated.vects[0].x - camera.x) +
        vector3d.y * (triTranslated.vects[0].y - camera.y) +
        vector3d.z * (triTranslated.vects[0].z - camera.z)
        )