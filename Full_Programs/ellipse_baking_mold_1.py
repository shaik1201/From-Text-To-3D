import rhinoinside
rhinoinside.load()
# System and Rhino can only be loaded after rhinoinside is initialized
import Rhino.Geometry as rg  # noqa
import Rhino
import traceback

print('finished loading rhinoinside')
TOLERANCE = 0.01


def create_ellipse_baking_mold_body(origin, normal, width, length, height):
    """
    This function creates a 3D model of a ellipse baking mold body. 
    The body of the mold is modeled as an extruded ellipse.

    Parameters:
        origin (Rhino.Geometry.Point3d): origin of the body plane
        normal (Rhino.Geometry.Vector3d): normal of body plane
        length (float): the length of the body 
        width (float): the width of the body
        height (float): the height of the body

    Return: 
        Rhino.Geometry.Brep: 3D model of the baking mold body
    """
    TOLERANCE = 0.01

    try:
        print("INFO: create_ellipse_baking_mold_body - start", locals())
        # Create a plane to locate the body
        body_plane = rg.Plane(origin, normal)

        # Create the base of the body - the bottom ellipse
        bottom_ellipse = rg.Ellipse(body_plane, length / 2, width / 2).ToNurbsCurve() # The dim input is a radius - divide by 2 = diameter

        # Create the body - the extrusion of the ellipse
        ellipse_body = rg.Extrusion.CreateExtrusion(bottom_ellipse, normal * height).ToBrep()

        print("INFO: create_ellipse_baking_mold_body - return", ellipse_body)
        return ellipse_body

    except Exception as error:
        print("ERROR: create_ellipse_baking_mold_body ", "An error occurred:", traceback.format_exc())
        return None


def create_ellipse_baking_mold_base(origin, normal, width, length):
    """
    This function creates a 3D model of a ellipse baking mold base. 
    The base of the mold is modeled as a flat ellipse surface.

    Parameters:
        origin (Rhino.Geometry.Point3d): origin of the base plane
        normal (Rhino.Geometry.Vector3d): normal of base plane
        length (float): the length of the base 
        width (float): the width of the base

    Return: 
        Rhino.Geometry.Brep: 3D model of the baking mold base
    """
    TOLERANCE = 0.01

    try:
        print("INFO: create_ellipse_baking_mold_base - start", locals())
        # Create a plane to locate the base
        base_plane = rg.Plane(origin, normal)

        # Create the base ellipse
        base_ellipse = rg.Ellipse(base_plane, length / 2, width / 2).ToNurbsCurve() # The dim input is a radius - divide by 2 = diameter

        # Create the base surface
        base_surface = rg.Brep.CreatePlanarBreps(base_ellipse, TOLERANCE)[0]

        print("INFO: create_ellipse_baking_mold_base - return", base_surface)
        return base_surface

    except Exception as error:
        print("ERROR: create_ellipse_baking_mold_body ", "An error occurred:", traceback.format_exc())
        return None


def create_ellipse_baking_mold_rim(origin, normal, width, length, height, alignment, thickness):
    """
    This function creates a 3D model of a ellipse baking mold rim. 
    The rim of the mold is modeled a pipe cut vertically in the shape of an ellipse.

    Parameters:
        origin (Rhino.Geometry.Point3d): the origin of the rim plane
        normal (Rhino.Geometry.Vector3d): the normal of the rim plane
        alignment (Rhino.Geometry.Vector3d): the direction in which the rim expands
        height (float): the height of the rim
        thickness (float): the thickness of the rim
        length (float): the length of the ellipse 
        width (float): the width of the ellipse 

    Return: 
        Rhino.Geometry.Brep: 3D model of the baking mold rim
    """
    TOLERANCE = 0.01

    try:
        print("INFO: create_ellipse_baking_mold_rim - start", locals())
        if thickness == 0 or height == 0: # No rim option
            return None
        # Create a plane to locate the rim
        rim_plane = rg.Plane(origin, alignment)
        
        # Create an ellipse at the top of the rim
        top_ellipse = rg.Ellipse(rim_plane, length / 2, width / 2).ToNurbsCurve() # The input is a radius -> divided by 2 = diameter
        
        # Determining an arc section for sweeping
        start_pt = origin + (normal * length / 2) # From the center of the ellipse to the edge
        end_pt = start_pt - (alignment * height)
        mid_pt = start_pt - (alignment * height)/2 + (normal * thickness)
        arc = rg.Arc(start_pt, mid_pt, end_pt).ToNurbsCurve()
        
        # Sweep the arc along the ellipse shape to create the rim
        closed = False
        rim = rg.Brep.CreateFromSweep(top_ellipse, arc, closed, TOLERANCE)[0]
        
        print("INFO: create_ellipse_baking_mold_rim - return", rim)
        return rim

    except Exception as error:
        print("ERROR: create_ellipse_baking_mold_rim ", "An error occurred:", traceback.format_exc())
        return None


# Generate input sliders by (name,value,min,max)
# input_list = [
#     InputSlider('body_width', 230, 10, 600),
#     InputSlider('body_length', 280, 10, 600),
#     InputSlider('body_height', 50, 10, 100),
#     InputSlider('rim_thickness', 3, 0, 50),
#     InputSlider('rim_height', 6, 0, 10)
# ]
# create_params(input_list)

try:
    sliders_value = locals()['sliders_value']
    body_width = int(sliders_value['body_width'])
    body_length = int(sliders_value['body_length'])
    body_height = int(sliders_value['body_height'])
    rim_thickness = int(sliders_value['rim_thickness'])
    rim_height = int(sliders_value['rim_height'])
except:  # If any of the keys are not found, set default values for all
    body_width = 230
    body_length = 280
    body_height = 50
    rim_thickness = 3
    rim_height = 6

# Parameters
body_origin = rg.Point3d(0, 0, 0)
body_normal = rg.Vector3d.ZAxis

base_origin = body_origin
base_normal = body_normal.ZAxis
base_width = body_width
base_length = body_length

rim_ellipse_width = body_width
rim_ellipse_length = body_length
rim_origin = rg.Point3d(0, 0, body_height)
rim_normal = rg.Vector3d.XAxis # The 'sweep' works well when using this axis
rim_alignment = body_normal.ZAxis

# Assembling
ellipse_baking_mold_body = create_ellipse_baking_mold_body(body_origin, body_normal, body_length, body_width, body_height)
ellipse_baking_mold_base = create_ellipse_baking_mold_base(base_origin, base_normal, base_length, base_width)
ellipse_baking_mold_rim = create_ellipse_baking_mold_rim(rim_origin, rim_normal, rim_ellipse_length, rim_ellipse_width, rim_height, rim_alignment, rim_thickness)

# Return the created object by placing it in variable a
a = [ellipse_baking_mold_body, ellipse_baking_mold_base, ellipse_baking_mold_rim]
b = {"body_width": [10, 600, body_width], "body_length": [10, 600, body_length],
     "body_height": [10, 600, body_height], "rim_thickness": [0, 50, rim_thickness],
     "rim_height": [0, 10, rim_height]}
