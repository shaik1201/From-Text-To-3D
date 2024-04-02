import rhinoinside
rhinoinside.load()
import Rhino.Geometry as rg
import traceback

print('finished loading rhinoinside')
TOLERANCE = 0.01


def create_plate_rim(origin, normal, radius, height, thickness):
    """
    This function creates a 3D model of a plate rim. 
    The rim is modeled as a cylinder that is placed on the top edge of the plate body.

    Parameters:
        origin (Rhino.Geometry.Point3d): the origin of the plate rim plane
        normal (Rhino.Geometry.Vector3d): the normal of plate rim plane 
        radius (float): the radius of the plate rim
        height (float): the height of the plate rim
        thickness (float): the thickness of the plate rim

    Return: 
        Rhino.Geometry.Brep: the created 3D model
    """
    try:
        print("INFO: create_plate_rim - start", locals())
        # Create plane to locate the rim
        rim_plane = rg.Plane(origin, normal)

        # Create the rim
        rim_bottom_circle = rg.Circle(rim_plane, radius)
        rim_top_circle = rg.Circle(rim_plane, radius)
        rim_top_circle.Translate(normal * height)
        rim = rg.Brep.CreateFromLoft([rim_bottom_circle.ToNurbsCurve(), rim_top_circle.ToNurbsCurve()], rg.Point3d.Unset, rg.Point3d.Unset, rg.LoftType.Normal, False)[0]

        print("INFO: create_plate_rim - return", rim)
        return rim
    except Exception as error:
        print("ERROR: create_plate_rim ", "An error occurred:", traceback.format_exc())
        return None


# Parameters
body_radius = 100
body_origin = rg.Point3d(0, 0, 0)
body_normal = rg.Vector3d.ZAxis

rim_radius = body_radius
rim_height = 2
rim_thickness = 2
rim_origin = body_origin
rim_normal = body_normal

# Assembling
plate_rim = create_plate_rim(rim_origin, rim_normal, rim_radius, rim_height, rim_thickness)

# Return the created object by placing it in variable a
a = plate_rim