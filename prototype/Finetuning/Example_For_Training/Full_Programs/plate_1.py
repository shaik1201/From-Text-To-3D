import rhinoinside
rhinoinside.load()
import Rhino.Geometry as rg
import traceback

print('finished loading rhinoinside')
TOLERANCE = 0.01


def create_plate_body(body_origin, body_normal, body_bottom_radius, body_top_radius, body_height):
    """
    This function creates a 3D model of a plate body. 
    The plate body is modeled as sloping sides that extend upward from the base

    Parameters:
        body_origin (Rhino.Geometry.Point3d): the origin of the plate body plane
        body_normal (Rhino.Geometry.Vector3d): the normal of plate body plane
        body_bottom_radius (float): the radius of the base of the plate body
        body_top_radius (float): the radius of the top of the plate body
        body_height (float): the plate's body height

    Return: 
        Rhino.Geometry.Brep: 3D model of the plate body
    """
    import clr
    clr.AddReference("System.Collections")
    from System.Collections.Generic import List

    try:
        print("INFO: create_plate_body - start", locals())
        # Create plane to locate the plate body
        body_plane = rg.Plane(body_origin, body_normal)

        # Create the bottom part of the body
        body_bottom_circle = rg.Circle(body_plane, body_bottom_radius).ToNurbsCurve()

        # Create the top part of the plate body
        body_top_plane = rg.Plane(body_origin + body_normal * body_height, body_normal)
        body_top_circle = rg.Circle(body_top_plane, body_top_radius).ToNurbsCurve()

        # Create a .NET list to hold the curves
        curveList = List[rg.Curve]()
        curveList.Add(body_bottom_circle)
        curveList.Add(body_top_circle)

        closed = False
        loft = rg.Brep.CreateFromLoft(curveList, rg.Point3d.Unset, rg.Point3d.Unset, rg.LoftType.Normal, closed)[0]

        print("INFO: create_plate_body - return", loft)
        return loft

    except Exception as error:
        print("ERROR: create_plate_body ", "An error occurred:", traceback.format_exc())
        return None


def create_plate_base(origin, normal, base_radius):
    """
    This function creates a 3D model of a plate base. 
    The plate base is modeled as a flat surface in a circle shape at the bottom of the plate.

    Parameters:
        base_origin (Rhino.Geometry.Point3d): the origin of the plate base plane
        base_normal (Rhino.Geometry.Vector3d): the normal of the plate base plane
        base_radius (float): the radius of the plate base

    Return: 
        Rhino.Geometry.Brep: 3D model of the plate
    """
    TOLERANCE = 0.01

    try:
        print("INFO: create_plate_base - start", locals())
        # Create a plane to locate the plate base
        base_plane = rg.Plane(origin, normal)

        # Create the plate base
        base_circle = rg.Circle(base_plane, base_radius).ToNurbsCurve()
        plate_base = rg.Brep.CreatePlanarBreps(base_circle, TOLERANCE)[0]  

        print("INFO: create_plate_base - return", plate_base)
        return plate_base

    except Exception as error:
        print("ERROR: create_plate_base ", "An error occurred:", traceback.format_exc())
        return None


try:
    sliders_value = locals()['sliders_value']
    body_bottom_radius = int(sliders_value['body_bottom_radius'])
    body_top_radius = int(sliders_value['body_top_radius'])
    body_height = int(sliders_value['body_height'])

except:
    # If conversion to int fails, set defaults
    body_bottom_radius = 100
    body_top_radius = 140
    body_height = 21

# Internal Parameters:
body_origin = rg.Point3d(0, 0, 0)
body_normal = rg.Vector3d.ZAxis

base_radius = body_bottom_radius
base_origin = body_origin
base_normal = body_normal

# Assembling
plate_body = create_plate_body(body_origin, body_normal, body_bottom_radius, body_top_radius, body_height)
plate_base = create_plate_base(base_origin, base_normal, base_radius)

# Return the created objects by placing them in variable a
a = [plate_base, plate_body]

# Return the parameters by placing them in variable b
b = {"body_bottom_radius": [10, 300, body_bottom_radius],
     "body_top_radius": [10, 300, body_top_radius],
     "body_height": [10, 100, body_height]}
