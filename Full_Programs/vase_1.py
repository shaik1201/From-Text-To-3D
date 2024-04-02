import Rhino
import Rhino.Geometry as rg
import traceback

TOLERANCE = Rhino.RhinoDoc.ActiveDoc.ModelAbsoluteTolerance

def create_vase_body(origin, normal, height, bottom_radius, wider_radius, widening_relative_height, neck_radius, neck_relative_height):
    """
    This function creates a 3D model of a vase body. 
    The body is modeled as a curved cylinder tapering into a narrow cylinder

    Parameters:
        origin (Rhino.Geometry.Point3d): origin of the vase body plane
        normal (Rhino.Geometry.Vector3d): normal of vase body plane
        height (float): the height of the vase
        bottom_radius (float): the radius of the vase at its bottom
        wider_radius (float): the radius of the vase at its widest part
        widening_relative_height (float): the relative height at which the vase is the widest
        neck_radius (float): the radius of the vase neck
        neck_relative_height (float): the relative height at which the neck of the vase starts

    Return: 
        Rhino.Geometry.Brep: 3D model of the vase body
    """
    try:
        print("INFO: create_vase_body - start", locals())
        # Create plane to locate the vase
        plane = rg.Plane(origin, normal)

        # Create the base circle at the bottom of the vase
        base_circle = rg.Circle(plane, bottom_radius).ToNurbsCurve()

        # Create the top circle at the middle of the vase
        mid_plane = rg.Plane(origin + normal * height * widening_relative_height, normal)
        mid_circle = rg.Circle(mid_plane, wider_radius).ToNurbsCurve()

        # Create the circle at the bottom of the vase neck
        neck_bottom_plane = rg.Plane(origin + normal * height * neck_relative_height, normal)
        neck_bottom_circle = rg.Circle(neck_bottom_plane, neck_radius).ToNurbsCurve()

        # Create the top circle at the top of the vase
        top_plane = rg.Plane(origin + normal * height, normal)
        top_circle = rg.Circle(top_plane, neck_radius).ToNurbsCurve()

        # Create the bowl by lofting the two circles
        closed = False
        vase = rg.Brep.CreateFromLoft([base_circle, mid_circle, neck_bottom_circle, top_circle], rg.Point3d.Unset, rg.Point3d.Unset, rg.LoftType.Normal, closed)[0]

        print("INFO: create_vase_body - return", vase)
        return vase
    except Exception as error:
        print("ERROR: create_vase_body ", "An error occurred:", traceback.format_exc())
        return None

def create_vase_base(origin, normal, radius):
    """
    This function creates a 3D model of a vase base. 
    The base is modeled as a circle at the base of the vase.

    Parameters:
        origin (Rhino.Geometry.Point3d): origin of the vase base plane
        normal (Rhino.Geometry.Vector3d): normal of vase base plane 
        radius (float): the radius of the base

    Return: 
        Rhino.Geometry.Circle: the created circle
    """
    try:
        print("INFO: create_vase_base - start", locals())
        # Create plane to locate the base
        plane = rg.Plane(origin, normal)

        # Create the base circle
        base_circle = rg.Circle(plane, radius).ToNurbsCurve()
        base = rg.Brep.CreatePlanarBreps(base_circle, TOLERANCE)[0]
        
        print("INFO: create_vase_base - return", base)
        return base
    except Exception as error:
        print("ERROR: create_vase_base ", "An error occurred:", traceback.format_exc())
        return None


# Generate input sliders by (name,value,min,max)
input_list = [
    InputSlider('body_height', 200, 10, 500),
    InputSlider('body_bottom_radius', 70, 10, 300),
    InputSlider('body_wider_radius', 120, 10, 300),
    InputSlider('body_widening_relative_height', 0.3, 0.1, 0.9),
    InputSlider('body_neck_radius', 30, 10, 100),
    InputSlider('body_neck_relative_height', 0.7, 0.1, 0.9),
    ]
create_params(input_list)

# User Parameters:
try: body_height 
except: body_height = 200

try: body_bottom_radius 
except: body_bottom_radius = 70

try: body_wider_radius 
except: body_wider_radius = 120

try: body_widening_relative_height 
except: body_widening_relative_height = 0.3

try: body_neck_radius 
except: body_neck_radius = 30

try: body_neck_relative_height 
except: body_neck_relative_height = 0.7

# Internal Parameters:
body_origin = rg.Point3d(0, 0, 0)
body_normal = rg.Vector3d.ZAxis

base_radius = body_bottom_radius
base_origin = body_origin
base_normal = body_normal
# Assembling
vase_body = create_vase_body(body_origin, body_normal, body_height, body_bottom_radius, body_wider_radius, body_widening_relative_height, body_neck_radius, body_neck_relative_height)
vase_base = create_vase_base(base_origin, base_normal, base_radius)

# Return created object by placing it in variable a
a = [vase_body, vase_base]