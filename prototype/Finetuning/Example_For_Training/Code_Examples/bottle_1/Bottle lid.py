import rhinoinside
rhinoinside.load()
import Rhino.Geometry as rg
import traceback

print('finished loading rhinoinside')
TOLERANCE = 0.01


def create_bottle_lid(origin, normal, radius, height):
    """
    This function creates a 3D model of a bottle lid. 
    The lid is modeled as a cylinder with a cap on top.

    Parameters:
        origin (Rhino.Geometry.Point3d): origin of the bottle lid plane
        normal (Rhino.Geometry.Vector3d): normal of bottle lid plane 
        radius (float): the radius of the lid
        height (float): the height of the lid

    Return: 
        Rhino.Geometry.Brep: The created 3D model
    """

    try:
        print("INFO: create_bottle_lid - start", locals())
        # Create plane to locate the lid
        plane = rg.Plane(origin, normal)

        # Create the lid
        base_circle = rg.Circle(plane, radius)
        cylinder = rg.Cylinder(base_circle, height)
        cap_bottom = False
        cap_top = True
        lid = cylinder.ToBrep(cap_bottom, cap_top)

        print("INFO: create_bottle_lid - return", lid)
        return lid

    except Exception as error:
        print("ERROR: create_bottle_lid ", "An error occurred:", traceback.format_exc())
        return None


# Parameters
body_bottom_part_height = 140
body_neck_radius = 25
body_neck_height = 70
body_origin = rg.Point3d(0, 0, 0)
body_normal = rg.Vector3d.ZAxis

lid_radius = body_neck_radius
lid_height = 15
lid_origin = rg.Point3d(0, 0, body_bottom_part_height + body_neck_height - lid_height)
lid_normal = body_normal

# Assembling
bottle_lid = create_bottle_lid(lid_origin, lid_normal, lid_radius, lid_height)

# Return created object by placing it in variable a
a = bottle_lid