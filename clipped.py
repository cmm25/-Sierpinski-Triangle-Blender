import bpy as D
import random

class SierpinskiTriangle:
    def __init__(self):
        self.base_triangle_vertices = [(-7, -7, 0), (7, -7, 0), (0, 7, 0)]
        self.colors = [(1, 0, 0, 1), (0, 0, 0, 1), (1, 1, 0, 1), (1, 1, 1, 1), (0.2, 0.5, 0.9, 1), (0.7, 1, 0.3, 1), (0, 1, 0, 1), (1, 0.5, 0, 1)]

    def draw_triangle(self, color, vertices):
        mesh = D.data.meshes.new(name="triangle")
        obj = D.data.objects.new("Triangle", mesh)
        D.context.collection.objects.link(obj)
        mesh.from_pydata(vertices, [], [(0, 1, 2)])
        mesh.update()

        # Create a new material with the specified color
        color_material = D.data.materials.new(name="Color")
        color_material.diffuse_color = color
        mesh.materials.append(color_material)

    def clip_polygon(self, subject_polygon, clipping_polygon):
        result = []
        subject = subject_polygon.copy()

        for i in range(len(clipping_polygon)):
            next_index = (i + 1) % len(clipping_polygon)
            clip_start = clipping_polygon[i]
            clip_end = clipping_polygon[next_index]

            output_polygon = []
            for j in range(len(subject)):
                next_subject = (j + 1) % len(subject)
                subject_start = subject[j]
                subject_end = subject[next_subject]

                intersection = self.calculate_intersection(subject_start, subject_end, clip_start, clip_end)
                if intersection:
                    self.classify_intersection(intersection, subject_start, subject_end, clip_end)

                    if intersection[0] == -1.0:
                        output_polygon.append(intersection)
                        if subject_end[0] >= 0:  # Check if next vertex is inside clipping region
                            output_polygon.append(subject_end)
                    elif intersection[0] == -2.0:
                        output_polygon.append(intersection)
                    else:  # Exiting case (intersection.x == -3.0)
                        # Add the remaining part of the subject polygon to the output
                        if subject_end[0] >= intersection[0]:
                            output_polygon.append(subject_end)

            subject = output_polygon

        # Final step for backward clipping: reverse the output polygon
        result = output_polygon[::-1]

        # Keep only points inside the clipping region
        for point in result:
            if point[0] >= 0:
                result.append(point)

        return result

    def calculate_intersection(self, p1, p2, p3, p4):
        x1, y1, z1 = p1
        x2, y2, z2 = p2
        x3, y3, z3 = p3
        x4, y4, z4 = p4

        s1_x = x2[0] - x1[0]
        s1_y = y2[0] - y1[0]
        s2_x = x4[0] - x3[0]
        s2_y = y4[0] - y3[0]

        denom = s1_x * s2_y - s2_x * s1_y
        if denom == 0:  # Lines are parallel
            return None

        s = (-s1_y * (x1 - x3) + s1_x * (y1 - y3)) / denom
        t = (s2_x * (y1 - y3) - s2_y * (x1 - x3)) / denom

        if 0 <= s <= 1 and 0 <= t <= 1:
            # Intersection exists
            intersection_x = x1 + (t * s1_x)
            intersection_y = y1 + (t * s1_y)
            return intersection_x, intersection_y
        else:
            return None  # No intersectioncf


    def classify_intersection(self, intersection, edge_start, edge_end, clip_vertex):
        dx = edge_end[0] - edge_start[0]
        dy = edge_end[1] - edge_start[1]
        dxi = clip_vertex[0] - edge_start[0]
        dyi = clip_vertex[1] - edge_start[1]
        cross_product = dx * dyi - dy * dxi

        if dy == 0:
            if dx > 0 and clip_vertex[1] < edge_start[1]:
                intersection[0] = -1.0  # Entering
            elif dx < 0 and clip_vertex[1] > edge_start[1]:
                intersection[0] = -2.0  # Entering
            else:
                intersection[0] = -3.0  # Exiting
        elif cross_product > 0:
            intersection[0] = -1.0  # Entering
        else:
            intersection[0] = -3.0  # Exiting

    def sierpinski(self, x, y, z, depth, clipping_polygon=None):
        if depth == 0:
            # Clip the triangle even for depth 0
            clipped_triangle = self.clip_polygon([[x, y, z]], clipping_polygon) if clipping_polygon else [[x, y, z]]
            if clipped_triangle:  # Only draw if clipping produced a valid triangle
                self.draw_triangle(random.choice(self.colors), clipped_triangle[0])
        else:
            mid1 = [(x[0] + y[0]) / 2, (x[1] + y[1]) / 2, (x[2] + z[2]) / 2]
            mid2 = [(y[0] + z[0]) / 2, (y[1] + z[1]) / 2, (y[2] + z[2]) / 2]
            mid3 = [(x[0] + z[0]) / 2, (x[1] + z[1]) / 2, (x[2] + z[2]) / 2]

            # Apply clipping to all recursive calls
            self.sierpinski(x, mid1, mid3, depth - 1, clipping_polygon)
            self.sierpinski(mid1, y, mid2, depth - 1, clipping_polygon)
            self.sierpinski(mid3, mid2, z, depth - 1, clipping_polygon)

    def generate_fractal(self, depth, clipping_polygon=None):
        # Generate Sierpinski triangle with clipping only for the first triangle
        self.sierpinski(self.base_triangle_vertices[0], self.base_triangle_vertices[1], self.base_triangle_vertices[2], depth, clipping_polygon)

# Example usage with a clipping polygon
clipping_polygon = [(-4, 0, 0), (4, 0, 0), (0, 4, 0)]  # Example clip region
sierpinski_triangle = SierpinskiTriangle()
sierpinski_triangle.generate_fractal(5, clipping_polygon)
