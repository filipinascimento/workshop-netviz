
"""
==========================================
Earth Coordinate Conversion with a network
==========================================

In this tutorial, we will show how to place actors on specific locations
on the surface of the Earth using a new function.
"""

from fury import window, actor, utils, io
import matplotlib.cm as cm
from fury.data import read_viz_textures, fetch_viz_textures
import math
import numpy as np
import itertools
import igraph as ig
import xnetwork as xn
from math import radians, atan2, asin
import math
from splines.quaternion import UnitQuaternion
from geographiclib.geodesic import Geodesic


def angles2quat(azimuth, elevation, roll):
    return (
        UnitQuaternion.from_axis_angle((0, 0, 1), radians(azimuth)) *
        UnitQuaternion.from_axis_angle((1, 0, 0), radians(elevation)) *
        UnitQuaternion.from_axis_angle((0, 1, 0), radians(roll))
    )


# See https://AudioSceneDescriptionFormat.readthedocs.io/quaternions.html
def quat2angles(quat):
    a, b, c, d = quat.wxyz
    sin_elevation = 2 * (a * b + c * d)
    if 0.999999 < sin_elevation:
        # elevation ~= 90Â°
        return (
            math.degrees(atan2(2 * (a * c + b * d), 2 * (a * b - c * d))),
            90,
            0)
    elif sin_elevation < -0.999999:
        # elevation ~= -90Â°
        return (
            math.degrees(atan2(-2 * (a * c + b * d), 2 * (c * d - a * b))),
            -90,
            0)
    return (
        math.degrees(atan2(2 * (a * d - b * c), 1 - 2 * (b**2 + d**2))),
        math.degrees(asin(sin_elevation)),
        math.degrees(atan2(2 * (a * c - b * d), 1 - 2 * (b**2 + c**2))))

def slerp(one, two, t):
    return (two * one.inverse())**t * one

###############################################################################
# Create a new scene, and load in the image of the Earth using
# ``fetch_viz_textures`` and ``read_viz_textures``. We will use a 16k
# resolution texture for maximum detail.

scene = window.Scene()
g = xn.xnet2igraph("../../Networks/Airports.xnet")

# fetch_viz_textures()
# earth_file = read_viz_textures("1_earth_16k.jpg")
# earth_image = io.load_image(earth_file)
# earth_image = io.load_image("5_night_16k.jpg")
earth_image = io.load_image("1_earth_16k_gray.jpg")
earth_actor = actor.texture_on_sphere(earth_image)


###############################################################################
# Define the function to convert geographical coordinates of a location in
# latitude and longitude degrees to coordinates on the ``earth_actor`` surface.
# In this function, convert to radians, then to spherical coordinates, and
# lastly, to cartesian coordinates.


def latlong_coordinates(lat, lon,radius=1.0):
    # Convert latitude and longitude to spherical coordinates
    degrees_to_radians = math.pi/180.0
    # phi = 90 - latitude
    phi = (90-lat)*degrees_to_radians
    # theta = longitude
    theta = lon*degrees_to_radians*-1
    # now convert to cartesian
    x = radius*np.sin(phi)*np.cos(theta)
    y = radius*np.sin(phi)*np.sin(theta)
    z = radius*np.cos(phi)
    # flipping z to y for FURY coordinates
    return (x, z, y)


###############################################################################
# Use this new function to place some sphere actors on several big cities
# around the Earth.

# locationone = latlong_coordinates(40.730610, -73.935242)  # new york city, us
# locationtwo = latlong_coordinates(39.916668, 116.383331)  # beijing, china
# locationthree = latlong_coordinates(48.864716, 2.349014)  # paris, france

###############################################################################
# Set the centers, radii, and colors of these spheres, and create a new
# ``sphere_actor`` for each location to add to the scene.

# centers = np.array([[*locationone], [*locationtwo], [*locationthree]])
# colors = np.random.rand(3, 3)
# radii = np.array([0.005, 0.005, 0.005])

centers = []
nodeColors = []
scales = []
positions = g.vs["Position"]
degrees = g.strength(weights="weight")
maxDegree = np.max(degrees)
cmap = cm.get_cmap('hot')
for vertexIndex in range(g.vcount()):
    position = positions[vertexIndex]
    degree = degrees[vertexIndex]
    nodeColors.append(cmap((degree/maxDegree)**0.5))
    scales.append(np.sqrt(degree/maxDegree)*0.04)
    centers.append(latlong_coordinates(position[1], position[0], radius=1.01))



