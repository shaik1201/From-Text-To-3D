import Rhino
import Rhino.Geometry as rg
import traceback

TOLERANCE = Rhino.RhinoDoc.ActiveDoc.ModelAbsoluteTolerance

def create_pot_body(origin, normal, radius, height):
    """
    This function creates a 3D model of a cooking pot body. 
    The body is modeled as a cylinder.
    
    Parameters:
        origin (Rhino.Geometry.Point3d): origin of the pot body plane
        normal (Rhino.Geometry.Vector3d): normal of pot body plane 
        radius (float): the radius of the pot 
        height (float): the height of the pot
    
    Return: 
        Rhino.Geometry.Brep: 3D model of the pot body
    """
    try:
        print("INFO: create_pot_body - start", locals())
        # Create plane to locate the body
        plane = rg.Plane(origin, normal)

        # Create the base circle at the bottom of the pot
        base_circle = rg.Circle(plane, radius)
        cylinder = rg.Cylinder(base_circle, height)
        cap_bottom = False
        cap_top = False
        pot = cylinder.ToBrep(cap_bottom, cap_top)
        print("INFO: create_pot_body - return", pot)
        return pot
    except Exception as error:
        print("ERROR: create_pot_body ", traceback.format_exc())
        return None

def create_pot_base(origin, normal, radius):
    """
    This function creates a 3D model of a pot base. 
    The base is modeled as a circle at the base of the pot.

    Parameters:
        origin (Rhino.Geometry.Point3d): origin of the pot base plane
        normal (Rhino.Geometry.Vector3d): normal of pot base plane 
        radius (float): the radius of the base

    Return: 
        Rhino.Geometry.Circle: the created circle
    """
    try:
        print("INFO: create_pot_base - start", locals())
        # Create plane to locate the base
        plane = rg.Plane(origin, normal)

        # Create the base circle
        base_circle = rg.Circle(plane, radius)
        base = rg.Brep.CreatePlanarBreps(base_circle.ToNurbsCurve(), TOLERANCE)[0]

        print("INFO: create_pot_base - return", base)
        return base
    except Exception as error:
        print("ERROR: create_pot_base ", "An error occurred:", traceback.format_exc())
        return None

def create_pot_handle(origin, normal, alignment, radius, thickness):
    """
    Create a 3D model of a pot handle
    The handle is modeled as a slightly elongated semi-circle or crescent

    Parameters:
        origin (Rhino.Geometry.Point3d): origin of the shape
        normal (Rhino.Geometry.Vector3d): normal of the shape
        alignmen (Rhino.Geometry.Vector3d): The direction to define the start and end point of the semi circle
        radius (float): the radius of the shape
        thickness (float): The thickness of the pipe

    Returns:
    Rhino.Geometry.Brep: The created pipe
    """
    try:
        print("INFO: create_pot_handle - start", locals())
        # Create arc
        start_point = origin + (alignment * radius)
        end_point = origin - (alignment * radius)
        semi_circle = rg.Arc(start_point, normal, end_point).ToNurbsCurve()

        # Create a circle at the start of the semi-circle for the thickness
        start_point_plane = rg.Plane(semi_circle.PointAtStart, semi_circle.TangentAtStart)
        shape_circle = rg.Circle(start_point_plane, thickness/2)

        # Sweep the shape circle along the semi-circle
        closed = False
        pipe = rg.Brep.CreateFromSweep(semi_circle, shape_circle.ToNurbsCurve(), closed, TOLERANCE)[0]
        print("INFO: create_pot_handle - return", pipe)
        return pipe
    except Exception as error:
        print("ERROR: create_pot_handle ", "An error occurred:", traceback.format_exc())
        return None

def create_pot_rim(origin, normal, external_radius, thickness):
    """
    This function creates a 3D model of a pot rim. 
    The rim is modeled as a torus.
    
    Parameters:
        origin (Rhino.Geometry.Point3d): origin of the pot rim plane
        normal (Rhino.Geometry.Vector3d): normal of pot rim plane 
        external_radius (float): the external radius of the torus
        thickness (float): the thickness of the torus
    
    Return: 
        Rhino.Geometry.Brep: 3D model of the rim
    """
    try:
        print("INFO: create_pot_rim - start", locals())
        # Create plane to locate the rim
        plane = rg.Plane(origin, normal)
        
        # Create the rim surface
        external_circle = rg.Circle(plane, external_radius)
        internal_radius = external_radius - thickness
        internal_circle = rg.Circle(plane, internal_radius)
        
        # Create the lid by lofting the two circles
        closed = False
        rim = rg.Brep.CreateFromLoft([external_circle.ToNurbsCurve(), internal_circle.ToNurbsCurve()], rg.Point3d.Unset, rg.Point3d.Unset, rg.LoftType.Normal, closed)[0]
        
        print("INFO: create_pot_rim - return", rim)
        return rim
    except Exception as error:
        print("ERROR: create_pot_rim ", "An error occurred:", traceback.format_exc())
        return None

