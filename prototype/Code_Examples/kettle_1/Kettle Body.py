import Rhino.Geometry as rg
import traceback

TOLERANCE = 0.01

def create_kettle_body(origin, normal, bottom_radius, upper_radius, height):
    """
    This function creates a 3D model of a kettle body. 
    The body is modeled as a truncated cone.
    
    Parameters:
        origin (Rhino.Geometry.Point3d): origin of the kettle body plane
        normal (Rhino.Geometry.Vector3d): normal of kettle body plane 
        bottom_radius (float): the radius of the bottom of the kettle 
        upper_radius (float): the radius of the upper part of the kettle 
        height (float): the height of the kettle
    
    Return: 
    Rhino.Geometry.Brep: 3D model of the kettle body
    """
    try:
        print("INFO: create_kettle_body - start", locals())
        # Create plane to locate the body
        plane = rg.Plane(origin,normal)
        
        # Create the base circle at the bottom of the kettle
        base_circle = rg.Circle(plane, bottom_radius).ToNurbsCurve()
        
        # Create the top circle at the top of the kettle
        top_plane = rg.Plane(origin + normal * height, normal)
        top_circle = rg.Circle(top_plane, upper_radius).ToNurbsCurve()
        
        # Create the kettle body by lofting the two circles
        closed = False
        kettle = rg.Brep.CreateFromLoft([base_circle, top_circle], rg.Point3d.Unset, rg.Point3d.Unset, rg.LoftType.Normal, closed)[0]
        
        print("INFO: create_kettle_body - return", kettle)
        return kettle
    except Exception as error:
        print("ERROR: create_kettle_body ", "An error occurred:", traceback.format_exc())
        return None

# Parameters
body_bottom_radius = 150
body_upper_radius = 120
body_height = 200
body_origin = rg.Point3d(0,0,0)
body_normal = rg.Vector3d.ZAxis

# Assembling
kettle_body = create_kettle_body(body_origin, body_normal, body_bottom_radius, body_upper_radius, body_height)

# Return created object by placing it in variable a
a = kettle_body