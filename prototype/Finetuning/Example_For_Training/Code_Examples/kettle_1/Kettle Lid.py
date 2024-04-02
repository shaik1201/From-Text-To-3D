import Rhino.Geometry as rg
import traceback

TOLERANCE = 0.01

def create_kettle_lid(origin, normal, radius, height):
    """
    This function creates a 3D model of a kettle lid. 
    The lid is modeled as a slightly domed circular piece.
    
    Parameters:
        origin (Rhino.Geometry.Point3d): origin of the kettle lid plane
        normal (Rhino.Geometry.Vector3d): normal of kettle lid plane 
        radius (float): the radius of the lid 
        height (float): the height of the lid
    
    Return: 
    Rhino.Geometry.Brep: 3D model of the lid
    """
    try:
        print("INFO: create_kettle_lid - start", locals())
        # Create plane to locate the lid
        plane = rg.Plane(origin,normal)
        
        # Create the base circle at the bottom of the lid
        base_circle = rg.Circle(plane, radius)
        
        # Create the top circle at the top of the lid
        top_plane = rg.Plane(plane)
        top_plane.Translate(plane.Normal*height)
        top_circle = rg.Circle(top_plane, radius * 0.1)
        
        # Create the lid by lofting the two circles
        closed = False
        lid = rg.Brep.CreateFromLoft([base_circle.ToNurbsCurve(), top_circle.ToNurbsCurve()], rg.Point3d.Unset, rg.Point3d.Unset, rg.LoftType.Normal, closed)[0]
        
        print("INFO: create_kettle_lid - return", lid)
        return lid
    except Exception as error:
        print("ERROR: create_kettle_lid ", "An error occurred:", traceback.format_exc())
        return None


# Parameters
body_bottom_radius = 150
body_upper_radius = 120
body_height = 200
body_normal = rg.Vector3d.ZAxis

rim_external_radius = body_upper_radius
rim_thickness = 35

lid_radius = rim_external_radius - rim_thickness + 5
lid_height = 20
lid_origin = rg.Point3d(0,0,body_height)
lid_normal = body_normal


# Assembling
kettle_lid = create_kettle_lid(lid_origin, lid_normal, lid_radius, lid_height)

# Return created object by placing it in variable a
a = kettle_lid