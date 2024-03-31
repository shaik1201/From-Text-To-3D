import rhinoinside
rhinoinside.load()
# System and Rhino can only be loaded after rhinoinside is initialized
import Rhino.Geometry as rg  # noqa
import Rhino
import traceback
import math

print('finished loading rhinoinside')
TOLERANCE = 0.01


def create_toothpick_dispenser_lid_retention_ring(origin, normal, radius, height):
    """
    This function creates a 3D model of a toothpick dispenser lid retention ring. 
    The ring is modeled as a torus.

    Parameters:
        lid_origin (Rhino.Geometry.Point3d): origin of the lid plane
        lid_normal (Rhino.Geometry.Vector3d): normal of lid plane
        body_radius (float): the radius of the body
        lid_ring_radius (float): the radius of the ring
        lid_ring_height (float): the height of the ring

    Return: 
        Rhino.Geometry.Brep: 3D model of the lid retention ring
    """
    try:
        print("INFO: create_toothpick_dispenser_lid_retention_ring - start", locals())
        # Create plane to locate the ring
        plane = rg.Plane(origin, normal)

        # Create the base circle at the bottom of the mug
        base_circle = rg.Circle(plane, radius)

        # Create cylinder with open bottom and top
        cylinder = rg.Cylinder(base_circle, height)
        cap_bottom = False
        cap_top = False
        ring = cylinder.ToBrep(cap_bottom, cap_top)

        print("INFO: create_toothpick_dispenser_lid_retention_ring - return", ring)
        return ring

    except Exception as error:
        print("ERROR: create_toothpick_dispenser_lid_retention_ring ", "An error occurred:", traceback.format_exc())
        return None


# Parameters
body_radius = 100
body_height = 200
body_origin = rg.Point3d(0,0,0)
body_normal = rg.Vector3d.ZAxis

lid_ring_distance_from_body = 2
lid_ring_radius = body_radius - lid_ring_distance_from_body
lid_ring_height = 10
lid_ring_origin = rg.Point3d(0,0,body_height-lid_ring_height)
lid_ring_normal = body_normal

# Assembling
toothpick_dispenser_lid_retention_ring = create_toothpick_dispenser_lid_retention_ring(lid_ring_origin, lid_ring_normal, lid_ring_radius, lid_ring_height)

# Return the created object by placing it in variable a
a = toothpick_dispenser_lid_retention_ring