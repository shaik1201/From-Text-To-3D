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


def create_baking_mold_base(origin, normal, width, length):
    """
    This function creates a 3D model of a baking mold base. 
    The base of the mold is modeled as a flat rectangle surface.

    Parameters:
        origin (Rhino.Geometry.Point3d): origin of the base plane
        normal (Rhino.Geometry.Vector3d): normal of base plane
        length (float): the length of the base
        width (float): the width of the base

    Return: 
        Rhino.Geometry.Brep: 3D model of the baking mold base
    """
    TOLERANCE = 0.01

    try:
        print("INFO: create_baking_mold_base - start", locals())
        # Create a plane to locate the base
        base_plane = rg.Plane(origin, normal)

        # Create the bottom of the base
        base_bottom_rectangle = rg.Rectangle3d(base_plane, rg.Interval(- length / 2, length / 2 ), rg.Interval(width / 2, - width / 2)).ToNurbsCurve()
        base_surface = rg.Brep.CreatePlanarBreps(base_bottom_rectangle, TOLERANCE)[0]

        print("INFO: create_baking_mold_base - return", base_surface)
        return base_surface

    except Exception as error:
        print("ERROR: create_baking_mold_base ", "An error occurred:", traceback.format_exc())
        return None


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


# User Parameters:
try:
    sliders_value = locals()['sliders_value']
    body_width = int(sliders_value['body_width'])
    body_length = int(sliders_value['body_length'])
    body_height = int(sliders_value['body_height'])
    rim_thickness_vertical = int(sliders_value['rim_thickness_vertical'])
    rim_thickness_horizontal = int(sliders_value['rim_thickness_horizontal'])

except:
    body_width = 230
    body_length = 280
    body_height = 50
    rim_thickness_vertical = 10
    rim_thickness_horizontal = 10

# Parameters
body_origin = rg.Point3d(0, 0, 0)
body_normal = rg.Vector3d.ZAxis

base_width = body_width
base_length = body_length
base_origin = body_origin
base_normal = body_normal.ZAxis

rim_origin = rg.Point3d(0, 0, body_height)
rim_normal = body_normal.ZAxis
rim_length_inner = body_length
rim_width_inner = body_width

# Assembling
baking_mold_body = create_baking_mold_body(body_origin, body_normal, body_length, body_width, body_height)
baking_mold_base = create_baking_mold_base(base_origin, base_normal, base_length, base_width)
baking_mold_rim = create_baking_mold_rim(rim_origin, rim_normal, rim_length_inner, rim_width_inner, rim_thickness_vertical, rim_thickness_horizontal)

# Return the created object by placing it in variable a
a = [baking_mold_body, baking_mold_base, baking_mold_rim]

# Return the parameters by placing them in variable b
b = {"body_width": [10, 800, body_width], "body_length": [10, 800, body_length],
     "body_height": [10, 300, body_height], "rim_thickness_vertical": [1, 50, rim_thickness_vertical],
     "rim_thickness_horizontal": [1, 50, rim_thickness_horizontal]}

