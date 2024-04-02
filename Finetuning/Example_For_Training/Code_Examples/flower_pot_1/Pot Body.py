import rhinoinside
rhinoinside.load()
import Rhino.Geometry as rg
import traceback
import math

print('finished loading rhinoinside')
TOLERANCE = 0.01


def create_expanding_pot_body(origin, normal, bottom_radius, top_radius, height, edge_protrusion,
                              edge_protrusion_reltaive_height):
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
        protrusion_bottom_circle = rg.Circle(top_plane, top_radius + edge_protrusion).ToNurbsCurve()
        protrusion_top_circle = protrusion_bottom_circle.Duplicate()
        protrusion_top_circle.Translate(normal * height * (1 - edge_protrusion_reltaive_height))

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


# Parameters
body_bottom_radius = 100
body_top_radius = 120
body_height = 100
body_edge_protrusion = 10
body_edge_protrusion_relative_height = 0.8
body_origin = rg.Point3d(0, 0, 0)
body_normal = rg.Vector3d.ZAxis

# Assembling
pot_body = create_expanding_pot_body(body_origin, body_normal, body_bottom_radius, body_top_radius, body_height, body_edge_protrusion, body_edge_protrusion_relative_height)

# Return created object by placing it in variable a
a = pot_body