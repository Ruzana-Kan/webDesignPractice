import bpy

from PIL import Image
import numpy as np
import math

circle_radius = 2


def rotate(vertices, angle_degrees, axis=(0,1,0)):
    theta_degrees = angle_degrees
    theta_radians = math.radians(theta_degrees)

    rotated_vertices = list(map(lambda v: np.dot(rotation_matrix(axis, theta_radians), v), vertices))
    
    return rotated_vertices



def circle(radius, coordinates):
    (a, b, z) = coordinates

    vertices = []
    for angle in range(0, 360, 10):
      print(angle)
      radians = math.radians(angle)
      x = a + circle_radius * math.cos(radians)
      y = b + circle_radius * math.sin(radians)
      vertices.append((x,y,z))
    
    # for convenience we are duplicating the first vertice and make it also the last vertice
    vertices.append(vertices[0])
    print(len(vertices))
    
    return vertices      


def rotation_matrix(axis, theta):
    """
    Return the rotation matrix associated with counterclockwise rotation about
    the given axis by theta radians.
    """
    axis = np.asarray(axis)
    axis = axis / math.sqrt(np.dot(axis, axis))
    a = math.cos(theta / 2.0)
    b, c, d = -axis * math.sin(theta / 2.0)
    aa, bb, cc, dd = a * a, b * b, c * c, d * d
    bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d
    return np.array([[aa + bb - cc - dd, 2 * (bc + ad), 2 * (bd - ac)],
                     [2 * (bc - ad), aa + cc - bb - dd, 2 * (cd + ab)],
                     [2 * (bd + ac), 2 * (cd - ab), aa + dd - bb - cc]])


test_circle_vertices = circle(10, (0,0,0))

rotated_circle = rotate(test_circle_vertices, 90)
delta_angle=10

donut_vertices = []
per_circle_vertices=0
# i am adding an extra set of points just for cheating
for angle in range(0, 370, delta_angle):
    circle_vertices = circle(10, (10,0,0))
    rotated_circle = rotate(circle_vertices, angle)
    per_circle_vertices = len(circle_vertices)
    donut_vertices += rotated_circle
    
number_rows = int(370 / delta_angle)

faces=[]
for row in range(0, number_rows-1):
    for index in range (0, per_circle_vertices-1):
         vertice1 = index + (row * per_circle_vertices)
         vertice2 = vertice1 + 1
         vertice3 = vertice1 + per_circle_vertices
         vertice4 = vertice2 + per_circle_vertices 
        
         face = (vertice1, vertice3, vertice4, vertice2)
        
        
         faces.append(face)
        

## draw a cylinder
#height = 20
#cilinder_vertices = []
#per_circle_vertices = 0
#for z in np.arange(0.0, height, 0.1):
#    vertices = circle(circle_radius, (0,0, z))
#    cilinder_vertices += vertices
#    per_circle_vertices = len(vertices)

#cilinder_rows = int(height / 0.1)

#faces=[]
#for row in range(0, cilinder_rows-1):
#    for index in range (0, per_circle_vertices-1):
#         vertice1 = index + (row * per_circle_vertices)
#         vertice2 = vertice1 + 1
#         vertice3 = vertice1 + per_circle_vertices
#         vertice4 = vertice2 + per_circle_vertices 
#        
#         face = (vertice1, vertice3, vertice4, vertice2)
#        
#        
#         faces.append(face)
#        

    
new_mesh=bpy.data.meshes.new("new_mesh")
new_mesh.from_pydata(donut_vertices,[],faces)
new_mesh.update()
## make objec from the mesh
new_object = bpy.data.objects.new("donut",new_mesh)
view_layer=bpy.context.view_layer
view_layer.active_layer_collection.collection.objects.link(new_object)


# let's rotate the donut

donut = bpy.data.objects["donut"]

def rotateDonut(donut, angle, axis=(0,0,1)):
    for vert in donut.data.vertices:
        vert.co = rotate([vert.co], angle, axis=axis)[0]
        
for angle in range(0, 360, 10):
    donut.rotation_euler = (math.radians(angle),math.radians(angle),math.radians(angle))    
    donut.keyframe_insert(data_path="rotation_euler", frame=angle)

#
#    rotateDonut(donut, angle)
#    donut.keyframe_insert(data_path="data.vertices", frame=angle)