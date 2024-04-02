import Rhino
import Rhino.Geometry as rg
import traceback

TOLERANCE = Rhino.RhinoDoc.ActiveDoc.ModelAbsoluteTolerance

def create_kettle_body(origin, normal, bottom_radius, upper_radius, height):
    """
    This function creates a 3D model of a kettle body. 
    The body is modeled as a truncated cone.

    Parameters:
        origin (Rhino.Geometry.Point3d): origin of the kettle body plane
        normal (Rhino.Geometry.Vector3d): normal of kettle body plane 
        bottom_radius (float): the radius of the bottom of the kettle 
        upper_radius (float): the radius of the upper part of the kettle 
        height (float): the height of the kettle

    Return:
        Rhino.Geometry.Brep: the created kettle body
    """
    try:
        print("INFO: create_kettle_body - start", locals())
        # Create plane to locate the body
        plane = rg.Plane(origin, normal)

        # Create the base circle at the bottom of the kettle
        base_circle = rg.Circle(plane, bottom_radius).ToNurbsCurve()

        # Create the top circle at the top of the kettle
        top_plane = rg.Plane(origin + normal * height, normal)
        top_circle = rg.Circle(top_plane, upper_radius).ToNurbsCurve()

        # Create the kettle body by lofting the two circles
        closed = False
        kettle = rg.Brep.CreateFromLoft([base_circle, top_circle], rg.Point3d.Unset, rg.Point3d.Unset, rg.LoftType.Normal, closed)[0]

        print("INFO: create_kettle_body - return", kettle)
        return kettle
    except Exception as error:
        print("ERROR: create_kettle_body", "An error occurred:", traceback.format_exc())
        return None

def create_kettle_base(origin, normal, radius):
    """
    This function creates a 3D model of a kettle base. 
    The base is modeled as a circle at the bottom of the kettle.

    Parameters:
        origin (Rhino.Geometry.Point3d): origin of the kettle base plane
        normal (Rhino.Geometry.Vector3d): normal of kettle base plane 
        radius (float): the radius of the base

    Return: 
        Rhino.Geometry.Circle: the created circle
    """
    try:
        print("INFO: create_kettle_base - start", locals())
        # Create plane to locate the base
        plane = rg.Plane(origin, normal)

        # Create the base circle
        base_circle = rg.Circle(plane, radius).ToNurbsCurve()
        base = rg.Brep.CreatePlanarBreps(base_circle,TOLERANCE)[0]
        
        print("INFO: create_kettle_base - return", base)
        return base
    except Exception as error:
        print("ERROR: create_kettle_base ", "An error occurred:", traceback.format_exc())
        return None

def create_kettle_handle(origin, normal, alignment, length, height, thickness):
    """
    Create a 3D model of a kettle handle
    The handle is modeled as a semi-circle or arc

    Parameters:
        origin (Rhino.Geometry.Point3d): origin of the handle - center of handle circle
        normal (Rhino.Geometry.Vector3d): normal of handle plane - tangent of handle
        alignmen (Rhino.Geometry.Vector3d): The direction to define the start and end point of the handle in relation to the origin
        length (float): the length of the handle
        height (float): The height of the handle
        thickness (float): The thickness of the handle

    Returns:
        Rhino.Geometry.Brep: The created semi cylinder
    """
    try:
        print("INFO: create_kettle_handle - start", locals())
        # Create semi circle
        radius = length / 2
        handle_start_point = origin + (alignment * radius)
        handle_end_point = origin - (alignment * radius)
        semi_circle = rg.Arc(handle_start_point, normal, handle_end_point).ToNurbsCurve()

        # Scale the semi-circle to create an elongated semi-circle or crescent
        plane = rg.Plane(origin, normal)
        transform = rg.Transform.Scale(plane, 1, 1, height / radius)
        semi_circle.Transform(transform)

        # Create a circle at the start of the semi-circle for the thickness
        start_point_plane = rg.Plane(semi_circle.PointAtStart, semi_circle.TangentAtStart)
        shape_circle = rg.Circle(start_point_plane, thickness / 2)

        # Sweep the shape circle along the semi-circle to create the handle
        closed = False
        handle = rg.Brep.CreateFromSweep(semi_circle, shape_circle.ToNurbsCurve(), closed, TOLERANCE)[0]
        print("INFO: create_kettle_handle - return", handle)
        return handle
    except Exception as error:
        print("ERROR: create_kettle_handle", "An error occurred:", traceback.format_exc())
        return None

