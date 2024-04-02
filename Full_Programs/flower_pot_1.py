import rhinoinside
rhinoinside.load()
# System and Rhino can only be loaded after rhinoinside is initialized
import Rhino.Geometry as rg  # noqa
import Rhino
import traceback
import math

print('finished loading rhinoinside')
TOLERANCE = 0.01


def create_expanding_pot_body(origin, normal, bottom_radius, top_radius, height, edge_protrusion, edge_protrusion_reltaive_height):
    """
    This function creates a 3D model of a flower pot body. 
    The body is modeled as a cylinder with a slight curve outwards at the top edge.

    Parameters:
        origin (Rhino.Geometry.Point3d): origin of the pot body plane
        normal (Rhino.Geometry.Vector3d): normal of pot body plane 
        bottom_radius (float): the radius of the bottom of the pot
        top_radius (float): the radius of the top of the pot
        height (float): the height of the pot
        edge_protrusion (float): the amount of protrusion of the edge of the pot
        edge_protrusion_reltive_hieght (float): the relative height of the upper protrusion

    Return: 
        Rhino.Geometry.Brep: 3D model of the pot body
    """
    import clr
    clr.AddReference("System.Collections")
    from System.Collections.Generic import List
    
    try:
        print("INFO: create_expanding_pot_body - start", locals())
        # Create plane to locate the pot
        plane = rg.Plane(origin, normal)

        # Create the base circle at the bottom of the pot
        base_circle = rg.Circle(plane, bottom_radius).ToNurbsCurve()

        # Create the top circle at the top of the pot
        top_plane_origin = origin + plane.Normal * height * edge_protrusion_reltaive_height
        top_plane = rg.Plane(top_plane_origin, normal)
        top_circle = rg.Circle(top_plane, top_radius).ToNurbsCurve()

        # Create the edge protrusion
        protrusion_bottom_circle = rg.Circle(top_plane, top_radius+ edge_protrusion).ToNurbsCurve()
        protrusion_top_circle = protrusion_bottom_circle.Duplicate()
        protrusion_top_circle.Translate(normal*height*(1-edge_protrusion_reltaive_height))
        
        # Create a .NET list to hold the curves
        curveList = List[rg.Curve]()
        curveList.Add(base_circle)
        curveList.Add(top_circle)
        curveList.Add(protrusion_bottom_circle)
        curveList.Add(protrusion_top_circle)
    
        closed = False
        loft = rg.Brep.CreateFromLoft(curveList, rg.Point3d.Unset, rg.Point3d.Unset, rg.LoftType.Normal, closed)[0]

        print("INFO: create_expanding_pot_body - return", loft)
        return loft

    except Exception as error:
        print("ERROR: create_bowl_body ", "An error occurred:", traceback.format_exc())
        return None

def create_pot_base(origin, normal, base_radius, holes_radius, holes_amount, holes_distance_from_center):
    """
    This function creates a 3D model of a pot base. 
    The base is modeled as a perforated flat surface in circle shape at the bottom of the pot. 
    The holes are located in a circle around the center of the surface.

    Parameters:
        origin (Rhino.Geometry.Point3d): origin of the pot base plane
        normal (Rhino.Geometry.Vector3d): normal of pot base plane 
        base_radius (float): the radius of the base
        holes_radius (float): the radius of the holes
        holes_amount (int): the amount of holes in the base
        holes_distance_from_center (float): the distance of the holes from the center of the base

    Return: 
        Rhino.Geometry.Brep: 3D model of the pot base
    """
    import clr
    clr.AddReference("System.Collections")
    from System.Collections.Generic import List
    import math
    TOLERANCE = 0.01
    
    try:
        print("INFO: create_pot_base - start", locals())
        # Create plane to locate the base
        plane = rg.Plane(origin, normal)

        # Create the base
        base_circle = rg.Circle(plane, base_radius)
        base = rg.Brep.CreatePlanarBreps(base_circle.ToNurbsCurve(), TOLERANCE)[0]

        # Create the holes
        holes = []
        holesList = List[rg.Brep]()
        
        for i in range(holes_amount):
            angle = i * (2 * math.pi / holes_amount)
            x = holes_distance_from_center * math.cos(angle)
            y = holes_distance_from_center * math.sin(angle)
            hole_origin = plane.PointAt(x, y)
            hole_normal = plane.Normal
            hole_plane = rg.Plane(hole_origin, hole_normal)
            hole = rg.Circle(hole_plane, holes_radius).ToNurbsCurve()
            hole = rg.Brep.CreatePlanarBreps(hole, TOLERANCE)[0]
            holes.append(hole)
            holesList.Add(hole)
            

        # Subtract the holes from the base
        curveList = List[rg.Brep]()
        curveList.Add(base)

        res = rg.Brep.CreateBooleanDifference(curveList, holesList, TOLERANCE)[0]

        print("INFO: create_pot_base - return", res)
        return res

    except Exception as error:
        print("ERROR: create_pot_base ", "An error occurred:", traceback.format_exc())
        return None

# Generate input sliders by (name,value,min,max)
# input_list = [
#     InputSlider('body_bottom_radius', 100, 10, 300),
#     InputSlider('body_top_radius', 120, 10, 320),
#     InputSlider('body_height', 100, 10, 400),
#     InputSlider('body_edge_protrusion', 10, 0, 100),
#     InputSlider('body_edge_protrusion_reltive_hieght', 0.8, 0.0, 1.0),
#     InputSlider('holes_radius', 10, 1, 50),
#     InputSlider('holes_amount', 4, 3, 20),
#     InputSlider('holes_distance_from_center', 40, 10, 200)
# ]
# create_params(input_list)

# User Parameters:
try:
    sliders_value = locals()['sliders_value']
    body_bottom_radius = int(sliders_value['body_bottom_radius'])
    body_top_radius = int(sliders_value['body_top_radius'])
    body_height = int(sliders_value['body_height'])
    body_edge_protrusion = int(sliders_value['body_edge_protrusion'])
    body_edge_protrusion_relative_height = float(sliders_value['body_edge_protrusion_relative_height'])
    holes_radius = int(sliders_value['holes_radius'])
    holes_amount = int(sliders_value['holes_amount'])
    holes_distance_from_center = int(sliders_value['holes_distance_from_center'])

except:
    body_top_radius = 120
    body_bottom_radius = 150
    body_height = 100
    body_edge_protrusion = 10
    body_edge_protrusion_relative_height = 0.8
    holes_radius = 10
    holes_amount = 4
    holes_distance_from_center = 40
    

# Internal Parameters:
body_origin = rg.Point3d(0, 0, 0)
body_normal = rg.Vector3d.ZAxis

base_radius = body_bottom_radius
base_origin = body_origin
base_normal = body_normal

# Assembling
pot_body = create_expanding_pot_body(body_origin, body_normal, body_bottom_radius, body_top_radius, body_height, body_edge_protrusion, body_edge_protrusion_relative_height)
pot_base = create_pot_base(base_origin, base_normal, base_radius, holes_radius, holes_amount, holes_distance_from_center)

# Return created object by placing it in variable a
a = [pot_body, pot_base]

b = {"body_top_radius": [10, 320, body_top_radius], "body_bottom_radius": [10, 300, body_bottom_radius], "body_height": [10, 400, body_height],
     "body_edge_protrusion": [0, 100, body_edge_protrusion], "body_edge_protrusion_relative_height": [0.0, 1.0, body_edge_protrusion_relative_height],
     "holes_radius": [1, 50, holes_radius], "holes_amount": [3, 20, holes_amount], "holes_distance_from_center": [10, 200, holes_distance_from_center]}
