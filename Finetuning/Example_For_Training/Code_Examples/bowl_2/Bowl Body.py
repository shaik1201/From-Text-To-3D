import rhinoinside
rhinoinside.load()
import Rhino.Geometry as rg
import traceback

print('finished loading rhinoinside')
TOLERANCE = 0.01


def create_bowl_body(origin, normal, bottom_radius, top_radius, height):
    """
    This function creates a 3D model of a bowl body.
    The body is modeled as a conical or semi-spherical shape.

    Parameters:
        origin (Rhino.Geometry.Point3d): the origin of the bowl body plane
        normal (Rhino.Geometry.Vector3d): the normal of bowl body plane
        bottom_radius (float): the radius of the bottom of the bowl
        top_radius (float): the radius of the top of the bowl
        height (float): the height of the bowl

    Return:
        Rhino.Geometry.Brep: 3D model of the bowl body
    """
    import clr
    clr.AddReference("System.Collections")
    from System.Collections.Generic import List

    try:
        print("INFO: create_bowl_body - start", locals())
        # Create plane to locate the body
        plane = rg.Plane(origin, normal)

        # Create the base circle at the bottom of the bowl
        base_circle = rg.Circle(plane, bottom_radius).ToNurbsCurve()

        # Create the top circle at the top of the bowl
        top_plane = rg.Plane(origin + normal * height, normal)
        top_circle = rg.Circle(top_plane, top_radius).ToNurbsCurve()

        # Create a .NET list to hold the curves
        curveList = List[rg.Curve]()
        curveList.Add(base_circle)
        curveList.Add(top_circle)

        closed = False
        loft = rg.Brep.CreateFromLoft(curveList, rg.Point3d.Unset, rg.Point3d.Unset, rg.LoftType.Normal, closed)[0]

        print("INFO: create_bowl_body - return", loft)
        return loft

    except Exception as error:
        print("ERROR: create_bowl_body ", "An error occurred:", traceback.format_exc())
        return None


# Parameters
body_height = 80
body_bottom_radius = 100
body_top_radius = 125
body_origin = rg.Point3d(0, 0, 0)
body_normal = rg.Vector3d.ZAxis

# Assembling
bowl_body = create_bowl_body(body_origin, body_normal, body_bottom_radius, body_top_radius, body_height)

# Return the created object by placing it in variable a
a = bowl_body