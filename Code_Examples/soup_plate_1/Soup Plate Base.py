import Rhino.Geometry as rg
import traceback

TOLERANCE = 0.01

def create_soup_plate_base(base_radius, origin, normal):
    """
    This function creates a 3D model of a  soup plate base. 
    The soup plate base is modeled as a flat surface in a circle shape at the bottom of the soup plate.

    Parameters:
        base_origin (Rhino.Geometry.Point3d): the origin of the soup plate base plane
        base_normal (Rhino.Geometry.Vector3d): the normal of the soup plate base plane
        base_radius (float): the radius of the soup plate base

    Return: 
        Rhino.Geometry.Brep: 3D model of the soup plate
    """
    try:
        print("INFO: create_soup_plate_base - start", locals())
        #create a plane to locate the soup plate base
        base_plane = rg.Plane(origin, normal)

        #create the plate base
        base_circle = rg.Circle(base_plane, base_radius)
        plate_base = rg.Brep.CreatePlanarBreps(base_circle.ToNurbsCurve(), TOLERANCE)[0]  

        print("INFO: create_soup_plate_base - return", plate_base)
        return plate_base 
    except Exception as error:
        print("ERROR: create_soup_plate_base ", "An error occurred:", traceback.format_exc())
        return None

# Parameters
body_bottom_radius = 100
body_origin = rg.Point3d(0, 0, 0)
body_normal = rg.Vector3d.ZAxis

base_radius = body_bottom_radius
base_origin = body_origin
base_normal = body_normal

# Assembling
soup_plate_base = create_soup_plate_base(base_radius, base_origin, base_normal)

# Return the created object by placing it in variable a
a = soup_plate_base
