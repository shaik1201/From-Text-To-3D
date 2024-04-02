import rhinoinside
rhinoinside.load()
import Rhino.Geometry as rg
import traceback

print('finished loading rhinoinside')
TOLERANCE = 0.01


def create_baking_mold_rim(origin, normal, length_inner, width_inner, thickness_vertical, thickness_horizontal):
    """
    This function creates a 3D model of a baking mold. 
    The mold is modeled as an open box with edges.

    Parameters:
        origin (Rhino.Geometry.Point3d): origin of the molds rim plane
        normal (Rhino.Geometry.Vector3d): normal of molds rim plane
        length_inner (float): the length of the inner rectangle of the rim
        width_inner (float): the width of the inner rectangle of the rim
        height (float): the height of the molds rim
        thickness_vertical (float): the length of the outer rectangle of the rim
        thickness_horizontal (float): : the width of the outer rectangle of the rim

    Return: 
        Rhino.Geometry.Brep: 3D model of the baking mold rim
    """
    import clr
    clr.AddReference("System.Collections")
    from System.Collections.Generic import List

    try:
        print("INFO: create_baking_mold_rim - start", locals())
        if thickness_vertical == 0 and thickness_horizontal == 0: # No rim option
            return None
        # Create a plane to locate the rim
        rim_plane = rg.Plane(origin, normal)

        # Create the inner rectangle of the rim - the top rectangle of the body
        rim_inner_rectangle = rg.Rectangle3d(rim_plane, rg.Interval(width_inner / 2, - width_inner / 2), rg.Interval(- length_inner / 2, length_inner / 2 )).ToNurbsCurve()

        # Create the rim by adding an outer rectangle - the rim thickness
        length_outer = length_inner + thickness_vertical
        width_outer = width_inner + thickness_horizontal
        rim_outer_rectangle = rg.Rectangle3d(rim_plane, rg.Interval(width_outer / 2, - width_outer / 2), rg.Interval(- length_outer / 2, length_outer / 2 )).ToNurbsCurve()

        # Create a .NET list to hold the curves
        curveList = List[rg.Curve]()
        curveList.Add(rim_inner_rectangle)
        curveList.Add(rim_outer_rectangle)

        closed = False
        loft = rg.Brep.CreateFromLoft(curveList, rg.Point3d.Unset, rg.Point3d.Unset, rg.LoftType.Normal, closed)[0]

        print("INFO: create_baking_mold_rim - return", loft)
        return loft

    except Exception as error:
        print("ERROR: create_baking_mold_rim ", "An error occurred:", traceback.format_exc())
        return None


# Parameters
body_width = 230
body_length = 280
body_height = 50
body_normal = rg.Vector3d.ZAxis

rim_origin = rg.Point3d(0, 0, body_height)
rim_normal = body_normal.ZAxis
rim_length_inner = body_length
rim_width_inner = body_width
rim_thickness_vertical = 10
rim_thickness_horizontal = 10

# Assembling
baking_mold_rim = create_baking_mold_rim(rim_origin, rim_normal, rim_length_inner, rim_width_inner, rim_thickness_vertical, rim_thickness_horizontal)

# Return the created object by placing it in variable a
a = baking_mold_rim