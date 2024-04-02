import Rhino
import Rhino.Geometry as rg
import traceback

TOLERANCE = Rhino.RhinoDoc.ActiveDoc.ModelAbsoluteTolerance

def create_wine_glass_body(origin, normal, height, bottom_radius, mid_radius, top_radius, relative_mid_height):
    """
    This function creates a 3D model of a wine glass body.
    The body of the wine glass is modeled as a truncated cone or a goblet. It features a wider bowl at the top that gradually tapers down into a narrower stem towards the base. The bowl itself can be approximated as a portion of a sphere or a paraboloid.

    Parameters:
        origin (Rhino.Geometry.Point3d): the origin of the wine glass body plane
        normal (Rhino.Geometry.Vector3d): the normal of the wine glass body plane
        height (float): the hieght of the body
        bottom_radius (float): the bootom radius of the body
        mid_radius (float): the middle radius of the body
        top_radius (float): the top radius of the body
        relative_mid_height (float): the relative height of the midlle circle along the body

    Return: 
        Rhino.Geometry.Brep: 3D model of the wine glass body
    """
    try:
        print("INFO: wine_glass_body - start", locals())
        # Create plane to locate the body
        plane = rg.Plane(origin, normal)

        # Create the base circle at the bottom of the body
        base_circle = rg.Circle(plane, bottom_radius).ToNurbsCurve()

        # Create circle at the relative middle of the body
        mid_plane = rg.Plane(origin + normal * height * relative_mid_height, normal)
        mid_circle = rg.Circle(mid_plane, mid_radius).ToNurbsCurve()

        # Create the top circle at the top of the body
        top_plane = rg.Plane(origin + normal * height, normal)
        top_circle = rg.Circle(top_plane, top_radius).ToNurbsCurve()

        # Create the body by lofting the circles
        closed = False
        loft = rg.Brep.CreateFromLoft([base_circle, mid_circle, top_circle], rg.Point3d.Unset, rg.Point3d.Unset, rg.LoftType.Normal, closed)[0]

        print("INFO: wine_glass_body - return", loft)
        return loft
    except Exception as error:
        print("ERROR: wine_glass_body ", "An error occurred:", traceback.format_exc())
        return None

def create_wine_glass_handle(origin, normal, height, radius):
    """
    This function creates a 3D model of a wine glass handle.
    The wine glass handle is modeled as a tall thin cylinder.

    Parameters:
        origin (Rhino.Geometry.Point3d): the origin of the wine glass handle plane
        normal (Rhino.Geometry.Vector3d): the normal of the wine glass handle plane
        height (float): the height of the handle
        radius (float): the thickness of the handle

    Return: 
        Rhino.Geometry.Brep: 3D model of the wine glass handle
    """
    try:
        print("INFO: wine_glass_handle - start", locals())
        # Create a plane to locate the handle
        handle_plane = rg.Plane(origin, normal)

        # Create the base circle of the handle
        bottom_circle = rg.Circle(handle_plane, radius)

        # Create the cylinder that defines the handle shape
        cylinder = rg.Cylinder(bottom_circle, height)
        cap_bottom = False
        cap_top = False
        handle = cylinder.ToBrep(cap_bottom, cap_top)

        print("INFO: wine_glass_handle - return", handle)
        return handle
    except Exception as error:
        print("ERROR: wine_glass_handle ", "An error occurred:", traceback.format_exc())
        return None