def create_kettle_spout(origin, normal, height, bottom_radius, upper_radius):
    """
    This function creates a 3D model of a kettle spout. 
    The spout is modeled as a conical shape.

    Parameters:
        origin (Rhino.Geometry.Point3d): origin of the kettle spout plane
        normal (Rhino.Geometry.Vector3d): normal of kettle spout plane 
        height (float): the height of the spout 
        bottom_radius (float): the radius of the bottom of the spout
        upper_radius (float): the radius of the top of the spout

    Return:
        Rhino.Geometry.Brep: the created kettle spout
    """
    try:
        print("INFO: create_kettle_spout - start", locals())
        # Create plane to locate the spout
        plane = rg.Plane(origin, normal)

        # Create the base ellipse at the bottom of the spout
        base_ellipse = rg.Ellipse(plane, bottom_radius, bottom_radius*0.5)
        base_circle = base_ellipse.ToNurbsCurve()

        # Create the top ellipse at the top of the spout
        top_plane = rg.Plane(plane)
        top_plane.Translate(plane.Normal * height)
        top_ellipse = rg.Ellipse(top_plane, upper_radius, upper_radius*0.5)
        top_circle = top_ellipse.ToNurbsCurve()

        # Create the kettle spout by lofting the two ellipses
        closed = False
        spout = rg.Brep.CreateFromLoft([base_circle, top_circle], rg.Point3d.Unset, rg.Point3d.Unset, rg.LoftType.Normal, closed)[0]

        print("INFO: create_kettle_spout - return", spout)
        return spout
    except Exception as error:
        print("ERROR: create_kettle_spout", "An error occurred:", traceback.format_exc())
        return None

def create_kettle_rim(origin, normal, external_radius, thickness):
    """
    This function creates a 3D model of a kettle rim. 
    The rim is modeled as a surface between 2 circles.
    
    Parameters:
        origin (Rhino.Geometry.Point3d): origin of the kettle rim plane
        normal (Rhino.Geometry.Vector3d): normal of kettle rim plane 
        external_radius (float): the external radius of the torus
        thickness (float): the thickness of the torus
    
    Return: 
        Rhino.Geometry.Brep: 3D model of the rim
    """
    try:
        print("INFO: create_kettle_rim - start", locals())
        # Create plane to locate the rim
        plane = rg.Plane(origin,normal)
        
        # Create the rim surface
        external_circle = rg.Circle(plane,external_radius)
        internal_radius = external_radius - thickness
        internal_circle = rg.Circle(plane, internal_radius)
        
        # Create the lid by lofting the two circles
        closed = False
        rim = rg.Brep.CreateFromLoft([external_circle.ToNurbsCurve(), internal_circle.ToNurbsCurve()], rg.Point3d.Unset, rg.Point3d.Unset, rg.LoftType.Normal, closed)[0]
        
        print("INFO: create_kettle_rim - return", rim)
        return rim
    except Exception as error:
        print("ERROR: create_kettle_rim ", "An error occurred:", traceback.format_exc())
        return None

def create_kettle_lid(origin, normal, radius, height):
    """
    This function creates a 3D model of a kettle lid. 
    The lid is modeled as a slightly domed circular piece.
    
    Parameters:
        origin (Rhino.Geometry.Point3d): origin of the kettle lid plane
        normal (Rhino.Geometry.Vector3d): normal of kettle lid plane 
        radius (float): the radius of the lid 
        height (float): the height of the lid
    
    Return: 
    Rhino.Geometry.Brep: 3D model of the lid
    """
    try:
        print("INFO: create_kettle_lid - start", locals())
        # Create plane to locate the lid
        plane = rg.Plane(origin,normal)
        
        # Create the base circle at the bottom of the lid
        base_circle = rg.Circle(plane, radius)
        
        # Create the top circle at the top of the lid
        top_plane = rg.Plane(plane)
        top_plane.Translate(plane.Normal*height)
        top_circle = rg.Circle(top_plane, radius * 0.1)
        
        # Create the lid by lofting the two circles
        closed = False
        lid = rg.Brep.CreateFromLoft([base_circle.ToNurbsCurve(), top_circle.ToNurbsCurve()], rg.Point3d.Unset, rg.Point3d.Unset, rg.LoftType.Normal, closed)[0]
        
        print("INFO: create_kettle_lid - return", lid)
        return lid
    except Exception as error:
        print("ERROR: create_kettle_lid ", "An error occurred:", traceback.format_exc())
        return None

