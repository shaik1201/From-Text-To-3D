import Rhino.Geometry as rg
import traceback

TOLERANCE = 0.01

def create_kettle_rim(origin, normal, external_radius, thickness):
    """
    This function creates a 3D model of a kettle rim. 
    The rim is modeled as a surface between 2 circles.
    
    Parameters:
        origin (Rhino.Geometry.Point3d): origin of the kettle rim plane
        normal (Rhino.Geometry.Vector3d): normal of kettle rim plane 
        external_radius (float): the external radius of the torus
        thickness (float): the thickness of the torus
    
    Return: 
        Rhino.Geometry.Brep: 3D model of the rim
    """
    try:
        print("INFO: create_kettle_rim - start", locals())
        # Create plane to locate the rim
        plane = rg.Plane(origin,normal)
        
        # Create the rim surface
        external_circle = rg.Circle(plane,external_radius)
        internal_radius = external_radius - thickness
        internal_circle = rg.Circle(plane, internal_radius)
        
        # Create the lid by lofting the two circles
        closed = False
        rim = rg.Brep.CreateFromLoft([external_circle.ToNurbsCurve(), internal_circle.ToNurbsCurve()], rg.Point3d.Unset, rg.Point3d.Unset, rg.LoftType.Normal, closed)[0]
        
        print("INFO: create_kettle_rim - return", rim)
        return rim
    except Exception as error:
        print("ERROR: create_kettle_rim ", "An error occurred:", traceback.format_exc())
        return None


# Parameters
body_upper_radius = 120
body_height = 200
body_origin = rg.Point3d(0,0,0)
body_normal = rg.Vector3d.ZAxis

rim_external_radius = body_upper_radius
rim_thickness = 35
rim_origin = rg.Point3d(0,0,body_height)
rim_normal = body_normal

# Assembling
kettle_rim = create_kettle_rim(rim_origin, rim_normal, rim_external_radius, rim_thickness)

# Return created object by placing it in variable a
a = kettle_rim