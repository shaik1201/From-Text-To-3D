import Rhino
import Rhino.Geometry as rg
import traceback

TOLERANCE = Rhino.RhinoDoc.ActiveDoc.ModelAbsoluteTolerance

def create_mug_body(origin, normal, radius, height):
    """
    This function creates a 3D model of a mug body. 
    The body is modeled as a cylinder.
    
    Parameters:
        origin (Rhino.Geometry.Point3d): origin of the mug body plane
        normal (Rhino.Geometry.Vector3d): normal of mug body plane 
        radius (float): the radius of the mug 
        height (float): the height of the mug
    
    Return: 
        Rhino.Geometry.Brep: 3D model of the mug body
    """
    try:
        print("INFO: create_mug_body - start", locals())
        # Create plane to locate the body
        plane = rg.Plane(origin,normal)
        
        # Create the base circle at the bottom of the mug
        base_circle = rg.Circle(plane, radius)
        cylinder = rg.Cylinder(base_circle, height)
        cap_bottom = False
        cap_top = False
        mug = cylinder.ToBrep(cap_bottom, cap_top)
        print("INFO: create_mug_body - return", mug)
        return mug
    except Exception as error:
        print("ERROR: create_mug_body ", traceback.format_exc())
        return None

def create_mug_base(origin, normal, radius):
    """
    This function creates a 3D model of a mug base. 
    The base is modeled as a circle at the base of the mug.

    Parameters:
        origin (Rhino.Geometry.Point3d): origin of the mug base plane
        normal (Rhino.Geometry.Vector3d): normal of mug base plane 
        radius (float): the radius of the base

    Return: 
        Rhino.Geometry.Circle: the created circle
    """
    try:
        print("INFO: create_mug_base - start", locals())
        # Create plane to locate the base
        plane = rg.Plane(origin, normal)

        # Create the base circle
        base_circle = rg.Circle(plane, radius).ToNurbsCurve()
        base = rg.Brep.CreatePlanarBreps(base_circle,TOLERANCE)[0]
        
        print("INFO: create_mug_base - return", base)
        return base
    except Exception as error:
        print("ERROR: create_mug_base ", "An error occurred:", traceback.format_exc())
        return None

def create_mug_handle(origin, normal, alignment, height, width, thickness):
    """
    Create a 3D model of a mug handle
    The handle is modeled as a slightly elongated semi-circle or crescent
    
    Parameters:
        origin (Rhino.Geometry.Point3d): origin of the handle - center of handle circle
        normal (Rhino.Geometry.Vector3d): normal of handle plane - tangent of handle
        alignmen (Rhino.Geometry.Vector3d): The direction to define the start and end point of the handle in relation to the origin
        height (float): the height of the handle
        width (float): The width of the handle
        thickness (float): The thickness of the handle
    
    Returns:
    Rhino.Geometry.Brep: The created semi cylinder
    """
    try:
        print("INFO: create_mug_handle - start", locals())
        # Create semi circle
        radius = width/2
        handle_start_point = origin + (alignment * radius)
        handle_end_point = origin - (alignment * radius)
        semi_circle = rg.Arc(handle_start_point, normal, handle_end_point).ToNurbsCurve()
        
        # Scale the semi-circle to create an elongated semi-circle or crescent
        plane = rg.Plane(origin,normal)
        transform = rg.Transform.Scale(plane, 1, height/radius, 1)
        semi_circle.Transform(transform)
        
        # Create a circle at the start of the semi-circle for the thickness
        start_point_plane = rg.Plane(semi_circle.PointAtStart ,semi_circle.TangentAtStart)
        shape_circle = rg.Circle(start_point_plane, thickness/2).ToNurbsCurve()
        
        # Sweep the shape circle along the semi-circle to create the handle
        closed = False
        handle = rg.Brep.CreateFromSweep(semi_circle, shape_circle, closed , TOLERANCE)[0]
        print("INFO: create_mug_handle - return", handle)
        return handle
    except Exception as error:
        print("ERROR: create_mug_handle ", "An error occurred:", traceback.format_exc())
        return None

# Generate input sliders by (name,value,min,max)
input_list = [
    InputSlider('body_radius', 50, 10, 300),
    InputSlider('body_height', 100, 10, 300),
    InputSlider('handle_height', 70, 10, 300),
    InputSlider('handle_width', 30, 10, 300),
    InputSlider('handle_thickness', 10, 5, 25),
    InputSlider('handle_relative_height', 0.50, 0.00, 1.00),
    ]
create_params(input_list)

# User Parameters:
try: body_radius
except: body_radius = 50

try: body_height
except: body_height = 100

try: handle_height
except: handle_height = 70

try: handle_width
except: handle_width = 30

try: handle_thickness
except: handle_thickness = 10

try: handle_relative_height
except: handle_relative_height = 0.5


# Internal Parameters:
body_origin = rg.Point3d(0,0,0)
body_normal = rg.Vector3d.ZAxis

base_radius = body_radius
base_origin = body_origin
base_normal = body_normal

handle_alignment = body_normal.ZAxis
handle_origin = rg.Point3d(body_radius,0, body_height * handle_relative_height)
handle_normal = body_normal.XAxis

# Assembling
mug_body = create_mug_body(body_origin, body_normal, body_radius, body_height)
mug_base = create_mug_base(base_origin, base_normal, base_radius)
mug_handle = create_mug_handle(handle_origin, handle_normal, handle_alignment, handle_height, handle_width, handle_thickness)

# Return created object by placing it in variable a
a = [mug_body,mug_base,mug_handle]