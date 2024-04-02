"""
Car Body: A complex shape that resembles a rectangular prism with rounded corners and a semi-cylindrical top.
Parameters: body_length, body_width, body_height
Orientation: body_origin=(0,0,0), body_normal=ZAxis
"""
import Rhino
import Rhino.Geometry as rg
import traceback

TOLERANCE = Rhino.RhinoDoc.ActiveDoc.ModelAbsoluteTolerance

BASE_PLANE = rg.Plane.WorldXY
DEFAULT_BREP = rg.Brep.CreateFromSphere(rg.Sphere(BASE_PLANE,10))

def create_car_body(origin, normal, length, width, height):
    """
    This function creates a 3D model of a car body. 
    The body is modeled as a rectangular prism with rounded corners and a semi-cylindrical top.
    
    Parameters:
        origin (Rhino.Geometry.Point3d): origin of the car body plane
        normal (Rhino.Geometry.Vector3d): normal of car body plane 
        length (float): the length of the car body
        width (float): the width of the car body
        height (float): the height of the car body
    
    Return: 
    Rhino.Geometry.Brep: 3D model of the car body
    """
    try:
        print("INFO: create_car_body - start", locals())
        # Create plane to locate the body
        plane = rg.Plane(origin,normal)
        
        # Create the base rectangle
        base_box = rg.Box(plane,rg.Interval(-width/2,width/2),rg.Interval(-length/2,length/2),rg.Interval(0,height))
        base_brep = base_box.ToBrep()
        
        # Create the top semi-cylinder on perpendicular plane
        top_plane_origin = origin + rg.Vector3d(0,-length/2, height)
        top_plane_normal = normal.YAxis
        top_plane = rg.Plane(top_plane_origin,top_plane_normal)
        top_circle = rg.Circle(top_plane, width/2)
        top_cylinder = rg.Cylinder(top_circle, length)
        cap_bottom = True
        cap_top = True
        top_brep = top_cylinder.ToBrep(cap_bottom, cap_top)
        
        # Join the base and top to create the body
        body = rg.Brep.CreateBooleanUnion([base_brep, top_brep], TOLERANCE)
        print("INFO: create_car_body - return", body)
        return body
    except Exception as error:
        print("ERROR: create_car_body ", traceback.format_exc())
        return DEFAULT_BREP

# Parameters
body_length = 400
body_width = 200
body_height = 100
body_origin = rg.Point3d(0,0,0)
body_normal = rg.Vector3d.ZAxis

# Assembling
car_body = create_car_body(body_origin, body_normal, body_length, body_width, body_height)

# Return created object by placing it in variable a
a = car_body