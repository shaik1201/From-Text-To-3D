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
        plane = rg.Plane(origin,normal)
        
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
        plane = rg.Plane(origin,normal)
        
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


try:
    sliders_value = locals()['sliders_value']
    body_radius = int(sliders_value['body_radius'])
    body_height = int(sliders_value['body_height'])
    lid_ring_distance_from_body = int(sliders_value['lid_ring_distance_from_body'])
    lid_ring_height = int(sliders_value['lid_ring_height'])
    holes_radius = int(sliders_value['holes_radius'])
    holes_amount = int(sliders_value['holes_amount'])
    holes_distance_from_center = int(sliders_value['holes_distance_from_center'])

except:
    body_radius = 50
    body_height = 100
    lid_ring_distance_from_body = 2
    lid_ring_height = 10
    holes_radius = 2
    holes_amount = 6
    holes_distance_from_center = 20


# Internal Parameters:
body_origin = rg.Point3d(0, 0, 0)
body_normal = rg.Vector3d.ZAxis

base_radius = body_radius
base_origin = body_origin
base_normal = body_normal

lid_radius = body_radius
lid_origin = rg.Point3d(0,0,body_height)
lid_normal = body_normal

lid_ring_radius = body_radius - lid_ring_distance_from_body
lid_ring_origin = rg.Point3d(0,0,body_height-lid_ring_height)
lid_ring_normal = body_normal

# Assembling
toothpick_dispenser_base = create_toothpick_dispenser_base(base_origin, base_normal, base_radius)
toothpick_dispenser_body = create_toothpick_dispenser_body(body_origin, body_normal, body_radius, body_height)
toothpick_dispenser_lid = create_toothpick_dispenser_lid(lid_origin, lid_normal, lid_radius, holes_radius, holes_amount, holes_distance_from_center)
toothpick_dispenser_lid_retention_ring = create_toothpick_dispenser_lid_retention_ring(lid_ring_origin, lid_ring_normal, lid_ring_radius, lid_ring_height)

# Return the created objects by placing them in variable a
a = [toothpick_dispenser_base, toothpick_dispenser_body, toothpick_dispenser_lid, toothpick_dispenser_lid_retention_ring]

# Return the parameters by placing them in variable b
b = {"body_radius": [10, 300, body_radius], "body_height": [10, 300, body_height],
     "lid_ring_distance_from_body": [0, 50, lid_ring_distance_from_body],
     "lid_ring_height": [1, 50, lid_ring_height], "holes_radius": [1, 20, holes_radius],
     "holes_amount": [3, 12, holes_amount], "holes_distance_from_center": [10, 100, holes_distance_from_center]}
