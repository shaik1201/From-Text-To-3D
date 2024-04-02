import rhinoinside
rhinoinside.load()
import Rhino.Geometry as rg
import traceback

print('finished loading rhinoinside')
TOLERANCE = 0.01


def create_glass_body(origin, normal, radius, height):
    """
    This function creates a 3D model of a glass body. 
    The body is modeled as an open cylinder.

    Parameters:
        origin (Rhino.Geometry.Point3d): the origin of the glass body plane
        normal (Rhino.Geometry.Vector3d): the normal of the glass body plane
        radius (float): the radius of the glass body
        height (float): the height of the glass body

    Return: 
        Rhino.Geometry.Brep: the created 3D model
    """

    try:
        print("INFO: create_glass_body - start", locals())
        # Create plane to locate the body
        plane = rg.Plane(origin, normal)

        # Create the base circle at the bottom of the glass
        base_circle = rg.Circle(plane, radius)
        
        # Create open cylinder
        cylinder = rg.Cylinder(base_circle, height)
        cap_bottom = False
        cap_top = False
        glass = cylinder.ToBrep(cap_bottom, cap_top)

        print("INFO: create_glass_body - return", glass)
        return glass

    except Exception as error:
        print("ERROR: create_glass_body ", "An error occurred:", traceback.format_exc())
        return None


def create_glass_base(origin, normal, radius):
    """
    This function creates a 3D model of a glass base. 
    The base is modeled as a circle at the base of the glass.

    Parameters:
        origin (Rhino.Geometry.Point3d): origin of the glass base plane
        normal (Rhino.Geometry.Vector3d): normal of glass base plane 
        radius (float): the radius of the base

    Return: 
        Rhino.Geometry.Brep: 3D model of the base
    """
    TOLERANCE = 0.01
    
    try:
        print("INFO: create_glass_base - start", locals())
        # Create plane to locate the base
        plane = rg.Plane(origin, normal)

        # Create the base circle
        base_circle = rg.Circle(plane, radius).ToNurbsCurve()

        # Create the base
        base = rg.Brep.CreatePlanarBreps(base_circle, TOLERANCE)[0]

        print("INFO: create_glass_base - return", base)
        return base

    except Exception as error:
        print("ERROR: create_glass_base ", "An error occurred:", traceback.format_exc())
        return None


# User Parameters:
try:
    sliders_value = locals()['sliders_value']
    body_radius = int(sliders_value['body_radius'])
    body_height = int(sliders_value['body_height'])

except:
    body_radius = 80
    body_height = 300

# Parameters
body_origin = rg.Point3d(0, 0, 0)
body_normal = rg.Vector3d.ZAxis

base_radius = body_radius
base_origin = body_origin
base_normal = body_normal

# Assembling
glass_body = create_glass_body(body_origin, body_normal, body_radius, body_height)
glass_base = create_glass_base(base_origin, base_normal, base_radius)

# Return the created objects by placing them in variable a
a = [glass_body, glass_base]

# Return the parameters by placing them in variable b
b = {"body_height": [10, 500, body_height],
     "body_radius": [1, 300, body_radius],}