# constructing geometry for nodes as a marker actor
nodes = actor.markers(
    centers = np.array(centers),
    colors=nodeColors,
    marker_opacity=1.0,
    scales=np.array(scales),
    # radii=np.array(scales),
    marker="o"
    )

# geometry for edges
lines = []
colors = []
geod = Geodesic.WGS84
weightsArray = g.es["weight"]
maxWeight = max(weightsArray)

edges = np.array(list(zip(g.get_edgelist(),g.es["weight"])),dtype=object)


edgesIndices = np.random.choice(len(edges), 20000,
              p=weightsArray/np.sum(weightsArray),
              replace=False)

for (fromIndex,toIndex),weight in edges[edgesIndices]:

    normWeight = (weight/maxWeight)**0.25
    opacity = normWeight*0.25

    lineSegment = []
    colorSegment = []
    startPosition = positions[fromIndex]
    endPosition = positions[toIndex]
    startColor = np.array([0,0,0,opacity])
    endColor = np.array([0,0,0,opacity])
    startColor[0:3] = np.array(nodeColors[fromIndex])[0:3]
    endColor[0:3] = np.array(nodeColors[toIndex])[0:3]
    # midPosition = ((startPosition[0] + endPosition[0]) / 2, (startPosition[1] + endPosition[1]) / 2)
    lineSegment.append(latlong_coordinates(startPosition[1], startPosition[0], radius=1.01))
    colorSegment.append(startColor)

    g = geod.Inverse(startPosition[1], startPosition[0], endPosition[1], endPosition[0])
    totalDistance = g['s12']
    if totalDistance < 0.00001:
        continue
    l = geod.InverseLine(startPosition[1], startPosition[0], endPosition[1], endPosition[0])
    ds = 100e3;
    n = int(math.ceil(l.s13 / ds))
    for i in range(n + 1):
        # if i == 0:
        #   print("distance latitude longitude azimuth")
        s = min(ds * i, l.s13)
        g = l.Position(s, Geodesic.STANDARD | Geodesic.LONG_UNROLL)
        distance = g['s12']
        latitude = g['lat2']
        longitude = g['lon2']
        coeff = distance/totalDistance
        updowncoeff=math.sin(math.pi*coeff)
        lineSegment.append(latlong_coordinates(latitude, longitude , radius=1.00+totalDistance/5e7*updowncoeff ))
        color = (endColor - startColor) * coeff + startColor
        whiteColor=np.array([1,1,1,opacity])
        color = (whiteColor - color) * (totalDistance/2e7*updowncoeff) + color
        colorSegment.append(color)
    lineSegment.append(latlong_coordinates(endPosition[1], endPosition[0], radius=1.00))
    colorSegment.append(endColor)
    lines.append(lineSegment)
    colors.append(colorSegment)

lineActors = actor.line(lines, colors,linewidth =3)

scene.add(earth_actor)
scene.add(lineActors)
scene.add(nodes)
###############################################################################
# Rotate the Earth to make sure the texture is correctly oriented. Change it's
# scale using ``actor.SetScale()``.

utils.rotate(earth_actor, (-90, 1, 0, 0))
utils.rotate(earth_actor, (180, 0, 1, 0))
earth_actor.SetScale(2, 2, 2)



##############################################################################
# Create a ShowManager object, which acts as the interface between the scene,
# the window and the interactor.

showm = window.ShowManager(scene,
                           size=(900, 768), reset_camera=False,
                           order_transparent=True)

###############################################################################
# Let's create a ``timer_callback`` function to add some animation to the
# Earth. Change the camera position and angle to fly over and zoom in on each
# new location.

counter = itertools.count()


def timer_callback(_obj, _event):
    cnt = next(counter)
    showm.render()
    if cnt == 0:
        scene.set_camera(position=(1.5, 3.5, 7.0))



###############################################################################
# Initialize the ShowManager object, add the timer_callback, and watch the
# new animation take place!

showm.initialize()
showm.add_timer_callback(True, 25, timer_callback)
showm.start()

