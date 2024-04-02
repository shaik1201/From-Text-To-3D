import Rhino
import Rhino.Geometry as rg
import traceback
import math

TOLERANCE = Rhino.RhinoDoc.ActiveDoc.ModelAbsoluteTolerance

def create_measuring_jug_body(origin, normal, alignment, top_radius, base_radius, spout_length, height, relative_height):
    """
    This function creates a 3D model of a measuring jug body. 
    The measuring jug body is modeled as a cylindrical shape divided into an upper part featuring a spout and a lower part

    Parameters:
        origin (Rhino.Geometry.Point3d): the origin of the measuring jug body plane
        normal (Rhino.Geometry.Vector3d): the normal of measuring jug body plane
        alignment (Rhino.Geometry.Vector3d): the axis in which the spout and the handle located 
        base_radius (float): the radius of the base of the measuring jug body
        top_radius (float): the radius of the top of the measuring jug body
        height (float): the measuring jug body height
        spout_length (float): the distance from the top circle to the edge of the jug spout
        relative_height (float): the spout height

    Return: 
        list: List of curves representing the measuring jug body
    """
    try:
        print("INFO: create_measuring_jug_body - start", locals())
        # Create a plane to locate the measuring jug body
        body_plane = rg.Plane(origin, normal)

        # Create the base circle of the measuring jug body
        base_circle = rg.Circle(body_plane, base_radius).ToNurbsCurve()


        # Calculate the radius of the spout bottom circle that separates the upper part with the spout and the lower part of the body 
        spout_bottom_radius = base_radius + (top_radius - base_radius) * relative_height

        # Create the spout bottom circle
        spout_bottom_plane = rg.Plane(body_plane)
        spout_bottom_plane.Translate(spout_bottom_plane.Normal * (height * relative_height))
        spout_bottom_circle = rg.Circle(spout_bottom_plane, spout_bottom_radius).ToNurbsCurve()

        # Tween curves,takes two curves and completes additional curves according to a parameter for making the lower part of the body smoother
        number_of_curves = ((height * relative_height) / (height - (height * relative_height))) - 1 # Makes the distance between all curves equal
        tweened = rg.Curve.CreateTweenCurves(base_circle, spout_bottom_circle, int(number_of_curves))

        # Create the top circle of the upper part with the spout that construct from a circle and a triangle
        top_plane = rg.Plane(origin + normal * height, normal)
        top_circle = rg.Circle(top_plane, top_radius).ToNurbsCurve()

        # Determine the points on the top circle circumference to create the triangle
        # Use the angles to evenly divide the circle into equal parts to form a triangle
        first_corner_location = math.pi / 4 
        second_corner_location = 3 * math.pi / 4 
        edge_location = math.pi / 2 

        # Find the triangle corners on the top circle
        triangle_corner1 = top_circle.PointAt(first_corner_location) 
        triangle_corner2 = top_circle.PointAt(second_corner_location)
        triangle_edge = top_circle.PointAt(edge_location)

        # Move the triangle_edge along the handle normal to determine the spout length
        triangle_edge = triangle_edge + (alignment * spout_length)

        # Create the traingle
        triangle = rg.Polyline([triangle_corner1, triangle_corner2 , triangle_edge, triangle_corner1]).ToNurbsCurve()

        # Perform region union to create the top shape of the body
        curves_to_union = [top_circle, triangle]
        union_result = rg.Curve.CreateBooleanUnion(curves_to_union, TOLERANCE)
        if union_result:
            top_shape = union_result[0] 

            # Create the list of curves to loft
            curves_to_loft = [top_shape, spout_bottom_circle] + list(tweened) + [base_circle]

            # Sort the curves by their Z-axis coordinates (low to high) 
            curves_to_loft.sort(key=lambda curve: min(point.Location.Z for point in curve.Points))

            # Create the measuring jug by lofting the curves that defines the shape of the body
            closed = False
            loft = rg.Brep.CreateFromLoft(curves_to_loft, rg.Point3d.Unset, rg.Point3d.Unset, rg.LoftType.Normal, closed)[0]
        else:
            loft = None

        print("INFO: create_measuring_jug_body - return", loft)
        return loft
    except Exception as error:
        print("ERROR: create_measuring_jug_body ", "An error occurred:", traceback.format_exc())
        return None

