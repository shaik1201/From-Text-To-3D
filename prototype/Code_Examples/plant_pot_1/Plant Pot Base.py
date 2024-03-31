import Rhino.Geometry as rg
import traceback
import math

TOLERANCE = 0.01

def create_plant_pot_base(origin, normal, radius, alignment, triangles_width, triangle_bisection):
    """
    This function creates a 3D model of a plant pot base. 
    The base is modeled as a circular surface with a triangular pattern along its edges.

    Parameters:
        origin (Rhino.Geometry.Point3d): the origin of the base plane
        normal (Rhino.Geometry.Vector3d): the normal of the base plane
        radius (float): the radius of the base
        alignment (Rhino.Geometry.Vector3d): the direction in which the triangles are pointed
        triangles_width (float): the width of the triangles
        triangle_bisection (float): the length of the bisection (or the height) of the triangle

    Return: 
        tuple: 3D models of the plant pot base
    """
    try:
        print("INFO: create_plant_pot_base - start", locals())
        # Create a plane to locate the base
        base_plane = rg.Plane(origin, normal)

        # Create the base circle of the base
        base_circle = rg.Circle(base_plane, radius).ToNurbsCurve()

        # Initialize lists to store triangles
        top_triangles = []
        bottom_triangles = []

        # Get the circumference of the base circle
        circumference = base_circle.GetLength()

        # Calculate the number of triangles needed to cover the circumference
        num_triangles = int(circumference / triangles_width)

        # Calculate the angle between each triangle
        angle_between_triangles = 2 * math.pi / num_triangles

        # Loop to create triangle
        for i in range(num_triangles):
            # Calculate start and end angles for the current triangle
            start_angle = i * angle_between_triangles
            end_angle = (i + 1) * angle_between_triangles

            # Find the triangle corners on the top circle
            triangle_corner1 = base_circle.PointAt(start_angle) 
            triangle_corner2 = base_circle.PointAt(end_angle)

            # Calculate midpoint of the line connecting start and end points
            midpoint = (triangle_corner1 + triangle_corner2) / 2

            # Vector from center to midpoint
            center_to_midpoint = midpoint - rg.Circle(base_plane, radius).Center

            # Move the triangle edge along the calculated vector
            triangle_edge = midpoint + (center_to_midpoint * triangle_bisection)

            # Create the triangle
            triangle = rg.Polyline([triangle_corner2, triangle_edge, triangle_corner1]).ToNurbsCurve()

            # Append triangle to the lists
            bottom_triangles.append(triangle)

        # Join the bottom triangles to create a single polyline represent the base
        bottom_shape = rg.Curve.JoinCurves(bottom_triangles, TOLERANCE)[0]

        # Create a surface out of the bootom shape frame
        base_surface = rg.Brep.CreatePlanarBreps(bottom_shape, TOLERANCE)[0]

        print("INFO: create_plant_pot_base - return", base_surface)
        return base_surface
    except Exception as error:
        print("ERROR: create_plant_pot_base ", "An error occurred:", traceback.format_exc())
        return None

# Parameters
body_radius = 100
body_origin = rg.Point3d(0, 0, 0)
body_normal = rg.Vector3d.ZAxis

triangles_width = 20 
triangle_bisection = 0.2
body_alignment = -rg.Vector3d.XAxis

base_radius = body_radius
base_origin = body_origin
base_normal = body_normal.ZAxis
base_alignment = body_alignment.XAxis

# Assembling
plant_pot_base = create_plant_pot_base(base_origin, base_normal, base_radius, base_alignment, triangles_width, triangle_bisection)

# Return the created object by placing it in variable a
a = plant_pot_base
