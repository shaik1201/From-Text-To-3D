import rhinoinside
rhinoinside.load()
import Rhino.Geometry as rg
import traceback
import math

print('finished loading rhinoinside')
TOLERANCE = 0.01


def create_plate_body(origin, normal, radius, height):
    """
    This function creates a 3D model of a plate body. 
    The body is modeled as a cylinder.

    Parameters:
        origin (Rhino.Geometry.Point3d): origin of the plate body plane
        normal (Rhino.Geometry.Vector3d): normal of plate body plane
        radius (float): the radius of the plate body
        height (float): the height of the plate body

    Return: 
        Rhino.Geometry.Brep: the created 3D model
    """
    try:
        print("INFO: create_plate_body - start", locals())
        # Create plane to locate the body
        plate_body_plane = rg.Plane(origin, normal)

        # Create the plate body
        plate_body_circle = rg.Circle(plate_body_plane, radius)
        plate_body = rg.Brep.CreatePlanarBreps(plate_body_circle.ToNurbsCurve(), TOLERANCE)[0]

        print("INFO: create_plate_body - return", plate_body)
        return plate_body
    except Exception as error:
        print("ERROR: create_plate_body ", "An error occurred:", traceback.format_exc())
        return None


# Parameters
body_radius = 100
body_height = 10
body_origin = rg.Point3d(0, 0, 0)
body_normal = rg.Vector3d.ZAxis

# Assembling
plate = create_plate_body(body_origin, body_normal, body_radius, body_height)

# Return the created object by placing it in variable a
a = plate