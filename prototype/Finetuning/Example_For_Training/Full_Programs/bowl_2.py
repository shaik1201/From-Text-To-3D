import rhinoinside
rhinoinside.load()
import Rhino.Geometry as rg
import traceback

print('finished loading rhinoinside')
TOLERANCE = 0.01


def create_bowl_body(origin, normal, bottom_radius, top_radius, height):
    """
    This function creates a 3D model of a bowl body. 
    The body is modeled as a conical or semi-spherical shape.

    Parameters:
        origin (Rhino.Geometry.Point3d): the origin of the bowl body plane
        normal (Rhino.Geometry.Vector3d): the normal of bowl body plane 
        bottom_radius (float): the radius of the bottom of the bowl
        top_radius (float): the radius of the top of the bowl
        height (float): the height of the bowl

    Return: 
        Rhino.Geometry.Brep: 3D model of the bowl body
    """
    import clr
    clr.AddReference("System.Collections")
    from System.Collections.Generic import List
    
    try:
        print("INFO: create_bowl_body - start", locals())
        # Create plane to locate the body
        plane = rg.Plane(origin, normal)

        # Create the base circle at the bottom of the bowl
        base_circle = rg.Circle(plane, bottom_radius).ToNurbsCurve()

        # Create the top circle at the top of the bowl
        top_plane = rg.Plane(origin + normal * height, normal)
        top_circle = rg.Circle(top_plane, top_radius).ToNurbsCurve()

        # Create a .NET list to hold the curves
        curveList = List[rg.Curve]()
        curveList.Add(base_circle)
        curveList.Add(top_circle)

        closed = False
        loft = rg.Brep.CreateFromLoft(curveList, rg.Point3d.Unset, rg.Point3d.Unset, rg.LoftType.Normal, closed)[0]

        print("INFO: create_bowl_body - return", loft)
        return loft

    except Exception as error:
        print("ERROR: create_bowl_body ", "An error occurred:", traceback.format_exc())
        return None


def create_bowl_base(origin, normal, radius):
    """
    This function creates a 3D model of a bowl base. 
    The base is modeled as a circle at the base of the bowl.

    Parameters:
        origin (Rhino.Geometry.Point3d): the origin of the bowl base plane
        normal (Rhino.Geometry.Vector3d): the normal of bowl base plane 
        radius (float): the radius of the base

    Return: 
        Rhino.Geometry.Brep: 3D model of the base
    """
    TOLERANCE = 0.01

    try:
        print("INFO: create_bowl_base - start", locals())
        # Create plane to locate the base
        plane = rg.Plane(origin, normal)

        # Create the base circle
        base_circle = rg.Circle(plane, radius).ToNurbsCurve()

        # Create the base
        base = rg.Brep.CreatePlanarBreps(base_circle, TOLERANCE)[0]

        print("INFO: create_bowl_base - return", base)
        return base
    except Exception as error:
        print("ERROR: create_bowl_base ", "An error occurred:", traceback.format_exc())
        return None


# Generate input sliders by (name,value,min,max)
# input_list = [
#     InputSlider('body_height', 80, 10, 300),
#     InputSlider('body_bottom_radius', 200, 10, 400),
#     InputSlider('body_top_radius', 250, 10, 400),
#     ]
# create_params(input_list)

# User Parameters: this needs to be adjusted based on the llm output
try:
    sliders_value = locals()['sliders_value']
    body_height = int(sliders_value['body_height'])
    body_bottom_radius = int(sliders_value['body_bottom_radius'])
    body_top_radius = int(sliders_value['body_top_radius'])

except:
    body_height = 80
    body_bottom_radius = 100
    body_top_radius = 125

# Internal Parameters:
body_origin = rg.Point3d(0, 0, 0)
body_normal = rg.Vector3d.ZAxis

base_radius = body_bottom_radius
base_origin = body_origin
base_normal = body_normal

# Assembling
bowl_body = create_bowl_body(body_origin, body_normal, body_bottom_radius, body_top_radius, body_height)
bowl_base = create_bowl_base(base_origin, base_normal, base_radius)

# Return the created objects by placing them in variable a
a = [bowl_base, bowl_body]

# Return the parameters by placing them in variable b
b = {"body_height": [10, 300, body_height], "body_bottom_radius": [10, 400, body_bottom_radius],
     "body_top_radius": [10, 400, body_top_radius]}
