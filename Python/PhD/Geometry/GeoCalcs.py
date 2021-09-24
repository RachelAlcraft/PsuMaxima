#!/usr/bin/env python3
"""
Author:    Rachel Alcraft
Date:      11/05/2020
Function:  Geo calculations
Description:
============
Replicates the calculations for distance, angle and torsion for validation
"""

import math


def distance(x1, y1, z1, x2, y2, z2):
    """
    param: x1,y1,z1= the coordinates of the first atom
    param: x2,y2,z2= the coordinates of the second atom
    returns: distance between atoms and details of the calculation
    """
    calc = ''
    mag = 0
    if z2 != '':
        xd = float(x2) - float(x1)
        yd = float(y2) - float(y1)
        zd = float(z2) - float(z1)
        calc = 'x diff = ' + str(round(xd, 3))
        calc += '<br/>y diff = ' + str(round(yd, 3))
        calc += '<br/>z diff = ' + str(round(zd, 3))
        sumsqu = (xd * xd) + (yd * yd) + (zd * zd)
        calc += '<br/>sum squares = ' + str(round(sumsqu, 3))
        mag = math.sqrt(sumsqu)
        calc += '<br/>magnitude = ' + str(round(mag, 3))

    return (mag)


def angle(x1, y1, z1, x2, y2, z2, x3, y3, z3):
    """
    param: x1,y1,z1= the coordinates of the first atom
    param: x2,y2,z2= the coordinates of the second atom
    param: x3,y3,z3= the coordinates of the third atom
    returns: angle between atoms and details of the calculation
    """
    calc = ''
    theta_deg = 0
    if z3 != '':
        try:
            xd = float(x2) - float(x1)
            yd = float(y2) - float(y1)
            zd = float(z2) - float(z1)
            calc = '(a2-a1) = A = (' + str(round(xd, 3)) + ',' + str(round(yd, 3)) + ',' + str(round(zd, 3)) + ')'
            xe = float(x2) - float(x3)
            ye = float(y2) - float(y3)
            ze = float(z2) - float(z3)
            calc += '<br/>(a2-a3) = B = (' + str(round(xe, 3)) + ',' + str(round(ye, 3)) + ',' + str(round(ze, 3)) + ')'

            dot = (xd * xe) + (yd * ye) + (zd * ze)
            calc += '<br/>dot product = ' + str(round(dot, 3))

            magA = math.sqrt((xd * xd) + (yd * yd) + (zd * zd))
            magB = math.sqrt((xe * xe) + (ye * ye) + (ze * ze))

            calc += '<br/>magnitude A = ' + str(round(magA, 3))
            calc += '<br/>magnitude B = ' + str(round(magB, 3))

            cos_theta = dot / (magA * magB)
            calc += '<br/>cos theta = ' + str(round(cos_theta, 3))

            theta = math.acos(cos_theta)
            calc += '<br/>theta (radians) = ' + str(round(theta, 3))

            theta_deg = (theta / 3.141592653589793238463) * 180
            calc += '<br/>theta (degrees) = ' + str(round(theta_deg, 3))
        except:
            calc = 'error, could be a divide by zero'

    return (round(theta_deg, 3))


def crossProduct(A, B):
    x = (A[1] * B[2]) - (A[2] * B[1])
    y = (A[2] * B[0]) - (A[0] * B[2])
    z = (A[0] * B[1]) - (A[1] * B[0])
    return (x, y, z)


