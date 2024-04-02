import Rhino.Geometry as rg
import traceback

TOLERANCE = 0.01

def create_mug_body(origin, normal, radius, height):
    """
    This function creates a 3D model of a mug body. 
    The body is modeled as a cylinder.
    
    Parameters:
        origin (Rhino.Geometry.Point3d): origin of the mug body plane
        normal (Rhino.Geometry.Vector3d): normal of mug body plane 
        radius (float): the radius of the mug 
        height (float): the height of the mug
    
    Return: 
        Rhino.Geometry.Brep: 3D model of the mug body
    """
    try:
        print("INFO: create_mug_body - start", locals())
        # Create plane to locate the body
        plane = rg.Plane(origin,normal)
        
        # Create the base circle at the bottom of the mug
        base_circle = rg.Circle(plane, radius)

        # Create cylinder with open bottom and top
        cylinder = rg.Cylinder(base_circle, height)
        cap_bottom = False
        cap_top = False
        mug = cylinder.ToBrep(cap_bottom, cap_top)
        print("INFO: create_mug_body - return", mug)
        return mug
    except Exception as error:
        print("ERROR: create_mug_body ", traceback.format_exc())
        return None

# Parameters
body_radius = 50
body_height = 100
body_origin = rg.Point3d(0,0,0)
body_normal = rg.Vector3d.ZAxis

# Assembling
mug_body = create_mug_body(body_origin, body_normal, body_radius, body_height)

# Return created object by placing it in variable a
a = mug_body