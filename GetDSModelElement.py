
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



#Set up handles to the active Revit document and application
doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application
uidoc = uiapp.ActiveUIDocument
active_view = uidoc.ActiveView

def getGeobyElement(element):
    opt = Options()
    opt.ComputeReferences = True
    opt.DetailLevel = ViewDetailLevel.Fine  
    opt.IncludeNonVisibleObjects = True
    geoByElement = element.get_Geometry(opt)
    return(geoByElement)

# Get the current document and selection
ui_doc = DocumentManager.Instance.CurrentUIApplication.ActiveUIDocument
doc = ui_doc.Document

# Pick an object (an element in this case)
picked_object = ui_doc.Selection.PickObject(Selection.ObjectType.Element)

# Get the element using its ElementId
sel_element = doc.GetElement(picked_object.ElementId)

# Function to get valid solids from the selected element
def get_valid_solids(sel_element):
    geos = getGeobyElement(sel_element)  # Get geometry from element
    solids = []  # List to store solids
    
    # Iterate through the geometry and find GeometryInstance objects
    for geo in geos:
        if isinstance(geo, GeometryInstance):
            # Get instance geometry from the geometry instance
            instance_geometry = geo.GetInstanceGeometry()
            solids.extend(instance_geometry)  # Add to solids list

    # Flatten the list of geometry solids
    solids = [solid for solid in solids if isinstance(solid, Solid)]  # Ensure only Solid objects

    # Get solids with a valid volume
    valid_solids = [solid for solid in solids if solid.Volume > 0]

    return valid_solids

# Call the function to get valid solids
valid_solids = get_valid_solids(sel_element)

# Start a new transaction
t = Transaction(doc, "Create DirectShape from Selected Element")
t.Start()

# Get the Generic Models category
generic_model_category = Category.GetCategory(doc, BuiltInCategory.OST_GenericModel)

category_id = generic_model_category.Id

direct_shape = DirectShape.CreateElement(doc, category_id)


# Set the shape of the DirectShape
direct_shape.SetShape(valid_solids)

# Commit the transaction
t.Commit()

OUT = direct_shape
