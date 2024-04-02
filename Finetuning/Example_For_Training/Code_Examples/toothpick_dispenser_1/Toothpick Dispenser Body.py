import rhinoinside
rhinoinside.load()
import Rhino.Geometry as rg
import traceback
import math

print('finished loading rhinoinside')
TOLERANCE = 0.01


def create_toothpick_dispenser_body(origin, normal, radius, height):
    """
    This function creates a 3D model of a toothpick dispenser body. 
    The body is modeled as a cylinder.

    Parameters:
        origin (Rhino.Geometry.Point3d): origin of the toothpick dispenser body plane
        normal (Rhino.Geometry.Vector3d): normal of toothpick dispenser body plane 
        radius (float): the radius of the body
        height (float): the height of the body

    Return: 
    Rhino.Geometry.Brep: 3D model of the body
    """

    try:
        print("INFO: create_toothpick_dispenser_body - start", locals())
        # Create plane to locate the body
        plane = rg.Plane(origin, normal)

        # Create the base circle at the bottom of the mug
        base_circle = rg.Circle(plane, radius)

        # Create cylinder with open bottom and top
        cylinder = rg.Cylinder(base_circle, height)
        cap_bottom = False
        cap_top = False
        body = cylinder.ToBrep(cap_bottom, cap_top)
        print("INFO: create_toothpick_dispenser_body - return", body)
        return body

    except Exception as error:
        print("ERROR: create_toothpick_dispenser_body ", "An error occurred:", traceback.format_exc())
        return None


# Parameters
body_radius = 20
body_height = 60
body_origin = rg.Point3d(0, 0, 0)
body_normal = rg.Vector3d.ZAxis

# Assembling
toothpick_dispenser_body = create_toothpick_dispenser_body(body_origin, body_normal, body_radius, body_height)

# Return created object by placing it in variable a
a = toothpick_dispenser_body
