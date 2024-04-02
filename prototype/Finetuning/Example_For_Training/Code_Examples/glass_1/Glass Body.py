import rhinoinside
rhinoinside.load()
import Rhino.Geometry as rg
import traceback

print('finished loading rhinoinside')
TOLERANCE = 0.01


def create_glass_body(origin, normal, radius, height):
    """
    This function creates a 3D model of a glass body. 
    The body is modeled as an open cylinder.

    Parameters:
        origin (Rhino.Geometry.Point3d): the origin of the glass body plane
        normal (Rhino.Geometry.Vector3d): the normal of the glass body plane
        radius (float): the radius of the glass body
        height (float): the height of the glass body

    Return: 
        Rhino.Geometry.Brep: the created 3D model
    """

    try:
        print("INFO: create_glass_body - start", locals())
        # Create plane to locate the body
        plane = rg.Plane(origin, normal)

        # Create the base circle at the bottom of the glass
        base_circle = rg.Circle(plane, radius)

        # Create open cylinder
        cylinder = rg.Cylinder(base_circle, height)
        cap_bottom = False
        cap_top = False
        glass = cylinder.ToBrep(cap_bottom, cap_top)

        print("INFO: create_glass_body - return", glass)
        return glass

    except Exception as error:
        print("ERROR: create_glass_body ", "An error occurred:", traceback.format_exc())
        return None


# Parameters
body_radius = 80
body_height = 300
body_origin = rg.Point3d(0, 0, 0)
body_normal = rg.Vector3d.ZAxis

# Assembling
glass_body = create_glass_body(body_origin, body_normal, body_radius, body_height)

# Return the created object by placing it in variable a
a = glass_body