def create_wine_glass_base(origin, normal, height, bottom_radius, top_radius):
    """
    This function creates a 3D model of a wine glass base.
    The wine glass base is modeled as a cylindrical plate, transitioning smoothly from a wider bottom to a narrower top.

    Parameters:
        origin (Rhino.Geometry.Point3d): the origin of the wine glass base plane
        normal (Rhino.Geometry.Vector3d): the normal of the wine glass base plane
        height (float): the height of the base
        bottom_radius (float): the bottom radius of the base
        top_radius (float): the top radius of the base

    Return: 
        Rhino.Geometry.Brep: 3D model of the wine glass base
    """
    try:
        print("INFO: wine_glass_base - start", locals())
        # Create a plane to locate the bottom part of the base
        bottom_base_plane = rg.Plane(origin, normal)

        # Create the wide circle at the bottom plane of the base
        base_bottom_circle = rg.Circle(bottom_base_plane, bottom_radius).ToNurbsCurve()

        # Create and move a plane to locate the top part of the base
        top_plane = rg.Plane(origin + normal * height, normal)

        # Create the narrow circle at the top plane of the base
        base_top_circle = rg.Circle(top_plane, top_radius).ToNurbsCurve()

        # Create the base by lofting the two circles
        closed = False
        loft = rg.Brep.CreateFromLoft([base_bottom_circle, base_top_circle], rg.Point3d.Unset, rg.Point3d.Unset, rg.LoftType.Normal, closed)[0]

        print("INFO: wine_glass_base - return", loft)
        return loft
    except Exception as error:
        print("ERROR: wine_glass_base ", "An error occurred:", traceback.format_exc())
        return None

# Generate input sliders by (name,value,min,max)
input_list = [
    InputSlider('body_bottom_height', 140, 80, 300),
    InputSlider('relative_lower_mid_height', 0.5, 0.0, 1.0),
	InputSlider('relative_upper_mid_height', 0.8, 0.0, 1.0),
	InputSlider('body_top_height', 240, 90, 350),
	InputSlider('body_bottom_radius', 4.5, 1.0, 10.0),
	InputSlider('body_lower_mid_radius', 40.0, 4.5, 100.0),
	InputSlider('body_upper_mid_radius', 40.0, 4.5, 100.0),
	InputSlider('body_top_radius', 35.0, 4.5, 100.0),
	InputSlider('base_height', 10, 1, 80),
	InputSlider('base_bottom_radius', 32.5, 10.0, 50.0),
]
create_params(input_list)

# User Parameters:
try: body_bottom_height
except: body_bottom_height = 140

try: relative_lower_mid_height
except: relative_lower_mid_height = 0.5

try: relative_upper_mid_height
except: relative_upper_mid_height = 0.8

try: body_top_height
except: body_top_height =240

try: body_bottom_radius
except: body_bottom_radius = 4.5

try: body_lower_mid_radius
except: body_lower_mid_radius = 40

try: body_upper_mid_radius
except: body_upper_mid_radius = 40

try: body_top_radius
except: body_top_radius = 35

try: base_bottom_radius
except: base_bottom_radius = 32.5

try: base_height
except: base_height = 10

# Parameters
body_normal = rg.Vector3d.ZAxis

base_height = 10
base_bottom_radius = 32.5
base_top_radius = handle_radius
base_origin = rg.Point3d(0, 0, 0)
base_normal = body_normal

handle_height  = 100
handle_radius = 4.5
handle_origin = rg.Point3d(0, 0, base_height)
handle_normal = body_normal

body_height = 100
body_bottom_radius = handle_radius
body_mid_radius = 40
body_top_radius = 35
body_relative_mid_height = 0.4
body_origin = rg.Point3d(0, 0, base_height + handle_height)

# Assembling
wine_glass_body = create_wine_glass_body(body_origin, body_normal, body_bottom_height, relative_lower_mid_height, relative_upper_mid_height, body_top_height, body_bottom_radius, body_lower_mid_radius, body_upper_mid_radius, body_top_radius)
wine_glass_base = create_wine_glass_base(base_origin, base_normal, base_height, base_bottom_radius, base_top_radius)
wine_glass_handle = create_wine_glass_handle(handle_origin, handle_normal, handle_height, handle_radius)
# Return the created object by placing it in variable a
a = [wine_glass_body, wine_glass_base, wine_glass_handle]
