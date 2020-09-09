import math
import pygame
import copy
from Scripts.geometry import *
from Scripts.utility_functions import *
from Lib.primitives import *
from Lib.colors import *
import operator
from operator import attrgetter


"""

graphicsEngine3d.py
author: Damian Diaz

the meat and potatoes

"""


class GraphicsEngine:

    def __init__(self, width, height):
        self.screen_width = width
        self.screen_height = height
        self.mesh = Mesh()
        self.mat_projection = mat_4x4()
        self.f_theta = 0

    def on_user_create(self):

        # create a cube mesh
        #self.mesh = create_cube()

        # create ship mesh
        self.mesh = load_from_obj('ship.obj')

        # projection matrix
        f_near = 0.1
        f_far = 1000.0
        f_fov = 90.0
        f_aspect_ratio = self.screen_height / self.screen_width
        f_fov_rad = 1.0 / float(math.tan(f_fov * 0.5 / 180.0 * math.pi))

        self.mat_projection[0][0] = f_aspect_ratio * f_fov_rad
        self.mat_projection[1][1] = f_fov_rad
        self.mat_projection[2][2] = f_far / (f_far - f_near)
        self.mat_projection[3][2] = (-f_far * f_near) / (f_far - f_near)
        self.mat_projection[2][3] = 1.0
        self.mat_projection[3][3] = 0.0

        return True

    def on_user_update(self, screen, f_elapsed_time, wire_mode=False) -> bool:

        # rotation matrices
        mat_rot_z = mat_4x4()
        mat_rot_x = mat_4x4()

        self.f_theta += 1.0 * f_elapsed_time

        # rotation z
        mat_rot_z[0][0] = math.cos(self.f_theta)
        mat_rot_z[0][1] = math.sin(self.f_theta)
        mat_rot_z[1][0] = -math.sin(self.f_theta)
        mat_rot_z[1][1] = math.cos(self.f_theta)
        mat_rot_z[2][2] = 1
        mat_rot_z[3][3] = 1

        # rotation x
        mat_rot_x[0][0] = 1
        mat_rot_x[1][1] = math.cos(self.f_theta * 0.5)
        mat_rot_x[1][2] = math.sin(self.f_theta * 0.5)
        mat_rot_x[2][1] = -math.sin(self.f_theta * 0.5)
        mat_rot_x[2][2] = math.cos(self.f_theta * 0.5)
        mat_rot_x[3][3] = 1

        tris_to_raster = []

        # draw triangle
        for i in self.mesh.tris:

            tri = copy.deepcopy(i)
            tri_projected = Triangle()
            tri_rotated_z = Triangle()
            tri_rotated_zx = Triangle()

            # rotate z
            multiply_matrix_vector(tri.vectors[0], tri_rotated_z.vectors[0], mat_rot_z)
            multiply_matrix_vector(tri.vectors[1], tri_rotated_z.vectors[1], mat_rot_z)
            multiply_matrix_vector(tri.vectors[2], tri_rotated_z.vectors[2], mat_rot_z)

            # rotate x
            multiply_matrix_vector(
                tri_rotated_z.vectors[0], tri_rotated_zx.vectors[0], mat_rot_x)
            multiply_matrix_vector(
                tri_rotated_z.vectors[1], tri_rotated_zx.vectors[1], mat_rot_x)
            multiply_matrix_vector(
                tri_rotated_z.vectors[2], tri_rotated_zx.vectors[2], mat_rot_x)

            # Offset into the screen
            tri_translated = copy.deepcopy(tri_rotated_zx)
            tri_translated.vectors[0].z = tri_rotated_zx.vectors[0].z + 8
            tri_translated.vectors[1].z = tri_rotated_zx.vectors[1].z + 8
            tri_translated.vectors[2].z = tri_rotated_zx.vectors[2].z + 8

            # Normals
            normal = Vector()

            line1 = Vector()
            line2 = Vector()
            camera = Vector()

            line1.x = tri_translated.vectors[1].x - tri_translated.vectors[0].x
            line1.y = tri_translated.vectors[1].y - tri_translated.vectors[0].y
            line1.z = tri_translated.vectors[1].z - tri_translated.vectors[0].z

            line2.x = tri_translated.vectors[2].x - tri_translated.vectors[0].x
            line2.y = tri_translated.vectors[2].y - tri_translated.vectors[0].y
            line2.z = tri_translated.vectors[2].z - tri_translated.vectors[0].z

            normal.x = line1.y * line2.z - line1.z * line2.y
            normal.y = line1.z * line2.x - line1.x * line2.z
            normal.z = line1.x * line2.y - line1.y * line2.x
            normalize(normal)

            # dot product
            normal_dp = dot_product(normal, tri_translated, camera)

            # display vertices that exist behind normals
            if normal_dp < 0.0:

                # illumination
                light = Vector(0, 0, -1)
                normalize(light)
                light_dp = max(0, (normal.x * light.x + normal.y * light.y + normal.z * light.z))
                
                color = (light_dp * 255 , light_dp * 255, light_dp * 255)
                tri_projected.color = color

                # converting our 3d coordinates into a 2d space
                multiply_matrix_vector(
                    tri_translated.vectors[0], tri_projected.vectors[0], self.mat_projection)
                multiply_matrix_vector(
                    tri_translated.vectors[1], tri_projected.vectors[1], self.mat_projection)
                multiply_matrix_vector(
                    tri_translated.vectors[2], tri_projected.vectors[2], self.mat_projection)

                # scale
                tri_projected.vectors[0].x += 1.0
                tri_projected.vectors[0].y += 1.0

                tri_projected.vectors[1].x += 1.0
                tri_projected.vectors[1].y += 1.0

                tri_projected.vectors[2].x += 1.0
                tri_projected.vectors[2].y += 1.0

                tri_projected.vectors[0].x *= 0.5 * self.screen_width
                tri_projected.vectors[0].y *= 0.5 * self.screen_height
                tri_projected.vectors[1].x *= 0.5 * self.screen_width
                tri_projected.vectors[1].y *= 0.5 * self.screen_height
                tri_projected.vectors[2].x *= 0.5 * self.screen_width
                tri_projected.vectors[2].y *= 0.5 * self.screen_height

                z = float(tri_projected.vectors[0].z + tri_projected.vectors[1].z + tri_projected.vectors[2].z) / 3
                tri_projected.midpoint = z

                tris_to_raster.append(tri_projected)

        # render order back to front
        render_order = sorted(tris_to_raster, key=operator.attrgetter("midpoint"), reverse=True)

        for x in render_order:

            # converting our 3d coordinates to a 2d space
            f_projected = [
                [x.vectors[0].x, x.vectors[0].y],
                [x.vectors[1].x, x.vectors[1].y],
                [x.vectors[2].x, x.vectors[2].y]
            ]

            color = x.color

            # draw final tri
            if wire_mode:
                pygame.draw.polygon(screen, white, f_projected, 2)
            else:
                pygame.draw.polygon(screen, color, f_projected)