def torsion(x1, y1, z1, x2, y2, z2, x3, y3, z3, x4, y4, z4):
    """
    param: x1,y1,z1= the coordinates of the first atom
    param: x2,y2,z2= the coordinates of the second atom
    param: x3,y3,z3= the coordinates of the third atom
    param: x4,y4,z4= the coordinates of the fourth atom
    returns: angle between atoms and details of the calculation
    """
    calc = ''
    theta_deg = 0
    if z4 != '':
        try:
            xA = float(x2) - float(x1)
            yA = float(y2) - float(y1)
            zA = float(z2) - float(z1)
            calc = '(a2-a1) = A = (' + str(round(xA, 3)) + ',' + str(round(yA, 3)) + ',' + str(round(zA, 3)) + ')'

            xB = float(x2) - float(x3)
            yB = float(y2) - float(y3)
            zB = float(z2) - float(z3)
            calc += '<br/>(a2-a3) = B = (' + str(round(xB, 3)) + ',' + str(round(yB, 3)) + ',' + str(round(zB, 3)) + ')'

            xC = float(x4) - float(x3)
            yC = float(y4) - float(y3)
            zC = float(z4) - float(z3)
            calc += '<br/>(a4-a3) = C = (' + str(round(xC, 3)) + ',' + str(round(yC, 3)) + ',' + str(round(zC, 3)) + ')'

            # xcrossAB = (yA * zB) - (zA * yB)
            # ycrossAB = (zA * xB) - (xA * zB)
            # zcrossAB = (xA * yB) - (yA * xB)
            crossAB = crossProduct((xA, yA, zA), (xB, yB, zB))
            calc += '<br/>X product AB = (' + str(round(crossAB[0], 3)) + ',' + str(round(crossAB[1], 3)) + ',' + str(
                round(crossAB[2], 3)) + ')'

            # xcrossBC = (yB * zC) - (zB * yC)
            # ycrossBC = (zB * xC) - (xB * zC)
            # zcrossBC = (xB * yC) - (yB * xC)
            crossBC = crossProduct((xB, yB, zB), (xC, yC, zC))
            calc += '<br/>X product BC = (' + str(round(crossBC[0], 3)) + ',' + str(round(crossBC[1], 3)) + ',' + str(
                round(crossBC[2], 3)) + ')'

            dot = (crossAB[0] * crossBC[0]) + (crossAB[1] * crossBC[1]) + (crossAB[2] * crossBC[2])
            calc += '<br/>dot product = ' + str(round(dot, 3))

            ABsq = (crossAB[0] ** 2) + (crossAB[1] ** 2) + (crossAB[2] ** 2)
            BCsq = (crossBC[0] ** 2) + (crossBC[1] ** 2) + (crossBC[2] ** 2)
            calc += '<br/>Sum sq AxB = ' + str(round(ABsq, 3))
            calc += '<br/>Sum sq BxC = ' + str(round(BCsq, 3))
            magAB = math.sqrt(ABsq)
            magBC = math.sqrt(BCsq)
            calc += '<br/>|AxB| = ' + str(round(magAB, 3))
            calc += '<br/>|BxC| = ' + str(round(magBC, 3))

            cos_theta = dot / (magAB * magBC)
            calc += '<br/>cos theta = dot/(|AxB| x |BxC|)'
            calc += '<br/>cos theta = ' + str(round(cos_theta, 3))

            theta = math.acos(cos_theta)
            calc += '<br/>theta (radians) = ' + str(round(theta, 3))
            theta_deg = (theta / 3.141592653589793238463) * 180
            calc += '<br/>theta (degrees) = ' + str(round(theta_deg, 3))

            calc += '<br/><br/>now check the sign:'

            cross = crossProduct(crossAB, crossBC)
            # xcross = (crossAB[] * zcrossBC) - (zcrossAB * ycrossBC)
            # ycross = (zcrossAB * xcrossBC) - (xcrossAB * zcrossBC)
            # zcross = (xcrossAB * ycrossBC) - (ycrossAB * xcrossBC)
            calc += '<br/>X product AB x BC = (' + str(round(cross[0], 3)) + ',' + str(round(cross[1], 3)) + ',' + str(
                round(cross[2], 3)) + ')'
            dotB = (cross[0] * xB) + (cross[1] * yB) + (cross[2] * zB)
            calc += '<br/>dot product ABxBC . B = ' + str(round(dotB, 3))
            dotsign = 1
            if dotB > 0:
                dotsign = -1
                theta_deg *= -1
            calc += '<br/>sign of angle = ' + str(round(dotsign, 3))
            calc += '<br/>theta (degrees) = ' + str(round(theta_deg, 3))

        except:
            calc = 'error, could be a divide by zero'
            print("x=(",x1, x2, x3,x4,") y=(",y1,y2,y3,y4,") z=(",z1,z2,z3,z4)
            theta_deg = 0
    else:
        calc = 'error, no 4th atom'
        print(x1,x2,x3)
        theta_deg = 0

    return (round(theta_deg, 3))