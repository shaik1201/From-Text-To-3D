import rhinoinside
rhinoinside.load()
import Rhino.Geometry as rg
import traceback

print('finished loading rhinoinside')
TOLERANCE = 0.01


def create_bottle_base(origin, normal, radius):
    """
    This function creates a 3D model of a bottle base. 
    The base is modeled as a circle at the base of the bottle.

    Parameters:
        origin (Rhino.Geometry.Point3d): the origin of the bottle base plane
        normal (Rhino.Geometry.Vector3d): the normal of bottle base plane 
        radius (float): the radius of the base

    Return: 
        Rhino.Geometry.Brep: The created 3D model
    """
    TOLERANCE = 0.01

    try:
        print("INFO: create_bottle_base - start", locals())
        # Create plane to locate the base
        plane = rg.Plane(origin, normal)

        # Create the base surface
        base_circle = rg.Circle(plane, radius)
        base = rg.Brep.CreatePlanarBreps(base_circle.ToNurbsCurve(), TOLERANCE)[0]

        print("INFO: create_bottle_base - return", base)
        return base

    except Exception as error:
        print("ERROR: create_bottle_base ", "An error occurred:", traceback.format_exc())
        return None


def create_bottle_body(origin, normal, bottom_radius, bottom_height, neck_radius, neck_height):
    """
    This function creates a 3D model of a bottle body. 
    The body is modeled as a cylinder that becomes narrow in its neck.

    Parameters:
        origin (Rhino.Geometry.Point3d): origin of the bottle body plane
        normal (Rhino.Geometry.Vector3d): normal of bottle body plane 
        bottom_radius (float): the radius of the bottom of the bottle
        bottom_height (float): the height of the bottle body
        neck_radius (float): the radius of the neck of the bottle
        neck_height (float): the height of the neck of the bottle

    Return: 
        Rhino.Geometry.Brep: 3D model of the bottle body
    """
    import clr
    clr.AddReference("System.Collections")
    from System.Collections.Generic import List

    try:
        print("INFO: create_bottle_body - start", locals())
        # Create plane to locate the body
        plane = rg.Plane(origin, normal)

        # Create the base surface of the bottle
        botom_start_circle = rg.Circle(plane, bottom_radius).ToNurbsCurve()
        bottom_mid_plane = rg.Plane(plane)
        bottom_mid_plane.Translate(plane.ZAxis * (bottom_height/2))
        bottom_mid_circle = rg.Circle(bottom_mid_plane, bottom_radius).ToNurbsCurve()
        bottom_end_plane = rg.Plane(plane)
        bottom_end_plane.Translate(plane.ZAxis * (bottom_height*0.9))
        bottom_end_circle = rg.Circle(bottom_end_plane, bottom_radius).ToNurbsCurve()
        
        # Create the neck of the bottle
        neck_start_plane = rg.Plane(plane)
        neck_start_plane.Translate(plane.ZAxis * (bottom_height*1.1))
        neck_start_circle = rg.Circle(neck_start_plane, neck_radius).ToNurbsCurve()
        neck_mid_plane = rg.Plane(plane)
        neck_mid_plane.Translate(plane.ZAxis * (bottom_height+(neck_height/2)))
        neck_mid_circle = rg.Circle(neck_mid_plane, neck_radius).ToNurbsCurve()
        neck_end_plane = rg.Plane(plane)
        neck_end_plane.Translate(plane.ZAxis * (bottom_height+neck_height))
        neck_end_circle = rg.Circle(neck_end_plane, neck_radius).ToNurbsCurve()

        # Create a .NET list to hold the curves
        curveList = List[rg.Curve]()
        curveList.Add(botom_start_circle)
        curveList.Add(bottom_mid_circle)
        curveList.Add(bottom_end_circle)
        curveList.Add(neck_start_circle)
        curveList.Add(neck_mid_circle)
        curveList.Add(neck_end_circle)

        closed = False
        bottle = rg.Brep.CreateFromLoft(curveList, rg.Point3d.Unset, rg.Point3d.Unset, rg.LoftType.Normal, closed)[0]

        print("INFO: create_bottle_body - return", bottle)
        return bottle

    except Exception as error:
        print("ERROR: create_bottle_body ", "An error occurred:", traceback.format_exc())
        return None


def create_bottle_lid(origin, normal, radius, height):
    """
    This function creates a 3D model of a bottle lid. 
    The lid is modeled as a cylinder with a cap on top.

    Parameters:
        origin (Rhino.Geometry.Point3d): origin of the bottle lid plane
        normal (Rhino.Geometry.Vector3d): normal of bottle lid plane 
        radius (float): the radius of the lid
        height (float): the height of the lid

    Return: 
        Rhino.Geometry.Brep: The created 3D model
    """

    try:
        print("INFO: create_bottle_lid - start", locals())
        # Create plane to locate the lid
        plane = rg.Plane(origin, normal)

        # Create the lid
        base_circle = rg.Circle(plane, radius)
        cylinder = rg.Cylinder(base_circle, height)
        cap_bottom = False
        cap_top = True
        lid = cylinder.ToBrep(cap_bottom, cap_top)

        print("INFO: create_bottle_lid - return", lid)
        return lid

    except Exception as error:
        print("ERROR: create_bottle_lid ", "An error occurred:", traceback.format_exc())
        return None


try:
    sliders_value = locals()['sliders_value']
    body_bottom_radius = int(sliders_value['body_bottom_radius'])
    body_bottom_part_height = int(sliders_value['body_bottom_part_height'])
    body_neck_radius = int(sliders_value['body_neck_radius'])
    body_neck_height = int(sliders_value['body_neck_height'])
    lid_height = int(sliders_value['lid_height'])

except:
    body_bottom_radius = 100
    body_bottom_part_height = 140
    body_neck_radius = 25
    body_neck_height = 70
    lid_height = 15

# Internal Parameters:
body_origin = rg.Point3d(0, 0, 0)
body_normal = rg.Vector3d.ZAxis

base_radius = body_bottom_radius
base_origin = body_origin
base_normal = body_normal

lid_radius = body_neck_radius
lid_origin = rg.Point3d(0, 0, body_bottom_part_height + body_neck_height - lid_height)
lid_normal = body_normal

# Assembling
bottle_base = create_bottle_base(base_origin, base_normal, base_radius)
bottle_body = create_bottle_body(body_origin, body_normal, body_bottom_radius, body_bottom_part_height, body_neck_radius, body_neck_height)
bottle_lid = create_bottle_lid(lid_origin, lid_normal, lid_radius, lid_height)

# Return created object by placing it in variable a
a = [bottle_base, bottle_body, bottle_lid]

# Return the parameters by placing them in variable b
b = {"body_bottom_radius": [10, 300, body_bottom_radius], "body_bottom_part_height": [10, 300, body_bottom_part_height],
     "body_neck_radius": [5, 100, body_neck_radius], "body_neck_height": [10, 150, body_neck_height],
     "lid_height": [10, 300, lid_height]}

