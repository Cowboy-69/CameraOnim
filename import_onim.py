import math
from pathlib import Path

import bpy

# https://automaticaddison.com/how-to-convert-a-quaternion-into-euler-angles-in-python/
def euler_from_quaternion(x, y, z, w):
        """
        Convert a quaternion into euler angles (roll, pitch, yaw)
        roll is rotation around x in radians (counterclockwise)
        pitch is rotation around y in radians (counterclockwise)
        yaw is rotation around z in radians (counterclockwise)
        """
        t0 = +2.0 * (w * x + y * z)
        t1 = +1.0 - 2.0 * (x * x + y * y)
        roll_x = math.atan2(t0, t1)
     
        t2 = +2.0 * (w * y - z * x)
        t2 = +1.0 if t2 > +1.0 else t2
        t2 = -1.0 if t2 < -1.0 else t2
        pitch_y = math.asin(t2)
     
        t3 = +2.0 * (w * z + x * y)
        t4 = +1.0 - 2.0 * (y * y + z * z)
        yaw_z = math.atan2(t3, t4)
     
        return roll_x, pitch_y, yaw_z # in radians

class Importer:
    fileLines = []
    currentLine = 0

    version = ""
    flags = ""
    frames = ""
    sequenceFrameLimit = ""
    duration = ""
    _f10 = ""
    extraFlags = ""
    sequences = ""
    materialID = ""

    cameraPosition = [[], [], []]
    cameraRotation = [[], [], [], []]
    cameraFOV = []
    cameraDOF = [[], [], []]

def readLine():
    line = ""

    while True:
        line = Importer.fileLines[Importer.currentLine]

        Importer.currentLine += 1

        if ("{" not in line and "}" not in line):
            break

    return line

def readLineFull():
    line = Importer.fileLines[Importer.currentLine]
    
    Importer.currentLine += 1

    return line

def readCameraPosition():
    while True:
        line = readLine()

        if ("FramesData" in line):
            Importer.currentLine += 3

            while True:
                positionX = readLineFull()
                if ("}" in positionX):
                    break
                else:
                    positionX = float(positionX.split()[0])
                    Importer.cameraPosition[0].append(positionX)

            Importer.currentLine += 2

            while True:
                positionY = readLineFull()
                if ("}" in positionY):
                    break
                else:
                    positionY = float(positionY.split()[0])
                    Importer.cameraPosition[1].append(positionY)

            Importer.currentLine += 2

            while True:
                positionZ = readLineFull()
                if ("}" in positionZ):
                    break
                else:
                    positionZ = float(positionZ.split()[0])
                    Importer.cameraPosition[2].append(positionZ)

            line = Importer.fileLines[Importer.currentLine + 3]
            if ("channel" not in line):
                line = Importer.fileLines[Importer.currentLine + 1]
                if ("FramesData SingleChannel Static" in line):
                    Importer.currentLine += 5

                break
        else:

            break

def readCameraRotation():
    while True:
        line = readLine()

        if ("FramesData" in line):
            Importer.currentLine += 3

            while True:
                rotationX = readLineFull()
                if ("}" in rotationX):
                    break
                else:
                    rotationX = float(rotationX.split()[0])
                    Importer.cameraRotation[0].append(rotationX)

            Importer.currentLine += 2

            while True:
                rotationY = readLineFull()
                if ("}" in rotationY):
                    break
                else:
                    rotationY = float(rotationY.split()[0])
                    Importer.cameraRotation[1].append(rotationY)

            Importer.currentLine += 2

            while True:
                rotationZ = readLineFull()
                if ("}" in rotationZ):
                    break
                else:
                    rotationZ = float(rotationZ.split()[0])
                    Importer.cameraRotation[2].append(rotationZ)

            Importer.currentLine += 2

            while True:
                rotationW = readLineFull()
                if ("}" in rotationW):
                    break
                else:
                    rotationW = float(rotationW.split()[0])
                    Importer.cameraRotation[3].append(rotationW)

            line = Importer.fileLines[Importer.currentLine + 3]
            if ("channel" not in line):
                break
        else:
            break

def readCameraFOV():
    while True:
        line = readLine()

        if ("FramesData" in line):
            Importer.currentLine += 1

            while True:
                fieldOfView = readLineFull()
                if ("}" in fieldOfView):
                    break
                else:
                    fieldOfView = float(fieldOfView.split()[0])
                    Importer.cameraFOV.append(fieldOfView)

            #line = Importer.fileLines[Importer.currentLine + 3]
            #if ("channel" not in line):
                #break
        else:
            break

def Cleanup():
    Importer.fileLines = []
    Importer.currentLine = 0

    Importer.cameraPosition = [[], [], []]
    Importer.cameraRotation = [[], [], [], []]
    Importer.cameraFOV = []
    Importer.cameraDOF = [[], [], []]

def start_import(options):
    Cleanup()

    Importer.filePath = options['filePath']

    ###################### File reading section ######################

    with open(Importer.filePath) as bFile:
        Importer.fileLines = bFile.readlines()
    bFile.close()

    Importer.version = readLine()
    Importer.flags = readLine()
    Importer.frames = readLine()
    Importer.sequenceFrameLimit = readLine()
    Importer.duration = readLine()
    Importer._f10 = readLine()
    Importer.extraFlags = readLine()
    Importer.sequences = readLine()
    Importer.materialID = readLine()

    readLine()

    if ("CameraPosition" in readLine()):
        readCameraPosition()

    if ("CameraRotation" in readLine()):
        readCameraRotation()

    if ("CameraFOV" in readLine()):
        readCameraFOV()

    if ("CameraDof" in readLine()):
        pass

    if ("CameraMatrixRotateFactor" in readLine()):
        pass
    
    if ("CameraControl" in readLine()):
        pass

    ###################### Blender section ######################

    fileName = Path(Importer.filePath).stem

    # Collection
    blenderCollection = bpy.data.collections.new(fileName)
    bpy.context.scene.collection.children.link(blenderCollection)

    # Camera
    cameraData = bpy.data.cameras.new(name=fileName)
    cameraObject = bpy.data.objects.new(fileName, cameraData)
    blenderCollection.objects.link(cameraObject)

    cameraData.lens_unit = "FOV"
    #cameraData.dof.use_dof = True

    bpy.context.scene.frame_end = len(Importer.cameraPosition[0])

    for i in range(0, len(Importer.cameraPosition[0])):
        currentFrame = i + bpy.context.scene.frame_start

        cameraObject.location = (Importer.cameraPosition[0][i], Importer.cameraPosition[1][i], Importer.cameraPosition[2][i])
        cameraObject.keyframe_insert(data_path="location", frame=currentFrame)

        if (len(Importer.cameraRotation[0]) > i):
            rotationInEuler = euler_from_quaternion(Importer.cameraRotation[0][i], Importer.cameraRotation[1][i], Importer.cameraRotation[2][i], Importer.cameraRotation[3][i])
            cameraObject.rotation_euler = (rotationInEuler[0] + 1.5708, rotationInEuler[1], rotationInEuler[2])
            cameraObject.keyframe_insert(data_path="rotation_euler", frame=currentFrame)

        if (len(Importer.cameraFOV) > i):
            cameraData.angle = math.radians(Importer.cameraFOV[i])
            cameraData.keyframe_insert(data_path="lens", frame=currentFrame)

        # TODO focus object
        #cameraData.dof.focus_distance = Importer.cameraDOF[i]
        #cameraData.dof.keyframe_insert(data_path="focus_distance", frame=i)
