import Rhino.Geometry as rg
import traceback

TOLERANCE = 0.01

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

# Parameters
body_radius = 150
body_height = 50
body_normal = rg.Vector3d.ZAxis


rim_radius_inner = body_radius
rim_thickness = 10
rim_origin = rg.Point3d(0, 0, body_height)
rim_normal = body_normal

# Assembling
round_baking_mold_rim = create_round_baking_mold_rim(rim_origin, rim_normal, rim_radius_inner, rim_thickness)

# Return the created object by placing it in variable a
a = round_baking_mold_rim