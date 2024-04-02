import Rhino
import Rhino.Geometry as rg
import traceback

TOLERANCE = Rhino.RhinoDoc.ActiveDoc.ModelAbsoluteTolerance

def create_soup_plate_body(body_bottom_radius, body_top_radius, body_origin, body_normal, body_height):
    """
    This function creates a 3D model of a soup plate body. 
    The soup plate body is modeled as a curved or sloping sides that extend upward from the base

    Parameters:
        body_origin (Rhino.Geometry.Point3d): the origin of the plate body plane
        body_normal (Rhino.Geometry.Vector3d): the normal of plate body plane
        body_bottom_radius (float): the radius of the base of the plate body
        body_top_radius (float): the radius of the top of the plate body
        body_height (float): the plate's body height

    Return: 
        Rhino.Geometry.Brep: 3D model of the soup plate body
    """
    try:
        print("INFO: create_soup_plate_body - start", locals())
        #create plane to locate the plate body
        body_plane = rg.Plane(body_origin, body_normal)

        #ceate the bottom part of the body
        body_bottom_circle = rg.Circle(body_plane, body_bottom_radius)

        #create the top part of the plate body
        body_top_plane = rg.Plane(body_plane)
        body_top_plane.Translate(body_top_plane.Normal*body_height)
        body_top_circle = rg.Circle(body_top_plane, body_top_radius)

        #create the plate by lofting the three circles
        closed = False
        loft = rg.Brep.CreateFromLoft([body_bottom_circle.ToNurbsCurve(), body_top_circle.ToNurbsCurve()], rg.Point3d.Unset, rg.Point3d.Unset, rg.LoftType.Normal, closed)[0]

        print("INFO: create_soup_plate_body - return", loft)
        return loft 
    except Exception as error:
        print("ERROR: create_soup_plate_body ", "An error occurred:", traceback.format_exc())
        return None

def create_soup_plate_base(base_radius, origin, normal):
    """
    This function creates a 3D model of a  soup plate base. 
    The soup plate base is modeled as a flat surface in a circle shape at the bottom of the soup plate.

    Parameters:
        base_origin (Rhino.Geometry.Point3d): the origin of the soup plate base plane
        base_normal (Rhino.Geometry.Vector3d): the normal of the soup plate base plane
        base_radius (float): the radius of the soup plate base

    Return: 
        Rhino.Geometry.Brep: 3D model of the soup plate
    """
    try:
        print("INFO: create_soup_plate_base - start", locals())
        #create a plane to locate the soup plate base
        base_plane = rg.Plane(origin, normal)

        #create the plate base
        base_circle = rg.Circle(base_plane, base_radius)
        plate_base = rg.Brep.CreatePlanarBreps(base_circle.ToNurbsCurve(), TOLERANCE)[0]  

        print("INFO: create_soup_plate_base - return", plate_base)
        return plate_base 
    except Exception as error:
        print("ERROR: create_soup_plate_base ", "An error occurred:", traceback.format_exc())
        return None

def create_soup_plate_rim(rim_bottom_radius, rim_top_radius, rim_origin, rim_normal, rim_height):
    """
    This function creates a 3D model of a soup plate rim. 
    The plate rim is modeled as a curved surface with a circular shape around the body

    Parameters:
        rim_origin (Rhino.Geometry.Point3d): the origin of the soup plate rim plane
        rim_normal (Rhino.Geometry.Vector3d): the normal of the soup plate rim plane
        rim_bottom_radius (float): the radius of the base of the soup plate rim
        rim_top_radius (float): the radius of the top of the soup plate rim
        rim_height (float): the plate's rim height

    Return: 
        Rhino.Geometry.Brep: 3D model of the soup plate rim
    """
    try:
        print("INFO: create_plate_rim - start", locals())
        #create plane to locate the soup plate rim
        rim_plane = rg.Plane(rim_origin, rim_normal)

        #create the bottom part of the rim
        rim_bottom_circle = rg.Circle(rim_plane, rim_bottom_radius)

        #create the top part of the soup plate rim
        rim_top_plane = rg.Plane(rim_plane)
        rim_top_plane.Translate(rim_top_plane.Normal * rim_height)
        rim_top_circle = rg.Circle(rim_top_plane, rim_top_radius)

        #create the soup plate by lofting the two circles
        closed = False
        loft = rg.Brep.CreateFromLoft([rim_bottom_circle.ToNurbsCurve(), rim_top_circle.ToNurbsCurve()], rg.Point3d.Unset, rg.Point3d.Unset, rg.LoftType.Normal, closed)[0]

        print("INFO: create_soup_plate_rim - return", loft)
        return loft 
    except Exception as error:
        print("ERROR: create_soup_plate_rim ", "An error occurred:", traceback.format_exc())
        return None

# Generate input sliders by (name,value,min,max)
input_list = [
    InputSlider('body_bottom_radius', 100, 10, 300),
    InputSlider('body_top_radius', 145, 10, 300),
    InputSlider('body_height', 40, 10, 100),
    InputSlider('rim_top_radius', 185, 10, 350),
    InputSlider('rim_height', 6, 0, 200)
]
create_params(input_list)

# User Parameters:
try: body_bottom_radius
except: body_bottom_radius = 100

try: body_top_radius
except: body_top_radius = 145

try: body_height
except: body_height = 40

try: rim_top_radius
except: rim_top_radius = 185

try: rim_height
except: rim_height = 6

# Internal Parameters:
body_origin = rg.Point3d(0, 0, 0)
body_normal = rg.Vector3d.ZAxis

base_radius = body_bottom_radius
base_origin = body_origin
base_normal = body_normal

rim_bottom_radius = body_top_radius
rim_origin = rg.Point3d(0, 0, body_height)
rim_normal = body_normal

# Assembling
soup_plate_body = create_soup_plate_body(body_bottom_radius, body_top_radius, body_origin, body_normal, body_height)
soup_plate_base = create_soup_plate_base(base_radius, base_origin, base_normal)
soup_plate_rim = create_soup_plate_rim(rim_bottom_radius, rim_top_radius, rim_origin, rim_normal, rim_height)

# Return the created object by placing it in variable a
a = [soup_plate_body, soup_plate_base, soup_plate_rim]
