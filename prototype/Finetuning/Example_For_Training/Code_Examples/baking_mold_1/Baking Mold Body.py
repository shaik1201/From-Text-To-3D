import rhinoinside
rhinoinside.load()
import Rhino.Geometry as rg
import traceback

print('finished loading rhinoinside')
TOLERANCE = 0.01


def create_baking_mold_body(origin, normal, width, length, height):
    """
    This function creates a 3D model of a baking mold body.
    The body of the mold is modeled as a hollow box.

    Parameters:
        origin (Rhino.Geometry.Point3d): origin of the body plane
        normal (Rhino.Geometry.Vector3d): normal of body plane
        length (float): the length of the body
        width (float): the width of the body
        height (float): the height of the body

    Return:
        Rhino.Geometry.Brep: 3D model of the baking mold body
    """
    import clr
    clr.AddReference("System.Collections")
    from System.Collections.Generic import List

    try:
        print("INFO: create_baking_mold_body - start", locals())
        # Create a plane to locate the body
        body_plane = rg.Plane(origin, normal)

        # Create the base of the body
        body_base_rectangle = rg.Rectangle3d(body_plane, rg.Interval(- length / 2, length / 2 ), rg.Interval(width / 2, - width / 2)).ToNurbsCurve()

        # Create the top rectangle of the body
        top_plane = rg.Plane(origin + normal * height, normal)
        body_top_rectangle = rg.Rectangle3d(top_plane,rg.Interval(- length / 2, length / 2 ), rg.Interval(width / 2, - width / 2)).ToNurbsCurve()

        # Create a .NET list to hold the curves
        curveList = List[rg.Curve]()
        curveList.Add(body_base_rectangle)
        curveList.Add(body_top_rectangle)

        closed = False
        loft = rg.Brep.CreateFromLoft(curveList, rg.Point3d.Unset, rg.Point3d.Unset, rg.LoftType.Normal, closed)[0]
        print("INFO: create_baking_mold_body - return", loft)
        return loft

    except Exception as error:
        print("ERROR: create_baking_mold_body ", "An error occurred:", traceback.format_exc())
        return None


# Parameters
body_width = 230
body_length = 280
body_height = 50
body_origin = rg.Point3d(0, 0, 0)
body_normal = rg.Vector3d.ZAxis

# Assembling
baking_mold_body = create_baking_mold_body(body_origin, body_normal, body_length, body_width, body_height)

# Return the created object by placing it in variable a
a = baking_mold_body