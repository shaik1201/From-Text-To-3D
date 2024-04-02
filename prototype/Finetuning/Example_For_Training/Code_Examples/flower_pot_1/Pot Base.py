import rhinoinside
rhinoinside.load()
import Rhino.Geometry as rg
import traceback
import math

print('finished loading rhinoinside')
TOLERANCE = 0.01


def create_pot_base(origin, normal, base_radius, holes_radius, holes_amount, holes_distance_from_center):
    """
    This function creates a 3D model of a pot base.
    The base is modeled as a perforated flat surface in circle shape at the bottom of the pot.
    The holes are located in a circle around the center of the surface.

    Parameters:
        origin (Rhino.Geometry.Point3d): origin of the pot base plane
        normal (Rhino.Geometry.Vector3d): normal of pot base plane
        base_radius (float): the radius of the base
        holes_radius (float): the radius of the holes
        holes_amount (int): the amount of holes in the base
        holes_distance_from_center (float): the distance of the holes from the center of the base

    Return:
        Rhino.Geometry.Brep: 3D model of the pot base
    """
    import clr
    clr.AddReference("System.Collections")
    from System.Collections.Generic import List
    import math

    TOLERANCE = 0.01

    try:
        print("INFO: create_pot_base - start", locals())
        # Create plane to locate the base
        plane = rg.Plane(origin, normal)

        # Create the base
        base_circle = rg.Circle(plane, base_radius)
        base = rg.Brep.CreatePlanarBreps(base_circle.ToNurbsCurve(), TOLERANCE)[0]

        # Create the holes
        holes = []
        holesList = List[rg.Brep]()

        for i in range(holes_amount):
            angle = i * (2 * math.pi / holes_amount)
            x = holes_distance_from_center * math.cos(angle)
            y = holes_distance_from_center * math.sin(angle)
            hole_origin = plane.PointAt(x, y)
            hole_normal = plane.Normal
            hole_plane = rg.Plane(hole_origin, hole_normal)
            hole = rg.Circle(hole_plane, holes_radius).ToNurbsCurve()
            hole = rg.Brep.CreatePlanarBreps(hole, TOLERANCE)[0]
            holes.append(hole)
            holesList.Add(hole)

        # Subtract the holes from the base
        curveList = List[rg.Brep]()
        curveList.Add(base)

        res = rg.Brep.CreateBooleanDifference(curveList, holesList, TOLERANCE)[0]

        print("INFO: create_pot_base - return", res)
        return res
    except Exception as error:
        print("ERROR: create_pot_base ", "An error occurred:", traceback.format_exc())
        return None


# Parameters
body_bottom_radius = 150
body_origin = rg.Point3d(0, 0, 0)
body_normal = rg.Vector3d.ZAxis

base_radius = body_bottom_radius
holes_radius = 10
holes_amount = 4
holes_distance_from_center = 40
base_origin = body_origin
base_normal = body_normal

# Assembling
pot_base = create_pot_base(base_origin, base_normal, base_radius, holes_radius, holes_amount, holes_distance_from_center)

# Return created object by placing it in variable a
a = pot_base