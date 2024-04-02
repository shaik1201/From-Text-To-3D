import Rhino.Geometry as rg
import traceback

TOLERANCE = 0.01

def create_kettle_spout(origin, normal, height, bottom_radius, upper_radius):
    """
    This function creates a 3D model of a kettle spout. 
    The spout is modeled as a conical shape.
    
    Parameters:
        origin (Rhino.Geometry.Point3d): origin of the kettle spout plane
        normal (Rhino.Geometry.Vector3d): normal of kettle spout plane 
        height (float): the height of the spout 
        bottom_radius (float): the radius of the bottom of the spout
        upper_radius (float): the radius of the top of the spout
    
    Return: 
    Rhino.Geometry.Brep: 3D model of the spout
    """
    try:
        print("INFO: create_kettle_spout - start", locals())
        # Create plane to locate the spout
        plane = rg.Plane(origin,normal)
        
        # Create the base circle at the bottom of the spout
        base_circle = rg.Circle(plane, bottom_radius)
        
        # Create the top circle at the top of the spout
        top_plane = rg.Plane(plane)
        top_plane.Translate(plane.Normal*height)
        top_circle = rg.Circle(top_plane, upper_radius)
        
        # Create the spout by lofting the two circles
        closed=False
        spout = rg.Brep.CreateFromLoft([base_circle.ToNurbsCurve(), top_circle.ToNurbsCurve()], rg.Point3d.Unset, rg.Point3d.Unset, rg.LoftType.Normal, closed)[0]
        
        print("INFO: create_kettle_spout - return", spout)
        return spout
    except Exception as error:
        print("ERROR: create_kettle_spout ", "An error occurred:", traceback.format_exc())
        return None


# Parameters
body_bottom_radius = 150
body_upper_radius = 120
body_height = 200
body_origin = rg.Point3d(0,0,0)
body_normal = rg.Vector3d.ZAxis

spout_height = 100
spout_bottom_radius = 22
spout_upper_radius = 13
spout_relative_height = 0.6
spout_obliquity = 2.2
spout_origin = rg.Point3d(body_bottom_radius + (body_upper_radius-body_bottom_radius)*spout_relative_height,0,body_height * spout_relative_height)
spout_normal = rg.Vector3d(body_normal.XAxis + body_normal.ZAxis*spout_obliquity)

# Assembling
kettle_spout = create_kettle_spout(spout_origin, spout_normal, spout_height, spout_bottom_radius, spout_upper_radius)

# Return created object by placing it in variable a
a = kettle_spout