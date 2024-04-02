import rhinoinside
rhinoinside.load()
import Rhino.Geometry as rg
import traceback

print('finished loading rhinoinside')
TOLERANCE = 0.01


def create_expanding_box_base(origin, normal, length, width):
    """
    This function creates a 3D model of an expanding box base. 
    The base is modeled as a rectangle.

    Parameters:
        origin (Rhino.Geometry.Point3d): origin of the base plane
        normal (Rhino.Geometry.Vector3d): normal of base plane 
        length (float): the length of the base
        width (float): the width of the base

    Return: 
        Rhino.Geometry.Brep: the created base
    """
    TOLERANCE = 0.01

    try:
        print("INFO: create_expanding_box_base - start", locals())
        # Create a plane to locate the base
        plane = rg.Plane(origin, normal)

        # Create the base rectangle
        base_rectangle = rg.Rectangle3d(plane, rg.Interval(-length/2,length/2), rg.Interval(-width/2,width/2))

        # Create the expanding box base by extruding the rectangle
        base = rg.Brep.CreatePlanarBreps(base_rectangle.ToNurbsCurve(), TOLERANCE)[0]

        print("INFO: create_expanding_box_base - return", base)
        return base

    except Exception as error:
        print("ERROR: create_expanding_box_base ", "An error occurred:", traceback.format_exc())
        return None


# Parameters
body_length = 150
body_width = 100
body_origin = rg.Point3d(0, 0, 0)
body_normal = rg.Vector3d.ZAxis

base_length = body_length
base_width = body_width
base_origin = body_origin
base_normal = body_normal

# Assembling
box_base = create_expanding_box_base(base_origin, base_normal, base_length, base_width)

# Return created object by placing it in variable a
a = box_base