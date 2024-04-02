import Rhino.Geometry as rg
import traceback

TOLERANCE = 0.01

def create_pot_body(origin, normal, radius, height):
    """
    This function creates a 3D model of a cooking pot body. 
    The body is modeled as a cylinder.
    
    Parameters:
        origin (Rhino.Geometry.Point3d): origin of the pot body plane
        normal (Rhino.Geometry.Vector3d): normal of pot body plane 
        radius (float): the radius of the pot 
        height (float): the height of the pot
    
    Return: 
        Rhino.Geometry.Brep: 3D model of the pot body
    """
    try:
        print("INFO: create_pot_body - start", locals())
        # Create plane to locate the body
        plane = rg.Plane(origin,normal)
        
        # Create the base circle at the bottom of the pot
        base_circle = rg.Circle(plane, radius)

        # Create open cylinder
        cylinder = rg.Cylinder(base_circle, height)
        cap_bottom = False
        cap_top = False
        pot = cylinder.ToBrep(cap_bottom, cap_top)
        print("INFO: create_pot_body - return", pot)
        return pot
    except Exception as error:
        print("ERROR: create_pot_body ", traceback.format_exc())
        return None

# Parameters
body_radius = 150
body_height = 130
body_origin = rg.Point3d(0,0,0)
body_normal = rg.Vector3d.ZAxis

# Assembling
pot_body = create_pot_body(body_origin, body_normal, body_radius, body_height)

# Return created object by placing it in variable a
a = pot_body