import Rhino
import Rhino.Geometry as rg
import traceback

TOLERANCE = Rhino.RhinoDoc.ActiveDoc.ModelAbsoluteTolerance

def create_round_baking_mold_body(origin, normal, height, radius):
    """
    This function creates a 3D model of a baking mold body. 
    The body of the mold is modeled as a hollow cylinder.

    Parameters:
        origin (Rhino.Geometry.Point3d): origin of the body plane
        normal (Rhino.Geometry.Vector3d): normal of body plane
        height (float): the height of the body
        radius (float): the radius of the body
    Return: 
        Rhino.Geometry.Brep: 3D model of the baking mold body
    """
    try:
        print("INFO: create_round_baking_mold_body - start", locals())
        # Create a plane to locate the body
        body_plane = rg.Plane(origin, normal)

        # Create the base circle of the body
        round_base = rg.Circle(body_plane, radius)

        # Create the cylinder that detrmine the body
        cylinder = rg.Cylinder(round_base, height)
        cap_bottom = False
        cap_top = False
        round_baking_mold_body = cylinder.ToBrep(cap_bottom, cap_top)

        print("INFO: create_round_baking_mold_body - return", round_baking_mold_body)
        return round_baking_mold_body
    except Exception as error:
        print("ERROR: create_round_baking_mold_body ", "An error occurred:", traceback.format_exc())
        return None

def create_round_baking_mold_base(origin, normal, radius):
    """
    This function creates a 3D model of a round baking mold base. 
    The round baking mold base is modeled as a flat surface in a circular shape at the bottom of the round baking mold.

    Parameters:
        origin (Rhino.Geometry.Point3d): the origin of the round baking mold base plane
        normal (Rhino.Geometry.Vector3d): the normal of the round baking mold base plane
        radius (float): the radius of the round baking mold base

    Return: 
        Rhino.Geometry.Brep: 3D model of the round baking mold base
    """
    try:
        print("INFO: round_baking_mold_base - start", locals())
        # Create a plane to locate the round baking mold base
        base_plane = rg.Plane(origin, normal)

        # Create the round baking mold base
        base_circle = rg.Circle(base_plane, radius).ToNurbsCurve()
        round_baking_mold_base = rg.Brep.CreatePlanarBreps(base_circle, TOLERANCE)[0]  

        print("INFO: round_baking_mold_base - return", round_baking_mold_base)
        return round_baking_mold_base
    except Exception as error:
        print("ERROR: round_baking_mold_base ", "An error occurred:", traceback.format_exc())
        return None

def create_round_baking_mold_rim(origin, normal, radius_inner, thickness):
    """
    This function creates a 3D model of a round baking mold rim. 
    The mold is modeled as an offset circular surface along the top edges of the mold.

    Parameters:
        origin (Rhino.Geometry.Point3d): origin of the molds rim plane
        normal (Rhino.Geometry.Vector3d): normal of molds rim plane
        radius_inner (float): the radius of the inner circle of the rim
        thickness (float): the thickness of the rim

    Return: 
        Rhino.Geometry.Brep: 3D model of the round baking mold rim
    """
    try:
        print("INFO: create_round_baking_mold_rim - start", locals())
        if thickness == 0: # No rim option
            return None
        # Create a plane to locate the rim
        rim_plane = rg.Plane(origin, normal)

        # Calculate the offset of the rim from the body 
        radius_outer = radius_inner + thickness

        # Create the inner circle of the rim
        inner_circle = rg.Circle(rim_plane, radius_inner).ToNurbsCurve()

        # Create the outer circle of the rim
        outer_circle = rg.Circle(rim_plane, radius_outer).ToNurbsCurve()
        
        # Create the rim by lofting the two circles
        closed = False
        curves = [inner_circle, outer_circle]
        loft = rg.Brep.CreateFromLoft(curves, rg.Point3d.Unset, rg.Point3d.Unset, rg.LoftType.Normal, closed)[0]
        
        print("INFO: create_round_baking_mold_rim - return", loft)
        return loft
    except Exception as error:
        print("ERROR: create_round_baking_mold_rim ", "An error occurred:", traceback.format_exc())
        return None

# Generate input sliders by (name,value,min,max)
input_list = [
    InputSlider('body_radius', 150, 10, 900),
    InputSlider('body_height', 50, 10, 300),
    InputSlider('rim_thickness', 10, 0, 50),
]
create_params(input_list)

# User Parameters:
try: body_radius
except: body_radius = 150

try: body_height
except: body_height = 50

try: rim_thickness
except: rim_thickness = 10

# Parameters
body_origin = rg.Point3d(0, 0, 0)
body_normal = rg.Vector3d.ZAxis

base_radius = body_radius
base_origin = body_origin 
base_normal = body_normal

rim_radius_inner = body_radius
rim_origin = rg.Point3d(0, 0, body_height)
rim_normal = body_normal

# Assembling
round_baking_mold_body = create_round_baking_mold_body(body_origin, body_normal, body_height, body_radius)
round_baking_mold_base = create_round_baking_mold_base(base_origin, base_normal, base_radius)
round_baking_mold_rim = create_round_baking_mold_rim(rim_origin, rim_normal, rim_radius_inner, rim_thickness)

# Return the created object by placing it in variable a
a = [round_baking_mold_body, round_baking_mold_base, round_baking_mold_rim]