def create_measuring_jug_base(origin, normal, radius):
    """
    This function creates a 3D model of a measuring jug base. 
    The measuring jug base is modeled as a flat surface in a circular shape at the bottom of the measuring jug.

    Parameters:
        origin (Rhino.Geometry.Point3d): the origin of the measuring jug base plane
        normal (Rhino.Geometry.Vector3d): the normal of the measuring jug base plane
        radius (float): the radius of the measuring jug base

    Return: 
        Rhino.Geometry.Brep: 3D model of the measuring jug
    """
    try:
        print("INFO: measuring_jug_base - start", locals())
        # Create a plane to locate the measuring jug base
        base_plane = rg.Plane(origin, normal)

        # Create the measuring jug base
        base_circle = rg.Circle(base_plane, radius).ToNurbsCurve()
        measuring_jug_base = rg.Brep.CreatePlanarBreps(base_circle, TOLERANCE)[0]  

        print("INFO: measuring_jug_base - return", measuring_jug_base)
        return measuring_jug_base
    except Exception as error:
        print("ERROR: measuring_jug_base ", "An error occurred:", traceback.format_exc())
        return None

def create_measuring_jug_handle(origin, normal, alignment, top_face_length, side_face_length, thickness, width):
    """
    Create a 3D model of a measuring jug handle
    The handle is modeled a flipped L-shaped structure, sits directly opposite to the spout's direction.

    Parameters:
        origin (Rhino.Geometry.Point3d): the origin of the measuring jug body plane
        normal (Rhino.Geometry.Vector3d): the normal of measuring jug body plane
        alignment (Rhino.Geometry.Vector3d): the axis in which the spout and the handle located
        top_face_length (float): the length of the top part of the handle
        side_face_length (float): the length of the bottom part of the handle
        thickness (float): the thickness of the handle
        width (float): the width of the handle

    Returns:
    Rhino.Geometry.Brep: The created The created measuring jug handle
    """
    try:
        print("INFO: create_measuring_jug_handle - start", locals())
        # Generate a series of points to create a polyline that represent the handle L shape
        polyline_start_pt = origin
        polyline_middle_pt = polyline_start_pt + (normal * top_face_length)
        polyline_end_pt = polyline_middle_pt + (alignment * side_face_length)
        polyline_pts = polyline_start_pt, polyline_middle_pt, polyline_end_pt

        # Create the polyline that represents the handle L shape and will be used as a rail for sweeping.
        polyline_rail = rg.Polyline(polyline_pts).ToNurbsCurve()

        # Create a rectangle that defines the handle section
        sweep_rectangle_plane = rg.Plane(origin, normal)
        handle_rectangle = rg.Rectangle3d(sweep_rectangle_plane, rg.Interval(thickness / 2, - thickness / 2), rg.Interval(-width / 2, width / 2 )).ToNurbsCurve()

        # Sweep the rectangle along the handle shape to create the handle
        closed = False
        handle = rg.Brep.CreateFromSweep(polyline_rail, handle_rectangle, closed, TOLERANCE)[0]

        print("INFO: create_measuring_jug_handle - return", handle)
        return handle
    except Exception as error:
        print("ERROR: create_measuring_jug_handle ", "An error occurred:", traceback.format_exc())
        return None

# Generate input sliders by (name,value,min,max)
input_list = [
    InputSlider('body_base_radius', 60, 10, 900),
	InputSlider('body_top_radius', 70, 10, 900),
    InputSlider('body_height', 100, 10, 300),
	InputSlider('spout_relative_height', 0.8, 0.1, 1.0),
	InputSlider('jug_spout_length', 10, 1, 100),
	InputSlider('handle_thickness', 2, 0, 20),
	InputSlider('handle_top_face_length', 20, 5, 100),
	InputSlider('handle_side_face_length', 70, 5, 100),
	InputSlider('handle_width', 20, 5, 100),
]
create_params(input_list)

# User Parameters:
try: body_base_radius
except: body_base_radius = 60

try: body_top_radius
except: body_top_radius = 70

try: body_height
except: body_height = 100

try: spout_relative_height
except: spout_relative_height = 0.8

try: jug_spout_length
except: jug_spout_length = 10

try: handle_thickness
except: handle_thickness = 2

try: handle_top_face_length
except: handle_top_face_length = 20

try: handle_side_face_length
except: handle_side_face_length = 70

try: handle_width
except: handle_width = 20

# Parameters
body_origin = rg.Point3d(0, 0, 0)
body_normal = rg.Vector3d.ZAxis
body_alignment = rg.Vector3d.YAxis

base_origin = body_origin 
base_normal = body_normal
base_radius = body_base_radius

handle_origin = rg.Point3d(0, -body_top_radius, body_height-handle_thickness/2)
handle_normal = - body_normal.YAxis
handle_alignment = - body_normal.ZAxis

# Assembling
measuring_jug_body = create_measuring_jug_body(body_origin, body_normal, body_alignment, body_top_radius, body_base_radius, jug_spout_length, body_height, spout_relative_height)
measuring_jug_base = create_measuring_jug_base(base_origin, base_normal, base_radius)
measuring_jug_handle = create_measuring_jug_handle(handle_origin, handle_normal, handle_alignment, handle_top_face_length, handle_side_face_length, handle_thickness)

# Return the created object by placing it in variable a
a = [measuring_jug_body, measuring_jug_base, measuring_jug_handle]
