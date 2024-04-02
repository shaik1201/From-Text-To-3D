import rhinoinside
rhinoinside.load()
import Rhino.Geometry as rg
import traceback
import math

print('finished loading rhinoinside')
TOLERANCE = 0.01


def create_toothpick_dispenser_base(origin, normal, radius):
    """
    This function creates a 3D model of a toothpick dispenser base. 
    The base is modeled as a circle at the bottom of the dispenser.

    Parameters:
        origin (Rhino.Geometry.Point3d): origin of the toothpick dispenser base plane
        normal (Rhino.Geometry.Vector3d): normal of toothpick dispenser base plane 
        radius (float): the radius of the base

    Return: 
    Rhino.Geometry.Brep: 3D model of the base
    """
    TOLERANCE = 0.01

    try:
        print("INFO: create_toothpick_dispenser_base - start", locals())
        # Create plane to locate the base
        plane = rg.Plane(origin, normal)

        # Create the base surface
        base_circle = rg.Circle(plane, radius).ToNurbsCurve()
        base = rg.Brep.CreatePlanarBreps(base_circle, TOLERANCE)[0]

        print("INFO: create_toothpick_dispenser_base - return", base)
        return base

    except Exception as error:
        print("ERROR: create_toothpick_dispenser_base ", "An error occurred:", traceback.format_exc())
        return None


# Parameters
body_radius = 50
body_origin = rg.Point3d(0, 0, 0)
body_normal = rg.Vector3d.ZAxis

base_radius = body_radius
base_origin = body_origin
base_normal = body_normal

# Assembling
toothpick_dispenser_base = create_toothpick_dispenser_base(base_origin, base_normal, base_radius)

# Return the created object by placing it in variable a
a = toothpick_dispenser_base