def create_kettle_lid_handle(origin, normal, radius):
    """
    This function creates a 3D model of a kettle lid handle. 
    The handle is modeled as a semi-sphere.
    
    Parameters:
        origin (Rhino.Geometry.Point3d): origin of the kettle lid handle plane
        normal (Rhino.Geometry.Vector3d): normal of kettle lid handle plane 
        radius (float): the radius of the semi-sphere
    
    Return: 
        Rhino.Geometry.Brep: 3D model of the handle
    """
    try:
        print("INFO: create_kettle_lid_handle - start", locals())
        # Create plane to locate the handle
        plane = rg.Plane(origin,normal)
        
        # Create the sphere
        sphere = rg.Sphere(plane, radius)
        brep_sphere = rg.Brep.CreateFromSphere(sphere)
        
        # Create a cutting brep
        interval = rg.Interval(-radius,radius)
        cutting_brep = rg.PlaneSurface(plane,interval,interval).ToBrep()
        split_breps = brep_sphere.Split(cutting_brep, TOLERANCE)
        semi_sphere = [brep for brep in split_breps if brep.IsValid][0]
        
        print("INFO: create_kettle_lid_handle - return", brep_sphere)
        return semi_sphere
    except Exception as error:
        print("ERROR: create_kettle_lid_handle ", "An error occurred:", traceback.format_exc())
        return None

# Generate input sliders by (name,value,min,max)
input_list = [
    InputSlider('body_bottom_radius', 150, 10, 300),
    InputSlider('body_upper_radius', 120, 10, 300),
    InputSlider('body_height', 200, 10, 700),
    InputSlider('handle_height', 50, 10, 100),
    InputSlider('handle_thickness', 20, 5, 50),
    InputSlider('spout_height', 100, 5, 300),
    InputSlider('spout_bottom_radius', 22, 5, 100),
    InputSlider('spout_upper_radius', 13, 5, 100),
    InputSlider('spout_relative_height', 0.6, 0.0, 1.0),
    InputSlider('spout_obliquity', 2.2, 0.1, 5.0),
    InputSlider('rim_thickness', 35, 5, 100),
    InputSlider('lid_height', 20, 1, 100),
    InputSlider('lid_handle_radius', 9, 1, 50),
]
create_params(input_list)

# User Parameters:
try: body_bottom_radius
except: body_bottom_radius = 150

try: body_upper_radius
except: body_upper_radius = 120

try: body_height
except: body_height = 200

try: handle_height
except: handle_height = 50

try: handle_thickness
except: handle_thickness = 20

try: spout_height
except: spout_height = 100

try: spout_bottom_radius
except: spout_bottom_radius = 22

try: spout_upper_radius
except: spout_upper_radius = 13

try: spout_relative_height
except: spout_relative_height = 0.6

try: spout_obliquity
except: spout_obliquity = 2.2

try: rim_thickness
except: rim_thickness = 35

try: lid_height
except: lid_height = 20

try: lid_handle_radius
except: lid_handle_radius = 9

# Internal Parameters:
body_origin = rg.Point3d(0, 0, 0)
body_normal = rg.Vector3d.ZAxis

base_radius = body_bottom_radius
base_origin = body_origin
base_normal = body_normal

handle_length = body_upper_radius * 2 - handle_thickness
handle_alignment = body_normal.XAxis
handle_origin = rg.Point3d(0,0,body_height)
handle_normal = body_normal

spout_origin = rg.Point3d(body_bottom_radius + (body_upper_radius-body_bottom_radius)*spout_relative_height,0,body_height * spout_relative_height)
spout_normal = rg.Vector3d(body_normal.XAxis + body_normal.ZAxis*spout_obliquity)

rim_external_radius = body_upper_radius
rim_origin = rg.Point3d(0,0,body_height)
rim_normal = body_normal

lid_radius = rim_external_radius - rim_thickness + 5
lid_origin = rg.Point3d(0,0,body_height)
lid_normal = body_normal

lid_handle_origin = rg.Point3d(0,0,body_height+lid_height)
lid_handle_normal = lid_normal

# Assembling
kettle_body = create_kettle_body(body_origin, body_normal, body_bottom_radius, body_upper_radius, body_height)
kettle_base = create_kettle_base(base_origin, base_normal, base_radius)
kettle_handle = create_kettle_handle(handle_origin, handle_normal, handle_alignment, handle_length, handle_height, handle_thickness)
kettle_spout = create_kettle_spout(spout_origin, spout_normal, spout_height, spout_bottom_radius, spout_upper_radius)
kettle_rim = create_kettle_rim(rim_origin, rim_normal, rim_external_radius, rim_thickness)
kettle_lid = create_kettle_lid(lid_origin, lid_normal, lid_radius, lid_height)
kettle_lid_handle = create_kettle_lid_handle(lid_handle_origin, lid_handle_normal, lid_handle_radius)

# Return created object by placing it in variable a
a = [kettle_body, kettle_base, kettle_handle, kettle_spout, kettle_rim, kettle_lid, kettle_lid_handle]