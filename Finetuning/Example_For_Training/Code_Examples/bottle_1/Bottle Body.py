import rhinoinside
rhinoinside.load()
import Rhino.Geometry as rg
import traceback

print('finished loading rhinoinside')
TOLERANCE = 0.01


def create_bottle_body(origin, normal, bottom_radius, bottom_height, neck_radius, neck_height):
    """
    This function creates a 3D model of a bottle body.
    The body is modeled as a cylinder that becomes narrow in its neck.

    Parameters:
        origin (Rhino.Geometry.Point3d): origin of the bottle body plane
        normal (Rhino.Geometry.Vector3d): normal of bottle body plane
        bottom_radius (float): the radius of the bottom of the bottle
        bottom_height (float): the height of the bottle body
        neck_radius (float): the radius of the neck of the bottle
        neck_height (float): the height of the neck of the bottle

    Return:
        Rhino.Geometry.Brep: 3D model of the bottle body
    """
    import clr
    clr.AddReference("System.Collections")
    from System.Collections.Generic import List

    try:
        print("INFO: create_bottle_body - start", locals())
        # Create plane to locate the body
        plane = rg.Plane(origin, normal)

        # Create the base surface of the bottle
        bottom_start_circle = rg.Circle(plane, bottom_radius).ToNurbsCurve()
        bottom_mid_plane = rg.Plane(plane)
        bottom_mid_plane.Translate(plane.ZAxis * (bottom_height / 2))
        bottom_mid_circle = rg.Circle(bottom_mid_plane, bottom_radius).ToNurbsCurve()
        bottom_end_plane = rg.Plane(plane)
        bottom_end_plane.Translate(plane.ZAxis * (bottom_height * 0.9))
        bottom_end_circle = rg.Circle(bottom_end_plane, bottom_radius).ToNurbsCurve()

        # Create the neck of the bottle
        neck_start_plane = rg.Plane(plane)
        neck_start_plane.Translate(plane.ZAxis * (bottom_height * 1.1))
        neck_start_circle = rg.Circle(neck_start_plane, neck_radius).ToNurbsCurve()
        neck_mid_plane = rg.Plane(plane)
        neck_mid_plane.Translate(plane.ZAxis * (bottom_height + (neck_height / 2)))
        neck_mid_circle = rg.Circle(neck_mid_plane, neck_radius).ToNurbsCurve()
        neck_end_plane = rg.Plane(plane)
        neck_end_plane.Translate(plane.ZAxis * (bottom_height + neck_height))
        neck_end_circle = rg.Circle(neck_end_plane, neck_radius).ToNurbsCurve()

        # Create a .NET list to hold the curves
        curveList = List[rg.Curve]()
        curveList.Add(bottom_start_circle)
        curveList.Add(bottom_mid_circle)
        curveList.Add(bottom_end_circle)
        curveList.Add(neck_start_circle)
        curveList.Add(neck_mid_circle)
        curveList.Add(neck_end_circle)

        closed = False
        bottle = rg.Brep.CreateFromLoft(curveList, rg.Point3d.Unset, rg.Point3d.Unset, rg.LoftType.Normal, closed)[0]

        print("INFO: create_bottle_body - return", bottle)
        return bottle

    except Exception as error:
        print("ERROR: create_bottle_body ", "An error occurred:", traceback.format_exc())
        return None


# Parameters
body_bottom_radius = 40
body_bottom_part_height = 140
body_neck_radius = 25
body_neck_height = 70
body_origin = rg.Point3d(0, 0, 0)
body_normal = rg.Vector3d.ZAxis

# Assembling
bottle_body = create_bottle_body(body_origin, body_normal, body_bottom_radius, body_bottom_part_height, body_neck_radius, body_neck_height)

# Return created object by placing it in variable a
a = bottle_body