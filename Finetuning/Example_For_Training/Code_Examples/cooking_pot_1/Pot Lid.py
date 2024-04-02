import Rhino.Geometry as rg
import traceback

TOLERANCE = 0.01

def create_pot_lid(origin, normal, bottom_radius, height, top_radius):
    """
    This function creates a 3D model of a pot lid. 
    The lid is modeled as a slightly domed circular piece.
    
    Parameters:
        origin (Rhino.Geometry.Point3d): origin of the pot lid plane
        normal (Rhino.Geometry.Vector3d): normal of pot lid plane 
        bottom_radius (float): the bottom radius of the lid 
        height (float): the height of the lid
        top_radius (float): the top radius of the lid
    
    Return: 
    Rhino.Geometry.Brep: 3D model of the lid
    """
    try:
        print("INFO: create_pot_lid - start", locals())
        # Create plane to locate the lid
        plane = rg.Plane(origin,normal)
        
        # Create the base circle at the bottom of the lid
        base_circle = rg.Circle(plane, bottom_radius).ToNurbsCurve()
        
        # Create the top circle at the top of the lid
        top_plane = rg.Plane(plane)
        top_plane.Translate(plane.Normal*height)
        top_circle = rg.Circle(top_plane, top_radius).ToNurbsCurve()
        
        # Create the lid by lofting the two circles
        closed = False
        lid = rg.Brep.CreateFromLoft([base_circle, top_circle], rg.Point3d.Unset, rg.Point3d.Unset, rg.LoftType.Normal, closed)[0]
        
        print("INFO: create_pot_lid - return", lid)
        return lid
    except Exception as error:
        print("ERROR: create_pot_lid", "An error occurred:", traceback.format_exc())
        return None


# Parameters
body_height = 130
body_normal = rg.Vector3d.ZAxis

lid_handle_radius = 10

lid_bottom_radius = 145
lid_top_radius = lid_handle_radius
lid_height = 30
lid_origin = rg.Point3d(0,0,body_height)
lid_normal = body_normal


# Assembling
pot_lid = create_pot_lid(lid_origin, lid_normal, lid_bottom_radius, lid_height, lid_top_radius)

# Return created object by placing it in variable a
a = pot_lid