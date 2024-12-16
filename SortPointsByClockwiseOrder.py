
import clr  # Common Language Runtime, .NET's execution environment
import sys  # Fundamental Python library to manipulate the runtime environment

# Load standard IronPython libraries
sys.path.append('C:\Program Files\IronPython 2.7\Lib')

import System  # Root namespace of .NET
from System import Array  # .NET class for handling array information
from System.Collections.Generic import *  # To handle generic collections

# Add references to necessary Dynamo and Revit libraries
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *  # Dynamo geometry library

clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)
clr.ImportExtensions(Revit.GeometryConversion)

clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

clr.AddReference("RevitAPI")
clr.AddReference("RevitAPIUI")

import Autodesk 
from Autodesk.Revit.DB import *  # Revit API classes
from Autodesk.Revit.UI import *  # Revit API UI classes

import math

#Set up handles to the active Revit document and application
doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application
uidoc = uiapp.ActiveUIDocument
active_view = uidoc.ActiveView

# Get the current document and selection
ui_doc = DocumentManager.Instance.CurrentUIApplication.ActiveUIDocument
doc = ui_doc.Document



#SORT BY CLOCKWISE
def sort_points_clockwise(points):
    # Calculate the centroid (average X and Z coordinates)
    cx = sum(p.X for p in points) / len(points)
    cz = sum(p.Z for p in points) / len(points)

    # Compute angle of each point relative to the centroid using both X and Z coordinates
    points_with_angles = [(p, math.atan2(p.Z + cz, p.X - cx)) for p in points]

    # Sort points by angle (clockwise order)
    points_with_angles.sort(key=lambda x: x[1])

    # Extract and return the sorted points
    return [p[0] for p in points_with_angles]

# Example usage
sorted_points = sort_points_clockwise(points)