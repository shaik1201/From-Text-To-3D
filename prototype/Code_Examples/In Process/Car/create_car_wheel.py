"""
Car Wheels: Four cylindrical shapes, attached on the bottom corners of the car body.
Parameters: wheel_radius, wheel_thickness, wheel_distance_from_corner
Front Right Wheel Orientation: fr_wheel_origin=(body_width/2, body_length/2, 0), fr_wheel_normal=XAxis
Front Left Wheel Orientation: fl_wheel_origin=(-body_width/2, body_length/2, 0), fl_wheel_normal=-XAxis
Rear Right Wheel Orientation: rr_wheel_origin=(body_width/2, -body_length/2, 0), rr_wheel_normal=XAxis
Rear Left Wheel Orientation: rl_wheel_origin=(-body_width/2, -body_length/2, 0), rl_wheel_normal=-XAxis
"""
import Rhino
import Rhino.Geometry as rg
import traceback

TOLERANCE = Rhino.RhinoDoc.ActiveDoc.ModelAbsoluteTolerance

BASE_PLANE = rg.Plane.WorldXY
DEFAULT_BREP = rg.Brep.CreateFromSphere(rg.Sphere(BASE_PLANE,10))

def create_car_wheel(origin, normal, radius, thickness):
    """
    This function creates a 3D model of a car wheel. 
    The wheel is modeled as a cylinder.
    
    Parameters:
        origin (Rhino.Geometry.Point3d): origin of the wheel plane
        normal (Rhino.Geometry.Vector3d): normal of wheel plane 
        radius (float): the radius of the wheel 
        thickness (float): the thickness of the wheel
    
    Return: 
    Rhino.Geometry.Brep: 3D model of the wheel
    """
    try:
        print("INFO: create_car_wheel - start", locals())
        # Create plane to locate the wheel
        plane = rg.Plane(origin,normal)
        
        # Create the base circle at the bottom of the wheel
        base_circle = rg.Circle(plane, radius)
        cylinder = rg.Cylinder(base_circle, thickness)
        cap_bottom = True
        cap_top = True
        wheel = cylinder.ToBrep(cap_bottom, cap_top)
        print("INFO: create_car_wheel - return", wheel)
        return wheel
    except Exception as error:
        print("ERROR: create_car_wheel ", traceback.format_exc())
        return DEFAULT_BREP

# Parameters
body_width = 200
body_length = 400
body_origin = rg.Point3d(0,0,0)
body_normal = rg.Vector3d.ZAxis

wheel_radius = 50
wheel_thickness = 30
fr_wheel_origin = rg.Point3d(body_width/2, body_length/2, -wheel_radius)
fr_wheel_normal = rg.Vector3d(body_normal.XAxis)
fl_wheel_origin = rg.Point3d(-body_width/2, body_length/2, -wheel_radius)
fl_wheel_normal = rg.Vector3d(-body_normal.XAxis)
rr_wheel_origin = rg.Point3d(body_width/2, -body_length/2, -wheel_radius)
rr_wheel_normal = rg.Vector3d(body_normal.XAxis)
rl_wheel_origin = rg.Point3d(-body_width/2, -body_length/2, -wheel_radius)
rl_wheel_normal = rg.Vector3d(-body_normal.XAxis)

# Assembling
car_fr_wheel = create_car_wheel(fr_wheel_origin, fr_wheel_normal, wheel_radius, wheel_thickness)
car_fl_wheel = create_car_wheel(fl_wheel_origin, fl_wheel_normal, wheel_radius, wheel_thickness)
car_rr_wheel = create_car_wheel(rr_wheel_origin, rr_wheel_normal, wheel_radius, wheel_thickness)
car_rl_wheel = create_car_wheel(rl_wheel_origin, rl_wheel_normal, wheel_radius, wheel_thickness)

# Return created object by placing it in variable a
a = car_fr_wheel, car_fl_wheel, car_rr_wheel, car_rl_wheel