def create_pot_lid(origin, normal, bottom_radius, height, top_radius):
    """
    This function creates a 3D model of a pot lid. 
    The lid is modeled as a slightly domed circular piece.
    
    Parameters:
        origin (Rhino.Geometry.Point3d): origin of the pot lid plane
        normal (Rhino.Geometry.Vector3d): normal of pot lid plane 
        bottom_radius (float): the bottom radius of the lid 
        height (float): the height of the lid
        top_radius (float): the top radius of the lid
    
    Return: 
    Rhino.Geometry.Brep: 3D model of the lid
    """
    try:
        print("INFO: create_pot_lid - start", locals())
        # Create plane to locate the lid
        plane = rg.Plane(origin,normal)
        
        # Create the base circle at the bottom of the lid
        base_circle = rg.Circle(plane, bottom_radius).ToNurbsCurve()
        
        # Create the top circle at the top of the lid
        top_plane = rg.Plane(plane)
        top_plane.Translate(plane.Normal*height)
        top_circle = rg.Circle(top_plane, top_radius).ToNurbsCurve()
        
        # Create the lid by lofting the two circles
        closed = False
        lid = rg.Brep.CreateFromLoft([base_circle, top_circle], rg.Point3d.Unset, rg.Point3d.Unset, rg.LoftType.Normal, closed)[0]
        
        print("INFO: create_pot_lid - return", lid)
        return lid
    except Exception as error:
        print("ERROR: create_pot_lid", "An error occurred:", traceback.format_exc())
        return None

def create_pot_lid_handle(origin, normal, radius):
    """
    This function creates a 3D model of a pot lid handle. 
    The handle is modeled as a semi-sphere.

    Parameters:
        origin (Rhino.Geometry.Point3d): origin of the pot lid handle plane
        normal (Rhino.Geometry.Vector3d): normal of pot lid handle plane 
        radius (float): the radius of the semi-sphere

    Return: 
    Rhino.Geometry.Brep: 3D model of the handle
    """
    try:
        print("INFO: create_pot_lid_handle - start", locals())
        # Create plane to locate the handle
        plane = rg.Plane(origin, normal)

        # Create the sphere
        sphere = rg.Sphere(plane, radius)
        brep_sphere = rg.Brep.CreateFromSphere(sphere)

        # Create a cutting brep
        interval = rg.Interval(-radius, radius)
        cutting_brep = rg.PlaneSurface(plane, interval, interval).ToBrep()
        split_breps = brep_sphere.Split(cutting_brep, TOLERANCE)
        semi_sphere = [brep for brep in split_breps if brep.IsValid][0] #The first item in the list contain the upper half of the sphere

        print("INFO: create_pot_lid_handle - return", semi_sphere)
        return semi_sphere
    except Exception as error:
        print("ERROR: create_pot_lid_handle ", "An error occurred:", traceback.format_exc())
        return None


# Generate input sliders by (name,value,min,max)
input_list = [
    InputSlider('body_radius', 150, 10, 300),
    InputSlider('body_height', 130, 10, 300),
    InputSlider('rim_thickness', 10, 1, 50),
    InputSlider('lid_bottom_radius', 145, 10, 300),
    InputSlider('lid_height', 30, 10, 100),
    InputSlider('lid_handle_radius', 10, 5, 50),
    InputSlider('handle_radius', 30, 10, 200),
    InputSlider('handle_thickness', 20, 5, 50),
    InputSlider('handle_relative_height', 0.9, 0.0, 1.0)
]
create_params(input_list)

# User Parameters:
try: body_radius
except: body_radius = 150

try: body_height
except: body_height = 130

try: rim_thickness
except: rim_thickness = 10

try: lid_bottom_radius
except: lid_bottom_radius = 145

try: lid_height
except: lid_height = 30

try: lid_handle_radius
except: lid_handle_radius = 10

try: handle_radius
except: handle_radius = 30

try: handle_thickness
except: handle_thickness = 20

try: handle_relative_height
except: handle_relative_height = 0.9


# Internal Parameters:
body_origin = rg.Point3d(0, 0, 0)
body_normal = rg.Vector3d.ZAxis

base_radius = body_radius
base_origin = body_origin
base_normal = body_normal

rim_external_radius = body_radius
rim_origin = rg.Point3d(0, 0, body_height)
rim_normal = body_normal

lid_top_radius = lid_handle_radius
lid_origin = rg.Point3d(0, 0, body_height)
lid_normal = body_normal

lid_handle_origin = rg.Point3d(0, 0, body_height+lid_height)
lid_handle_normal = rg.Vector3d(lid_normal)

handle_alignment = body_normal.YAxis
right_handle_origin = rg.Point3d(body_radius,0, body_height * handle_relative_height)
right_handle_normal = body_normal.XAxis
left_handle_origin = rg.Point3d(-body_radius,0, body_height * handle_relative_height)
left_handle_normal = -body_normal.XAxis

# Assembling
pot_body = create_pot_body(body_origin, body_normal, body_radius, body_height)
pot_base = create_pot_base(base_origin, base_normal, base_radius)
pot_rim = create_pot_rim(rim_origin, rim_normal, rim_external_radius, rim_thickness)
pot_lid = create_pot_lid(lid_origin, lid_normal, lid_bottom_radius, lid_height, lid_top_radius)
pot_lid_handle = create_pot_lid_handle(lid_handle_origin, lid_handle_normal, lid_handle_radius)
pot_right_handle = create_pot_handle(right_handle_origin, right_handle_normal, handle_alignment, handle_radius, handle_thickness)
pot_left_handle = create_pot_handle(left_handle_origin, left_handle_normal, handle_alignment, handle_radius, handle_thickness)

# Return created object by placing it in variable a
a = [pot_base, pot_body, pot_lid, pot_rim, pot_lid_handle, pot_right_handle, pot_left_handle]