import rhinoinside
rhinoinside.load()
# System and Rhino can only be loaded after rhinoinside is initialized
import Rhino.Geometry as rg  # noqa
import Rhino
import traceback
import math

print('finished loading rhinoinside')
TOLERANCE = 0.01

def create_s_shape_hook_body(origin, normal, alignment, top_arc_radius, bottom_arc_radius, height, thickness, arc_angle_domain_relative_pi):
    """
    Create a 3D model of an S shape hook with rounded caps body. 
    The body is modeled as S-shaped pipe with rounded cap. The shape consists of two connected arcs at the top and bottom of the body..

    Parameters:
        origin (Rhino.Geometry.Point3d): origin of the hook body plane
        normal (Rhino.Geometry.Vector3d): normal of hook body plane 
        alignment (Rhino.Geometry.Vector3d): the direction in which the hook body is created
        top_arc_radius (float): the radius of the top arc
        bottom_arc_radius (float): the radius of the bottom arc
        height (float): the total height of the body
        thickness (float): the thickness of the pipe that models the hook
        arc_angle_domain_relative_pi (float): length of the arc in as a product of PI

    Return: 
        Rhino.Geometry.Brep: 3D model of the S-shaped hook body
    """
    import clr
    clr.AddReference("System.Collections")
    from System.Collections.Generic import List
    import math
    TOLERANCE = 0.01
    
    try:
        print("INFO: create_s_shape_hook_body - start", locals())
        # Create plane to locate the body
        plane = rg.Plane(origin, normal)
        
        # Create the top arc
        top_arc_center = plane.Origin + alignment * (height / 2 - top_arc_radius)
        top_arc = rg.Arc(top_arc_center, top_arc_radius, math.pi * arc_angle_domain_relative_pi).ToNurbsCurve()
        
        # Create the bottom arc
        bottom_arc_center = plane.Origin - alignment * (height / 2 - bottom_arc_radius)
        bottom_arc = rg.Arc(bottom_arc_center, bottom_arc_radius, math.pi * arc_angle_domain_relative_pi).ToNurbsCurve()
        # Flip the bottom arc
        bottom_arc.Rotate(math.pi, normal, bottom_arc_center)
        bottom_arc.Reverse()
        line_between_arcs = rg.Curve.CreateBlendCurve(top_arc, bottom_arc ,rg.BlendContinuity.Position)
        
        curveList = List[rg.Curve]()
        curveList.Add(top_arc)
        curveList.Add(line_between_arcs)
        curveList.Add(bottom_arc)
        
        s_shape_rail = rg.Curve.JoinCurves(curveList)[0]
        
        # Create the body by pipe around the rail
        local_blending = True
        fit_rail = True
        s_shape_hook_body = rg.Brep.CreatePipe(s_shape_rail, thickness, local_blending, rg.PipeCapMode.Round, fit_rail, TOLERANCE, TOLERANCE)[0]
        print("INFO: create_s_shape_hook_body - return", s_shape_hook_body)
        return s_shape_hook_body

    except Exception as error:
        print("ERROR: create_s_shape_hook_body ", "An error occurred:", traceback.format_exc())
        return None

# Generate input sliders by (name,value,min,max)
# input_list = [
#     InputSlider('body_top_arc_radius', 10, 5, 50),
#     InputSlider('body_bottom_arc_radius', 15, 5, 50),
#     InputSlider('body_height', 60, 10, 100),
#     InputSlider('body_thickness', 2.0, 0.1, 10),
#     InputSlider('body_arc_angle_domain_relative_pi', 1.25, 0.1, 2),
#     ]
# create_params(input_list)

# User Parameters:
try:
    sliders_value = locals()['sliders_value']
    body_top_arc_radius = float(sliders_value['body_top_arc_radius'])
    body_bottom_arc_radius = float(sliders_value['body_bottom_arc_radius'])
    body_height = float(sliders_value['body_height'])
    body_thickness = float(sliders_value['body_thickness'])
    body_arc_angle_domain_relative_pi = float(sliders_value['body_arc_angle_domain_relative_pi'])
except:
    body_top_arc_radius = 10
    body_bottom_arc_radius = 15
    body_height = 60
    body_thickness = 2
    body_arc_angle_domain_relative_pi = 1.25


# Internal Parameters:
body_alignment = rg.Vector3d.YAxis
body_origin = rg.Point3d(0, 0, 0)
body_normal = rg.Vector3d.ZAxis

# Assembling
s_shape_hook_body = create_s_shape_hook_body(body_origin, body_normal, body_alignment, body_top_arc_radius, body_bottom_arc_radius, body_height, body_thickness, body_arc_angle_domain_relative_pi)

# Return created object by placing it in variable a
a = [s_shape_hook_body]

b = {"body_top_arc_radius": [5, 50, body_top_arc_radius], "body_bottom_arc_radius": [5, 50, body_bottom_arc_radius],
     "body_height": [10, 100, body_height], "body_thickness": [0.1, 10, body_thickness], "body_arc_angle_domain_relative_pi": [0.1, 2, body_arc_angle_domain_relative_pi]}


