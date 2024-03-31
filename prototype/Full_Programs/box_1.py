import rhinoinside
rhinoinside.load()
# System and Rhino can only be loaded after rhinoinside is initialized
import Rhino.Geometry as rg  # noqa
import Rhino
import traceback

print('finished loading rhinoinside')
TOLERANCE = 0.01


def create_expanding_box_body(origin, normal, length, width, height, expansion):
    """
    This function creates a 3D model of an expanding box body. 
    The box is modeled as a brep.

    Parameters:
        origin (Rhino.Geometry.Point3d): origin of the box plane
        normal (Rhino.Geometry.Vector3d): normal of box plane - box will be created on this plane
        length (float): the length of the box
        width (float): the width of the box
        height (float): the height of the box
        expansion (float): the amount of expansion in the vertical direction

    Return: 
        Rhino.Geometry.Brep: the created box
    """
    import clr
    clr.AddReference("System.Collections")
    from System.Collections.Generic import List
    TOLERANCE = 0.01
    
    try:
        print("INFO: create_expanding_box_body - start", locals())
        # Create a plane to locate the box
        plane = rg.Plane(origin, normal)

        # Create the base rectangle
        base_rectangle = rg.Rectangle3d(plane, rg.Interval(-length/2,length/2), rg.Interval(-width/2,width/2)).ToNurbsCurve()

        # Create the top rectangle by expanding the base rectangle
        top_rectangle = base_rectangle.Duplicate() # Duplicate the base rectangle
        scale_transformer = rg.Transform.Scale(plane, expansion, expansion, 1) # Create transformer to scale the top rectangle
        top_rectangle.Transform(scale_transformer)
        top_rectangle.Translate(normal * height) # Move the rectangle to the top
        
        curveList = List[rg.Curve]()
        curveList.Add(top_rectangle)
        curveList.Add(base_rectangle)

        closed = False
        loft = rg.Brep.CreateFromLoft(curveList, rg.Point3d.Unset, rg.Point3d.Unset, rg.LoftType.Normal, closed)[0]

        print("INFO: create_bowl_body - return", loft)
        return loft

    except Exception as error:
        print("ERROR: create_expanding_box_body ", "An error occurred:", traceback.format_exc())
        return None


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

# Generate input sliders by ( name, value, min, max )
# input_list = [
#     InputSlider('body_width', 80, 10, 300),
#     InputSlider('body_length', 150, 10, 400),
#     InputSlider('body_height', 100, 10, 500),
#     InputSlider('body_expansion', 1.2, 0.1, 5.0),
# ]
# create_params(input_list)

# User Parameters:
try:
    sliders_value = locals()['sliders_value']
    body_width = float(sliders_value['body_width'])
    body_length = float(sliders_value['body_length'])
    body_height = float(sliders_value['body_height'])
    body_expansion = float(sliders_value['body_expansion'])
except:
    body_width = 80
    body_length = 150
    body_height = 100
    body_expansion = 1.2


# Internal Parameters:
body_origin = rg.Point3d(0, 0, 0)
body_normal = rg.Vector3d.ZAxis

base_length = body_length
base_width = body_width
base_origin = body_origin
base_normal = body_normal

# Assembling
box_body = create_expanding_box_body(body_origin, body_normal, body_length, body_width, body_height, body_expansion)
box_base = create_expanding_box_base(base_origin, base_normal, base_length, base_width)

# Return created object by placing it in variable a
a = [box_body, box_base]

b = {"body_width": [10, 300, body_width], "body_length": [10, 400, body_length],
     "body_height": [10, 500, body_height], 'body_expansion': [0.1, 5.0, body_expansion]}

