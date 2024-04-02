import Rhino.Geometry as rg
import traceback

TOLERANCE = 0.01

def create_kettle_lid_handle(origin, normal, radius):
    """
    This function creates a 3D model of a kettle lid handle. 
    The handle is modeled as a semi-sphere.
    
    Parameters:
        origin (Rhino.Geometry.Point3d): origin of the kettle lid handle plane
        normal (Rhino.Geometry.Vector3d): normal of kettle lid handle plane 
        radius (float): the radius of the semi-sphere
    
    Return: 
        Rhino.Geometry.Brep: 3D model of the handle
    """
    try:
        print("INFO: create_kettle_lid_handle - start", locals())
        # Create plane to locate the handle
        plane = rg.Plane(origin,normal)
        
        # Create the sphere
        sphere = rg.Sphere(plane, radius)
        brep_sphere = rg.Brep.CreateFromSphere(sphere)
        
        # Create a cutting brep
        interval = rg.Interval(-radius,radius)
        cutting_brep = rg.PlaneSurface(plane,interval,interval).ToBrep()
        split_breps = brep_sphere.Split(cutting_brep, TOLERANCE)
        semi_sphere = [brep for brep in split_breps if brep.IsValid][0]
        
        print("INFO: create_kettle_lid_handle - return", brep_sphere)
        return semi_sphere
    except Exception as error:
        print("ERROR: create_kettle_lid_handle ", "An error occurred:", traceback.format_exc())
        return None


# Parameters
body_upper_radius = 120
body_height = 200
body_origin = rg.Point3d(0,0,0)
body_normal = rg.Vector3d.ZAxis

rim_external_radius = body_upper_radius
rim_thickness = 35

lid_radius = rim_external_radius - rim_thickness + 5
lid_height = 20
lid_origin = rg.Point3d(0,0,body_height)
lid_normal = body_normal

lid_handle_radius = 9
lid_handle_origin = rg.Point3d(0,0,body_height+lid_height)
lid_handle_normal = lid_normal

# Assembling
kettle_lid_handle = create_kettle_lid_handle(lid_handle_origin, lid_normal, lid_handle_radius)

# Return created object by placing it in variable a
a = kettle_lid_handle