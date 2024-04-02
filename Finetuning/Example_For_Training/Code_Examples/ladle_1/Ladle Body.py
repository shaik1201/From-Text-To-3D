import Rhino.Geometry as rg
import traceback

TOLERANCE = 0.01

def create_ladle_body(origin, normal, radius):
    """
    This function creates a 3D model of a ladle body. 
    The ladle body is modeled as a hollow hemisphere.

    Parameters:
        origin (Rhino.Geometry.Point3d): the origin of the ladle body
        normal (Rhino.Geometry.Vector3d): the normal of ladle body
        radius (float): the radius of the sphere

    Returns: 
        Rhino.Geometry.Brep: 3D model of the ladle body
    """
    try:
        print("INFO: create_ladle_body - start", locals())
        # Determine the middle point of the sphere
        sphere_mid_point = origin + (normal * radius)

        # Create a sphere for the ladle body
        sphere = rg.Sphere(sphere_mid_point, radius).ToBrep()

        # Create cutting surface (a circle) in the middle of the sphere to create a hemisphere
        mid_plane = rg.Plane(sphere_mid_point, normal)
        cutting_circle = rg.Circle(mid_plane, radius).ToNurbsCurve()
        cutter = rg.Brep.CreatePlanarBreps(cutting_circle, TOLERANCE)[0]  

        # Trim the sphere using the cutting brep
        splited_sphere = rg.Brep.Split(sphere, cutter, TOLERANCE)

        if splited_sphere:
        # Get the bottom part of the body by selecting the last item
            hollow_half_sphere = splited_sphere[-1]
        else:
             hollow_half_sphere = None

        print("INFO: create_ladle_body - return", hollow_half_sphere)
        return hollow_half_sphere
    except Exception as error:
        print("ERROR: create_ladle_body ", "An error occurred:", traceback.format_exc())
        return None

# Parameters
ladle_radius = 45
body_origin = rg.Point3d(0, 0, 0)
body_normal = rg.Vector3d.ZAxis

# Assembling
ladle_body = create_ladle_body(body_origin, body_normal, ladle_radius)

# Return the created object by placing it in variable a
a = ladle_body
