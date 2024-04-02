import rhinoinside
rhinoinside.load()
import Rhino.Geometry as rg
import traceback

print('finished loading rhinoinside')
TOLERANCE = 0.01


def create_glass_base(origin, normal, radius):
    """
    This function creates a 3D model of a glass base.
    The base is modeled as a circle at the base of the glass.

    Parameters:
        origin (Rhino.Geometry.Point3d): origin of the glass base plane
        normal (Rhino.Geometry.Vector3d): normal of glass base plane
        radius (float): the radius of the base

    Return:
        Rhino.Geometry.Brep: 3D model of the base
    """
    TOLERANCE = 0.01

    try:
        print("INFO: create_glass_base - start", locals())
        # Create plane to locate the base
        plane = rg.Plane(origin, normal)

        # Create the base circle
        base_circle = rg.Circle(plane, radius).ToNurbsCurve()

        # Create the base
        base = rg.Brep.CreatePlanarBreps(base_circle, TOLERANCE)[0]

        print("INFO: create_glass_base - return", base)
        return base

    except Exception as error:
        print("ERROR: create_glass_base ", "An error occurred:", traceback.format_exc())
        return None


# Parameters
body_radius = 60
body_origin = rg.Point3d(0, 0, 0)
body_normal = rg.Vector3d.ZAxis

base_radius = body_radius
base_origin = body_origin
base_normal = body_normal

# Assembling
glass_base = create_glass_base(base_origin, base_normal, base_radius)

# Return the created object by placing it in variable a
a = glass_base