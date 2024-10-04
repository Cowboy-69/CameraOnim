import math
from datetime import timedelta

import bpy

# Author: AutomaticAddison.com ( https://automaticaddison.com/how-to-convert-euler-angles-to-quaternions-using-python/ )
import numpy as np
def get_quaternion_from_euler(roll, pitch, yaw):
    """
    Convert an Euler angle to a quaternion.

    Input
        :param roll: The roll (rotation around x-axis) angle in radians.
        :param pitch: The pitch (rotation around y-axis) angle in radians.
        :param yaw: The yaw (rotation around z-axis) angle in radians.

    Output
        :return qx, qy, qz, qw: The orientation in quaternion [x,y,z,w] format
    """
    qx = np.sin(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) - np.cos(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
    qy = np.cos(roll/2) * np.sin(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.cos(pitch/2) * np.sin(yaw/2)
    qz = np.cos(roll/2) * np.cos(pitch/2) * np.sin(yaw/2) - np.sin(roll/2) * np.sin(pitch/2) * np.cos(yaw/2)
    qw = np.cos(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
 
    return [qx, qy, qz, qw]

class Exporter:
    file = -1

def writeDuration():
    frameCount = bpy.context.scene.frame_end
    FPS = bpy.context.scene.render.fps
    durationTimeDelta = timedelta(milliseconds=(frameCount / FPS))
    durationInSeconds = durationTimeDelta.microseconds / 1000
    Exporter.file.write("\t" + "Duration " + str(format(durationInSeconds, '.8f')) + "\n")

def writeCameraPosition():
    Exporter.file.write("\t\t" + "CameraPosition Float3 0" + "\n")
    Exporter.file.write("\t\t" + "{" + "\n")
    Exporter.file.write("\t\t\t" + "FramesData MultiChannel" + "\n")
    Exporter.file.write("\t\t\t" + "{" + "\n")
    Exporter.file.write("\t\t\t\t" + "channel" + "\n")
    Exporter.file.write("\t\t\t\t" + "{" + "\n")

    for blenderObject in bpy.context.selected_objects:
        blenderScene = bpy.context.scene

        for i in range(blenderScene.frame_start, blenderScene.frame_end+1):
            blenderScene.frame_set(i)
            Exporter.file.write("\t\t\t\t\t" + str(format(blenderObject.location.x, '.8f')) + "\n")

        Exporter.file.write("\t\t\t\t" + "}" + "\n")
        Exporter.file.write("\t\t\t\t" + "channel" + "\n")
        Exporter.file.write("\t\t\t\t" + "{" + "\n")

        for i in range(blenderScene.frame_start, blenderScene.frame_end+1):
            blenderScene.frame_set(i)
            Exporter.file.write("\t\t\t\t\t" + str(format(blenderObject.location.y, '.8f')) + "\n")

        Exporter.file.write("\t\t\t\t" + "}" + "\n")
        Exporter.file.write("\t\t\t\t" + "channel" + "\n")
        Exporter.file.write("\t\t\t\t" + "{" + "\n")

        for i in range(blenderScene.frame_start, blenderScene.frame_end+1):
            blenderScene.frame_set(i)
            Exporter.file.write("\t\t\t\t\t" + str(format(blenderObject.location.z, '.8f')) + "\n")

        break
    
    Exporter.file.write("\t\t\t\t" + "}" + "\n")
    Exporter.file.write("\t\t\t" + "}" + "\n")
    Exporter.file.write("\t\t" + "}" + "\n")

def writeCameraRotation():
    Exporter.file.write("\t\t" + "CameraRotation Float4 0" + "\n")
    Exporter.file.write("\t\t" + "{" + "\n")
    Exporter.file.write("\t\t\t" + "FramesData MultiChannel" + "\n")
    Exporter.file.write("\t\t\t" + "{" + "\n")
    Exporter.file.write("\t\t\t\t" + "channel" + "\n")
    Exporter.file.write("\t\t\t\t" + "{" + "\n")

    for blenderObject in bpy.context.selected_objects:
        blenderScene = bpy.context.scene

        for i in range(blenderScene.frame_start, blenderScene.frame_end+1):
            blenderScene.frame_set(i)
            rotationInQuaternion = get_quaternion_from_euler(blenderObject.rotation_euler.x - 1.5708, blenderObject.rotation_euler.y, blenderObject.rotation_euler.z)
            Exporter.file.write("\t\t\t\t\t" + str(format(rotationInQuaternion[0], '.8f')) + "\n")

        Exporter.file.write("\t\t\t\t" + "}" + "\n")
        Exporter.file.write("\t\t\t\t" + "channel" + "\n")
        Exporter.file.write("\t\t\t\t" + "{" + "\n")

        for i in range(blenderScene.frame_start, blenderScene.frame_end+1):
            blenderScene.frame_set(i)
            rotationInQuaternion = get_quaternion_from_euler(blenderObject.rotation_euler.x - 1.5708, blenderObject.rotation_euler.y, blenderObject.rotation_euler.z)
            Exporter.file.write("\t\t\t\t\t" + str(format(rotationInQuaternion[1], '.8f')) + "\n")

        Exporter.file.write("\t\t\t\t" + "}" + "\n")
        Exporter.file.write("\t\t\t\t" + "channel" + "\n")
        Exporter.file.write("\t\t\t\t" + "{" + "\n")

        for i in range(blenderScene.frame_start, blenderScene.frame_end+1):
            blenderScene.frame_set(i)
            rotationInQuaternion = get_quaternion_from_euler(blenderObject.rotation_euler.x - 1.5708, blenderObject.rotation_euler.y, blenderObject.rotation_euler.z)
            Exporter.file.write("\t\t\t\t\t" + str(format(rotationInQuaternion[2], '.8f')) + "\n")

        Exporter.file.write("\t\t\t\t" + "}" + "\n")
        Exporter.file.write("\t\t\t\t" + "channel" + "\n")
        Exporter.file.write("\t\t\t\t" + "{" + "\n")

        for i in range(blenderScene.frame_start, blenderScene.frame_end+1):
            blenderScene.frame_set(i)
            rotationInQuaternion = get_quaternion_from_euler(blenderObject.rotation_euler.x - 1.5708, blenderObject.rotation_euler.y, blenderObject.rotation_euler.z)
            Exporter.file.write("\t\t\t\t\t" + str(format(rotationInQuaternion[3], '.8f')) + "\n")

        break
    
    Exporter.file.write("\t\t\t\t" + "}" + "\n")
    Exporter.file.write("\t\t\t" + "}" + "\n")
    Exporter.file.write("\t\t" + "}" + "\n")

def writeCameraFOV():
    Exporter.file.write("\t\t" + "CameraFOV Float 0" + "\n")
    Exporter.file.write("\t\t" + "{" + "\n")
    Exporter.file.write("\t\t\t" + "FramesData SingleChannel" + "\n")
    Exporter.file.write("\t\t\t" + "{" + "\n")

    for blenderObject in bpy.context.selected_objects:
        blenderScene = bpy.context.scene

        for i in range(blenderScene.frame_start, blenderScene.frame_end+1):
            blenderScene.frame_set(i)
            cameraFOV = math.degrees(blenderObject.data.angle)
            Exporter.file.write("\t\t\t\t" + str(format(cameraFOV, '.8f')) + "\n")

        break

    Exporter.file.write("\t\t\t" + "}" + "\n")
    Exporter.file.write("\t\t" + "}" + "\n")

def writeCameraDOF():
    Exporter.file.write("\t\t" + "CameraDof Float3 0" + "\n")
    Exporter.file.write("\t\t" + "{" + "\n")
    Exporter.file.write("\t\t\t" + "FramesData MultiChannel" + "\n")
    Exporter.file.write("\t\t\t" + "{" + "\n")
    Exporter.file.write("\t\t\t\t" + "channel" + "\n")
    Exporter.file.write("\t\t\t\t" + "{" + "\n")

    for blenderObject in bpy.context.selected_objects:
        blenderScene = bpy.context.scene

        for i in range(blenderScene.frame_start, blenderScene.frame_end+1):
            blenderScene.frame_set(i)
            Exporter.file.write("\t\t\t\t\t" + str(format(0.0, '.8f')) + "\n")

        Exporter.file.write("\t\t\t\t" + "}" + "\n")
        Exporter.file.write("\t\t\t\t" + "channel" + "\n")
        Exporter.file.write("\t\t\t\t" + "{" + "\n")

        for i in range(blenderScene.frame_start, blenderScene.frame_end+1):
            blenderScene.frame_set(i)
            Exporter.file.write("\t\t\t\t\t" + str(format(0.0, '.8f')) + "\n")

        break

    Exporter.file.write("\t\t\t\t" + "}" + "\n")
    Exporter.file.write("\t\t\t\t" + "channel Static" + "\n")
    Exporter.file.write("\t\t\t\t" + "{" + "\n")
    Exporter.file.write("\t\t\t\t\t" + "0.00000000" + "\n")
    Exporter.file.write("\t\t\t\t" + "}" + "\n")
    Exporter.file.write("\t\t\t" + "}" + "\n")
    Exporter.file.write("\t\t" + "}" + "\n")

def writeCameraMatrixRotateFactor():
    Exporter.file.write("\t\t" + "CameraMatrixRotateFactor Float 0" + "\n")
    Exporter.file.write("\t\t" + "{" + "\n")
    Exporter.file.write("\t\t\t" + "FramesData SingleChannel Static" + "\n")
    Exporter.file.write("\t\t\t" + "{" + "\n")
    Exporter.file.write("\t\t\t\t" + "0.00000000" + "\n")
    Exporter.file.write("\t\t\t" + "}" + "\n")
    Exporter.file.write("\t\t" + "}" + "\n")

def writeCameraControl():
    Exporter.file.write("\t\t" + "CameraControl Float 0" + "\n")
    Exporter.file.write("\t\t" + "{" + "\n")
    Exporter.file.write("\t\t\t" + "FramesData SingleChannel" + "\n")
    Exporter.file.write("\t\t\t" + "{" + "\n")

    for blenderObject in bpy.context.selected_objects:
        blenderScene = bpy.context.scene

        for i in range(blenderScene.frame_start, blenderScene.frame_end+1):
            blenderScene.frame_set(i)

            currentLocationX = blenderObject.location.x
            currentLocationY = blenderObject.location.y

            blenderScene.frame_set(i + 1)

            nextLocationX = blenderObject.location.x
            nextLocationY = blenderObject.location.y

            if (int(nextLocationX) == int(currentLocationX) and int(nextLocationY) == int(currentLocationY)):
                # Interpolation between frames
                Exporter.file.write("\t\t\t\t" + str(format(-1.0, '.8f')) + "\n")
            else:
                # No interpolation between frames
                Exporter.file.write("\t\t\t\t" + str(format(1.0, '.8f')) + "\n")

        break
    
    Exporter.file.write("\t\t\t" + "}" + "\n")
    Exporter.file.write("\t\t" + "}" + "\n")

def start_export(options):
    filePath = options['filePath']

    Exporter.file = open(filePath, "w")

    Exporter.file.write("Version 8 2\n")
    Exporter.file.write("{" + "\n")
    Exporter.file.write("\t" + "Flags FLAG_0 FLAG_7 FLAG_8" + "\n") # TODO
    Exporter.file.write("\t" + "Frames " + str(bpy.context.scene.frame_end) + "\n")
    Exporter.file.write("\t" + "SequenceFrameLimit " + str(bpy.context.scene.frame_end + 5) + "\n") # TODO
    writeDuration()
    Exporter.file.write("\t" + "_f10 1999715593" + "\n") # TODO
    Exporter.file.write("\t" + "ExtraFlags" + "\n") # TODO
    Exporter.file.write("\t" + "Sequences " + str(bpy.context.scene.frame_end) + "\n")
    Exporter.file.write("\t" + "MaterialID -1" + "\n") # TODO
    Exporter.file.write("\t" + "Animation" + "\n")
    Exporter.file.write("\t" + "{" + "\n")
    writeCameraPosition()
    writeCameraRotation()
    writeCameraFOV()
    writeCameraDOF() # TODO
    writeCameraMatrixRotateFactor() # TODO
    writeCameraControl()
    Exporter.file.write("\t" + "}" + "\n")
    Exporter.file.write("}" + "\n")

    Exporter.file.close()

    bpy.context.scene.frame_set(1)