import Rhino
import Rhino.Geometry as rg
import traceback

TOLERANCE = Rhino.RhinoDoc.ActiveDoc.ModelAbsoluteTolerance

def create_bowl_body(origin, normal, bottom_radius, middle_radius, upper_radius, height):
    """
    This function creates a 3D model of a bowl body. 
    The body is modeled as a truncated cone.

    Parameters:
        origin (Rhino.Geometry.Point3d): origin of the bowl body plane
        normal (Rhino.Geometry.Vector3d): normal of bowl body plane 
        bottom_radius (float): the radius of the bottom of the bowl 
        middle_radius (float): the radius of the middle part of the bowl
        upper_radius (float): the radius of the upper part of the bowl
        height (float): the height of the bowl

    Return: 
        Rhino.Geometry.Brep: 3D model of the bowl body
    """
    try:
        print("INFO: create_bowl_body - start", locals())
        # Create plane to locate the body
        plane = rg.Plane(origin, normal)

        # Create the base circle at the bottom of the bowl
        base_circle = rg.Circle(plane, bottom_radius).ToNurbsCurve()

        # Create circle at the middle of the bowl
        mid_plane = rg.Plane(origin + normal * height/2, normal)
        mid_circle = rg.Circle(mid_plane, middle_radius).ToNurbsCurve()

        # Create the top circle at the top of the bowl
        top_plane = rg.Plane(origin + normal * height, normal)
        top_circle = rg.Circle(top_plane, upper_radius).ToNurbsCurve()

        # Create the bowl by lofting the circles
        closed = False
        bowl = rg.Brep.CreateFromLoft([base_circle, mid_circle, top_circle], rg.Point3d.Unset, rg.Point3d.Unset, rg.LoftType.Normal, closed)[0]

        print("INFO: create_bowl_body - return", bowl)
        return bowl
    except Exception as error:
        print("ERROR: create_bowl_body ", "An error occurred:", traceback.format_exc())
        return None

def create_bowl_base(origin, normal, radius):
    """
    This function creates a 3D model of a bowl base. 
    The base is modeled as a circle at the bottom of the bowl.

    Parameters:
        origin (Rhino.Geometry.Point3d): origin of the bowl base plane
        normal (Rhino.Geometry.Vector3d): normal of bowl base plane 
        radius (float): the radius of the base

    Return: 
        Rhino.Geometry.Brep: the created base
    """
    try:
        print("INFO: create_bowl_base - start", locals())
        # Create plane to locate the base
        plane = rg.Plane(origin, normal)

        # Create the base circle
        base_circle = rg.Circle(plane, radius).ToNurbsCurve()
        base = rg.Brep.CreatePlanarBreps(base_circle,TOLERANCE)[0]
        
        print("INFO: create_bowl_base - return", base)
        return base
    except Exception as error:
        print("ERROR: create_bowl_base ", "An error occurred:", traceback.format_exc())
        return None

# Generate input sliders by (name,value,min,max)
input_list = [
    InputSlider('body_height', 90, 0, 300),
    InputSlider('body_bottom_radius', 30, 0, 300),
    InputSlider('body_middle_radius', 110, 0, 300),
    InputSlider('body_upper_radius', 140, 0, 300),
    ]
create_params(input_list)

# User Parameters:
try: body_height 
except: body_height = 90

try: body_bottom_radius 
except: body_bottom_radius = 30

try: body_middle_radius
except: body_middle_radius = 110

try: body_upper_radius
except: body_upper_radius = 140

# Internal Parameters:
body_origin = rg.Point3d(0, 0, 0)
body_normal = rg.Vector3d.ZAxis

base_radius = body_bottom_radius
base_origin = body_origin
base_normal = body_normal

# Assembling
bowl_body = create_bowl_body(body_origin, body_normal, body_bottom_radius, body_middle_radius, body_upper_radius, body_height)
bowl_base = create_bowl_base(base_origin, base_normal, base_radius)

# Return created object by placing it in variable a
a = [bowl_body,bowl_base]