import rhinoinside
rhinoinside.load()
# System and Rhino can only be loaded after rhinoinside is initialized
import Rhino.Geometry as rg  # noqa
import Rhino
import traceback
import math

print('finished loading rhinoinside')
TOLERANCE = 0.01


def create_toothpick_dispenser_lid(origin, normal, radius, holes_radius, holes_amount, holes_distance_from_center):
    """
    This function creates a 3D model of a toothpick dispenser lid. 
    The lid is modeled as a perforated flat circular disk shape. The holes are modeled as cylinders.

    Parameters:
        origin (Rhino.Geometry.Point3d): origin of the lid plane
        normal (Rhino.Geometry.Vector3d): normal of lid plane
        radius (float): the radius of the lid
        holes_radius (float): the radius of the holes
        holes_amount (int): the number of holes in the lid
        holes_distance_from_center (flaot): the distance of the holes from the center of the lid

    Return: 
        Rhino.Geometry.Brep: 3D model of the lid
    """
    import math
    TOLERANCE = 0.01
    import clr
    clr.AddReference("System.Collections")
    from System.Collections.Generic import List

    try:
        print("INFO: create_toothpick_dispenser_lid - start", locals())
        # Create the plane to locate the lid
        plane = rg.Plane(origin, normal)

        # Create the lid
        lid = rg.Circle(plane, radius).ToNurbsCurve()
        lid = rg.Brep.CreatePlanarBreps(lid, TOLERANCE)[0]

        # Create the holes
        holes = []
        holesList = List[rg.Brep]()

        # Create the holes
        holes = []
        for i in range(int(holes_amount)):
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
        curveList.Add(lid)

        # Boolean difference to create the holes
        lid = rg.Brep.CreateBooleanDifference(curveList, holesList, TOLERANCE)[0]
        print("INFO: create_toothpick_dispenser_lid - return", lid)
        return lid

    except Exception as error:
        print("ERROR: create_toothpick_dispenser_lid ", "An error occurred:", traceback.format_exc())
        return None


# Parameters
body_radius = 50
body_height = 100
body_origin = rg.Point3d(0, 0, 0)
body_normal = rg.Vector3d.ZAxis

lid_radius = body_radius
lid_origin = rg.Point3d(0,0,body_height)
lid_normal = body_normal

holes_radius = 2
holes_amount = 6
holes_distance_from_center = 20

# Assembling
toothpick_dispenser_lid = create_toothpick_dispenser_lid(lid_origin, lid_normal, lid_radius, holes_radius, holes_amount, holes_distance_from_center)

# Return created object by placing it in variable a
a = toothpick_dispenser_lid