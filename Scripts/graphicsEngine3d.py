import math
import pygame
import copy
from Scripts.geometry import Vector, Triangle, Mesh, create_mesh
from Scripts.projection import multiply_matrix_vector, mat4x4
from Lib.meshes import *

"""

graphicsEngine3d.py
author: Damian Diaz

the meat and potatoes

"""


class ge3d:

    def __init__(self, width, height):
        self.screen_width = width
        self.screen_height = height
        self.meshCube = Mesh()
        self.matProj = mat4x4()
        self.fTheta = 0

    def on_user_create(self):

        # create a cube mesh 
        self.meshCube = create_mesh(cube)

        # projection matrix
        fNear = 0.1
        fFar = 1000.0
        fFov = 90.0
        fAspectRatio = self.screen_height / self.screen_width
        fFovRad = 1.0 / float(math.tan(fFov * 0.5 / 180.0 * math.pi))

        self.matProj[0][0] = fAspectRatio * fFovRad
        self.matProj[1][1] = fFovRad
        self.matProj[2][2] = fFar / (fFar - fNear)
        self.matProj[3][2] = (-fFar * fNear) / (fFar - fNear)
        self.matProj[2][3] = 1.0
        self.matProj[3][3] = 0.0

        return True

    def on_user_update(self, screen, color, fElapsedTime) -> bool:

        # rotation matrices
        matRotZ = mat4x4()
        matRotX = mat4x4()

        self.fTheta += 1.0 * fElapsedTime 

        # rotation z
        matRotZ[0][0] = math.cos(self.fTheta)
        matRotZ[0][1] = math.sin(self.fTheta)
        matRotZ[1][0] = -math.sin(self.fTheta)
        matRotZ[1][1] = math.cos(self.fTheta)
        matRotZ[2][2] = 1
        matRotZ[3][3] = 1

         # rotation x
        matRotX[0][0] = 1
        matRotX[1][1] = math.cos(self.fTheta * 0.5)
        matRotX[1][2] = math.sin(self.fTheta * 0.5)
        matRotX[2][1] = -math.sin(self.fTheta * 0.5)
        matRotX[2][2] = math.cos(self.fTheta * 0.5)
        matRotX[3][3] = 1


        # draw triangle
        for i in self.meshCube.tris:

            tri = copy.deepcopy(i)
            triProjected = Triangle()
            triRotatedZ = Triangle()
            triRotatedZX = Triangle()

            # rotate z
            multiply_matrix_vector(tri.vects[0], triRotatedZ.vects[0], matRotZ)
            multiply_matrix_vector(tri.vects[1], triRotatedZ.vects[1], matRotZ)
            multiply_matrix_vector(tri.vects[2], triRotatedZ.vects[2], matRotZ)

            # rotate x
            multiply_matrix_vector(triRotatedZ.vects[0], triRotatedZX.vects[0], matRotX)
            multiply_matrix_vector(triRotatedZ.vects[1], triRotatedZX.vects[1], matRotX)
            multiply_matrix_vector(triRotatedZ.vects[2], triRotatedZX.vects[2], matRotX)
            
            # Offset into the screen
            triTranslated = copy.deepcopy(triRotatedZX)
            triTranslated.vects[0].z = triRotatedZX.vects[0].z + 3.0
            triTranslated.vects[1].z = triRotatedZX.vects[1].z + 3.0
            triTranslated.vects[2].z = triRotatedZX.vects[2].z + 3.0

            # converting our 3d coordinates into a 2d space
            multiply_matrix_vector(triTranslated.vects[0], triProjected.vects[0], self.matProj)
            multiply_matrix_vector(triTranslated.vects[1], triProjected.vects[1], self.matProj)
            multiply_matrix_vector(triTranslated.vects[2], triProjected.vects[2], self.matProj)

            # scale
            mult = 0.5

            triProjected.vects[0].x += 1.0
            triProjected.vects[0].y += 1.0

            triProjected.vects[1].x += 1.0
            triProjected.vects[1].y += 1.0

            triProjected.vects[2].x += 1.0
            triProjected.vects[2].y += 1.0

            triProjected.vects[0].x *= mult * self.screen_width
            triProjected.vects[0].y *= mult * self.screen_height
            triProjected.vects[1].x *= mult * self.screen_width
            triProjected.vects[1].y *= mult * self.screen_height
            triProjected.vects[2].x *= mult * self.screen_width
            triProjected.vects[2].y *= mult * self.screen_height

            # converting our 3d coordinates to a 2d space
            fProjected = [
                [triProjected.vects[0].x, triProjected.vects[0].y],
                [triProjected.vects[1].x, triProjected.vects[1].y],
                [triProjected.vects[2].x, triProjected.vects[2].y]
            ]

            # rasterize
            pygame.draw.polygon(screen, color, fProjected, 2)
