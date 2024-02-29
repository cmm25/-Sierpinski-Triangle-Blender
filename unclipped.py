import bpy as D
import random

class SierpinskiTriangle:
    def __init__(self):
        self.base_triangle_vertices = [(-7, -7, 0), (7, -7, 0), (0, 7, 0)]
        self.colors = [(1, 0, 0, 1), (0, 0, 0, 1), (1, 1, 0, 1), (1, 1, 1, 1),(0.2,0.5,0.9,1),(0.7,1,0.3,1) ,(0, 1, 0, 1), (1, 0.5, 0, 1)]

    def draw_triangle(self, color, vertices):
        mesh = D.data.meshes.new(name="triangle")
        # Create a new object using the mesh
        obj = D.data.objects.new("Triangle", mesh)
        # Link the object to the current collection
        D.context.collection.objects.link(obj)
        # Set vertices and faces for the mesh
        mesh.from_pydata(vertices, [], [(0, 1, 2)])
        mesh.update()

        # Create a new material with the specified color
        color_material = D.data.materials.new(name="Color")
        color_material.diffuse_color = color
        # Assign the material to the mesh
        mesh.materials.append(color_material)

    def sierpinski(self, x, y, z, depth):
        if depth == 0:
            self.draw_triangle(random.choice(self.colors), [x, y, z])
        else:
            mid1 = [(x[0] + y[0]) / 2, (x[1] + y[1]) / 2, (x[2] + y[2]) / 2]
            mid2 = [(y[0] + z[0]) / 2, (y[1] + z[1]) / 2, (y[2] + z[2]) / 2]
            mid3 = [(x[0] + z[0]) / 2, (x[1] + z[1]) / 2, (x[2] + z[2]) / 2]

            # Recursively call the function with smaller triangles
            self.sierpinski(x, mid1, mid3, depth - 1)
            self.sierpinski(mid1, y, mid2, depth - 1)
            self.sierpinski(mid3, mid2, z, depth - 1)

    def generate_fractal(self, depth):
        # Generate Sierpinski triangle with given depth
        self.sierpinski(self.base_triangle_vertices[0], self.base_triangle_vertices[1], self.base_triangle_vertices[2], depth)


sierpinski_triangle = SierpinskiTriangle()
# Generate the Sierpinski triangle fractal with specified depth
sierpinski_triangle.generate_fractal(6)
