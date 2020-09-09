import math
import pygame
import copy
from Scripts.geometry import *
from Scripts.projection import *
from Lib.primitaves import *
from Lib.colors import *
import operator
from operator import attrgetter

"""

graphicsEngine3d.py
author: Damian Diaz

the meat and potatoes

"""


class ge3d:

    def __init__(self, width, height):
        self.screen_width = width
        self.screen_height = height
        self.mesh = Mesh()
        self.matProj = mat4x4()
        self.fTheta = 0

    def on_user_create(self):

        # create a cube mesh
        #self.mesh = create_cube(cube)

        # create ship mesh
        self.mesh = load_from_obj('ship.obj')

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

    def on_user_update(self, screen, fElapsedTime, wireframe=False) -> bool:

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

        trisToRaster = []

        # draw triangle
        for i in self.mesh.tris:

            tri = copy.deepcopy(i)
            triProjected = Triangle()
            triRotatedZ = Triangle()
            triRotatedZX = Triangle()

            # rotate z
            multiply_matrix_vector(tri.vects[0], triRotatedZ.vects[0], matRotZ)
            multiply_matrix_vector(tri.vects[1], triRotatedZ.vects[1], matRotZ)
            multiply_matrix_vector(tri.vects[2], triRotatedZ.vects[2], matRotZ)

            # rotate x
            multiply_matrix_vector(
                triRotatedZ.vects[0], triRotatedZX.vects[0], matRotX)
            multiply_matrix_vector(
                triRotatedZ.vects[1], triRotatedZX.vects[1], matRotX)
            multiply_matrix_vector(
                triRotatedZ.vects[2], triRotatedZX.vects[2], matRotX)

            # Offset into the screen
            triTranslated = copy.deepcopy(triRotatedZX)
            triTranslated.vects[0].z = triRotatedZX.vects[0].z + 8
            triTranslated.vects[1].z = triRotatedZX.vects[1].z + 8
            triTranslated.vects[2].z = triRotatedZX.vects[2].z + 8

            # Normals
            normal = Vector()

            line1 = Vector()
            line2 = Vector()
            camera = Vector()

            line1.x = triTranslated.vects[1].x - triTranslated.vects[0].x
            line1.y = triTranslated.vects[1].y - triTranslated.vects[0].y
            line1.z = triTranslated.vects[1].z - triTranslated.vects[0].z

            line2.x = triTranslated.vects[2].x - triTranslated.vects[0].x
            line2.y = triTranslated.vects[2].y - triTranslated.vects[0].y
            line2.z = triTranslated.vects[2].z - triTranslated.vects[0].z

            normal.x = line1.y * line2.z - line1.z * line2.y
            normal.y = line1.z * line2.x - line1.x * line2.z
            normal.z = line1.x * line2.y - line1.y * line2.x
            normalize(normal)

            # dot product
            normal_dp = dot_product(normal, triTranslated, camera)

            # display verts that exist behind normals
            if normal_dp < 0.0:

                # illumintaion
                light = Vector(0, 0, -1)
                normalize(light)
                light_dp = max(0, (normal.x * light.x + normal.y * light.y + normal.z * light.z))
                
                color = (light_dp * 255 , light_dp * 255, light_dp * 255)
                triProjected.color = color

                # converting our 3d coordinates into a 2d space
                multiply_matrix_vector(
                    triTranslated.vects[0], triProjected.vects[0], self.matProj)
                multiply_matrix_vector(
                    triTranslated.vects[1], triProjected.vects[1], self.matProj)
                multiply_matrix_vector(
                    triTranslated.vects[2], triProjected.vects[2], self.matProj)

                # scale
                triProjected.vects[0].x += 1.0
                triProjected.vects[0].y += 1.0

                triProjected.vects[1].x += 1.0
                triProjected.vects[1].y += 1.0

                triProjected.vects[2].x += 1.0
                triProjected.vects[2].y += 1.0

                triProjected.vects[0].x *= 0.5 * self.screen_width
                triProjected.vects[0].y *= 0.5 * self.screen_height
                triProjected.vects[1].x *= 0.5 * self.screen_width
                triProjected.vects[1].y *= 0.5 * self.screen_height
                triProjected.vects[2].x *= 0.5 * self.screen_width
                triProjected.vects[2].y *= 0.5 * self.screen_height

                z = float(triProjected.vects[0].z + triProjected.vects[1].z + triProjected.vects[2].z) / 3
                triProjected.midpoint = z

                trisToRaster.append(triProjected)


        renderOrder = sorted(
            trisToRaster, key=operator.attrgetter("midpoint"), reverse=True)

        for x in renderOrder:

            # converting our 3d coordinates to a 2d space
            fProjected = [
                [x.vects[0].x, x.vects[0].y],
                [x.vects[1].x, x.vects[1].y],
                [x.vects[2].x, x.vects[2].y]
            ]

            c = x.color

            if wireframe:
                pygame.draw.polygon(screen, white, fProjected, 2)
            else:
                pygame.draw.polygon(screen, c, fProjected)
