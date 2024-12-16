
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

###################
# Get the current document and selection
ui_doc = DocumentManager.Instance.CurrentUIApplication.ActiveUIDocument
doc = ui_doc.Document

#get Rebar Bar Type
all_rebar= FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Rebar).WhereElementIsElementType().ToElements()

for rebar_bar_type in all_rebar:
    rebar_name = rebar_bar_type.get_Parameter(BuiltInParameter.SYMBOL_NAME_PARAM).AsString()
    if rebar_name == "N24":
        bar_type = rebar_bar_type
        break

# Pick an object (an element in this case)
host_element = ui_doc.Selection.PickObject(Selection.ObjectType.Element,"Select Host Element")
# Get the element using its ElementId
host_element_ID = doc.GetElement(host_element.ElementId)
new_curves = UnwrapElement(IN[2])

bottom_edge = new_curves[1]
start_point = bottom_edge.GetEndPoint(0)
end_point = bottom_edge.GetEndPoint(1)
vector = XYZ(end_point.X - start_point.X,end_point.Y - start_point.Y,end_point.Z - start_point.Z).Normalize()
normal = vector.CrossProduct(XYZ.BasisZ)

    
# Start a new transaction
t = Transaction(doc, "Create from Selected Element")
t.Start()

start_hook_orientation = Structure.RebarHookOrientation.Left
end_hook_orientation = Structure.RebarHookOrientation.Left
rebar_style = Structure.RebarStyle.Standard
start_hook_type = UnwrapElement(IN[1])
end_hook_type = UnwrapElement(IN[1])

bar =  Structure.Rebar.CreateFromCurves(doc,
rebar_style,
rebar_bar_type,
start_hook_type,
end_hook_type,
host_element_ID,
normal,
new_curves,
start_hook_orientation,
end_hook_orientation,
True,
True)

t.Commit()	

OUT = bar
#OUT = new_points
# (point.ToPoint() for point in sorted_points)
# public static Rebar CreateFromCurves(
# 	Document doc,
# 	RebarStyle style,
# 	RebarBarType barType,
# 	RebarHookType startHook,
# 	RebarHookType endHook,
# 	Element host,
# 	XYZ norm,
# 	IList<Curve> curves,
# 	RebarHookOrientation startHookOrient,
# 	RebarHookOrientation endHookOrient,
# 	bool useExistingShapeIfPossible,
# 	bool createNewShape
# )
#(point.ToPoint() for point in sorted_points)

# # Pick an object (an element in this case)
# references = ui_doc.Selection.PickObjects(Selection.ObjectType.LinkedElement,"Select Linked Model Objects")

# geos = []
# for reference in references:
#     revitLinkInstance = doc.GetElement(reference) #as revitLinkInstance
#     linkedDoc = revitLinkInstance.GetLinkDocument()
#     # Get the element using its ElementId
#     sel_element = linkedDoc.GetElement(reference.LinkedElementId)
#     geo = getGeobyElement(sel_element)
#     geos.append(geo)
    
# # #  #flatten list of geos
# geos = [geo for geos in geos for geo in geos]


# solids = []
# for geom_obj in geos:
#     if isinstance(geom_obj, Solid) and geom_obj.Volume > 0:  # Ensure it's not an empty Solid
#         solids.append(geom_obj)
#     elif isinstance(geom_obj, GeometryInstance):  # Handle nested geometry instances
#         inst_geometry = geom_obj.GetInstanceGeometry()
#         for inst_geom_obj in inst_geometry:
#             if isinstance(inst_geom_obj, Solid) and inst_geom_obj.Volume > 0:
#                 solids.append(inst_geom_obj)
                
# #create sublist of solid from solids
# chunk_size = 1
# sub_solid = [solids[i:i + chunk_size] for i in range(0, len(solids), chunk_size)]

                
# # Start a new transaction
# t = Transaction(doc, "Create DirectShape from Selected Element")

# t.Start()
	
# # Get the Generic Models category
# generic_model_category = Category.GetCategory(doc, BuiltInCategory.OST_GenericModel)

# category_id = generic_model_category.Id



# # Set the shape of the DirectShape
# for solid in sub_solid:
#     direct_shape = DirectShape.CreateElement(doc, category_id)
#     direct_shape.SetShape(solid)

# # Commit the transaction
# t.Commit()


