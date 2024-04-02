"""
Alessi Kettle Plisse 
Plisse Kettle Body: A truncated cone shape with a flat bottom and pleated surface. The texture consists of vertical ridges and valleys that run parallel to the height of the kettle.
Parameters: kettle_height, kettle_bottom_radius, kettle_upper_radius, pleats_count, pleat_depth
Orientation: kettle_origin=(0,0,0), kettle_normal=ZAxis
"""
import Rhino
import Rhino.Geometry as rg
import traceback
import math

TOLERANCE = Rhino.RhinoDoc.ActiveDoc.ModelAbsoluteTolerance

BASE_PLANE = rg.Plane.WorldXY
DEFAULT_BREP = rg.Brep.CreateFromSphere(rg.Sphere(BASE_PLANE, 10))


def create_pleated_cone_kettle_body(origin, normal, bottom_radius, top_radius, height, pleats, pleat_depth):
    """
    Create a truncated cone with a pleated texture.

    Parameters:
        origin (Rhino.Geometry.Point3d): origin of the kettle
        normal (Rhino.Geometry.Vector3d): normal of kettle
        bottom_radius (float): Radius of the bottom circle.
        top_radius (float): Radius of the top circle.
        height (float): Height of the cone.
        pleats (int): Number of pleats in the texture.
        pleat_depth (float): Depth of each pleat.

    Returns:
        Rhino object ID of the created pleated cone.
    """
    try:
        print("INFO: create_pleated_cone_kettle_body - start", locals())
        # Create plane to locate the body
        plane = rg.Plane(origin, normal)

        # Create the base circle at the bottom of the kettle
        bottom_circle = rg.Circle(plane, bottom_radius).ToNurbsCurve()

        # Divide the circles into points
        includeEnds = True
        bottom_points = [bottom_circle.PointAt(
            t) for t in bottom_circle.DivideByCount(pleats, includeEnds)]

        # Adjust bottom points to create a zigzag pattern
        zigzag_bottom_points = []
        for i, point in enumerate(bottom_points):
            angle = math.atan2(point.Y, point.X)
            new_radius = bottom_radius + \
                (pleat_depth if i % 2 == 0 else -pleat_depth)
            x = new_radius * math.cos(angle)
            y = new_radius * math.sin(angle)
            zigzag_point = rg.Point3d(x, y, point.Z)
            zigzag_bottom_points.append(zigzag_point)
        zigzag_bottom_points.append(zigzag_bottom_points[0])

        # Interpolate curves through the points
        degree = 3
        bottom_curve = rg.Curve.CreateInterpolatedCurve(
            zigzag_bottom_points, degree, rg.CurveKnotStyle.UniformPeriodic)

        # Create curve at top of the kettle
        top_curve = bottom_curve.Duplicate()
        top_curve.Scale(top_radius/bottom_radius)
        top_curve.Translate(0, 0, height)

        # Loft between the two curves
        closed = False
        loft = rg.Brep.CreateFromLoft(
            [bottom_curve, top_curve], rg.Point3d.Unset, rg.Point3d.Unset, rg.LoftType.Normal, closed)

        # Create kettle base
        base = rg.Brep.CreatePlanarBreps(
            bottom_curve.ToNurbsCurve(), TOLERANCE)

        kettle = rg.Brep.JoinBreps(loft + base, TOLERANCE)[0]
        print("INFO: create_pleated_cone_kettle_body - return", kettle)
        return kettle
    except Exception as error:
        print("ERROR: create_pleated_cone_kettle_body ", traceback.format_exc())
        return DEFAULT_BREP


# Parameters
kettle_origin = rg.Point3d(0, 0, 0)
kettle_normal = rg.Vector3d.ZAxis
kettle_bottom_radius = 80
kettle_top_radius = 60
kettle_height = 200
pleats_count = 30
pleat_depth = 5

a = create_pleated_cone_kettle_body(kettle_origin, kettle_normal, kettle_bottom_radius,
                                    kettle_top_radius, kettle_height, pleats_count, pleat_depth)
