
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
reference = ui_doc.Selection.PickObject(Selection.ObjectType.LinkedElement,"Select Linked Model Objects")

revitLinkInstance = doc.GetElement(reference) #as revitLinkInstance

linkedDoc = revitLinkInstance.GetLinkDocument()

# Get the element using its ElementId
sel_element = linkedDoc.GetElement(reference.LinkedElementId)
geos = getGeobyElement(sel_element)

solids = []
for geom_obj in geos:
    if isinstance(geom_obj, Solid) and geom_obj.Volume > 0:  # Ensure it's not an empty Solid
        solids.append(geom_obj)
    elif isinstance(geom_obj, GeometryInstance):  # Handle nested geometry instances
        inst_geometry = geom_obj.GetInstanceGeometry()
        for inst_geom_obj in inst_geometry:
            if isinstance(inst_geom_obj, Solid) and inst_geom_obj.Volume > 0:
                solids.append(inst_geom_obj)
# Start a new transaction
t = Transaction(doc, "Create DirectShape from Selected Element")

t.Start()
	
# Get the Generic Models category
generic_model_category = Category.GetCategory(doc, BuiltInCategory.OST_GenericModel)

category_id = generic_model_category.Id

direct_shape = DirectShape.CreateElement(doc, category_id)

# Set the shape of the DirectShape
direct_shape.SetShape(solids)

# Commit the transaction
t.Commit()

OUT = solids
