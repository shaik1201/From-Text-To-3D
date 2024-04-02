import Rhino.Geometry as rg
import traceback
import math

TOLERANCE = 0.01

def create_plant_pot_body(origin, normal, alignment, radius, triangles_width, triangle_bisection, height, angle):
    """
    This function creates a 3D model of a plant pot body. 
    The body of the mold is modeled as a twisted cylindrical body with triangular patterns along its edge surface.

    Parameters:
        origin (Rhino.Geometry.Point3d): the origin of the body plane
        normal (Rhino.Geometry.Vector3d): the normal of the body plane
        radius (float): the radius of the body
        alignment (Rhino.Geometry.Vector3d): the direction in which the triangles are pointed
        triangles_width (float): the width of the triangles
        triangle_bisection (float): the length of the bisection (or the height) of the triangle
        height (Rhino.Geometry.Vector3d): vector indicating the direction and distance to move the geometry
        angle (float): angle in degrees to rotate the geometry fot twisting the shape.

    Return: 
        tuple: 3D models of the plant pot body
    """
    try:
        print("INFO: create_plant_pot_body - start", locals())
        # Create a plane to locate the body
        body_plane = rg.Plane(origin, normal)

        # Create the base circle of the body
        base_circle = rg.Circle(body_plane, radius).ToNurbsCurve()

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
            center_to_midpoint = midpoint - rg.Circle(body_plane, radius).Center

            # Move the triangle edge along the calculated vector
            triangle_edge = midpoint + (center_to_midpoint * triangle_bisection)

            # Create the triangle
            triangle = rg.Polyline([triangle_corner2, triangle_edge, triangle_corner1]).ToNurbsCurve()

            # Append triangle to the lists
            bottom_triangles.append(triangle)

        # Join the bottom triangles to create a single polyline represent the base
        bottom_shape = rg.Curve.JoinCurves(bottom_triangles, TOLERANCE)[0]

        # Move the top geometry by height parameter
        translation = rg.Transform.Translation(normal * height)
        top_shape = bottom_shape.Duplicate()
        top_shape.Transform(translation)

        # Rotate the top geometry by angle around the body normal to create a twisting shape
        rotation_axis = normal
        rotation_angle = math.radians(angle)
        rotation = rg.Transform.Rotation(rotation_angle, origin)
        top_shape.Transform(rotation)

        # Create the body by lofting the two shapes
        closed = False
        loft = rg.Brep.CreateFromLoft([top_shape, bottom_shape], rg.Point3d.Unset, rg.Point3d.Unset, rg.LoftType.Normal, closed)[0]

        print("INFO: create_plant_pot_body - return", base_circle)
        return loft, top_shape
    except Exception as error:
        print("ERROR: create_plant_pot_body ", "An error occurred:", traceback.format_exc())
        return None

# Parameters
body_origin = rg.Point3d(0, 0, 0)
body_normal = rg.Vector3d.ZAxis
body_alignment = -rg.Vector3d.XAxis
body_radius = 100
triangles_width = 20 
triangle_bisection = 0.2
body_height = 200 
twisting_angle = 60

# Assembling
plant_pot_body = create_plant_pot_body(body_origin, body_normal, body_alignment, body_radius, triangles_width, triangle_bisection, body_height, twisting_angle)

# Return the created object by placing it in variable a
a = plant_pot_body
