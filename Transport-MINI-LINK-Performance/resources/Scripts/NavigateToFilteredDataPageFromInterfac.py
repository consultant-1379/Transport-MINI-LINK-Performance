# ********************************************************************
# Ericsson Inc.                                                 SCRIPT
# ********************************************************************
#
#
# (c) Ericsson Inc. 2023 - All rights reserved.
#
# The copyright to the computer program(s) herein is the property
# of Ericsson Inc. The programs may be used and/or copied only with
# the written permission from Ericsson Inc. or in accordance with the
# terms and conditions stipulated in the agreement/contract under
# which the program(s) have been supplied.
#
# ********************************************************************
# Name    : NavigateToFilteredDataPageFromInterface.py
# Date    : 09/05/2023
# Revision: 2.0
# Purpose : Navigating user from interface level page to filtered data page
#
# Usage   : Transport Report
#

from Spotfire.Dxp.Data import DataValueCursor, IndexSet, DataProperty, DataType, DataPropertyClass
from Spotfire.Dxp.Application.Visuals import VisualTypeIdentifiers,BarChart,VisualContent,LineChart,TablePlot
import time
import clr

RLP='Radio Link Performance Interface'
ET='Ethernet Traffic Interface'
EBU='Ethernet Bandwidth Utilization Interface'
agg_doc_property_name_mapping = {ET: 'AggregationTR', EBU: 'AggregationBU', RLP: 'AggregationRL'}
filtered_page_name_mapping = {ET: 'TRAFFIC_INTERFACE_FILTERED', EBU: 'BANDWIDTH_INTERFACE_FILTERED', RLP: 'RADIO_LINK_INTERFACE_FILTERED'}

markings_mapping = {ET: ['Filtered Traffic', 'MarkingTrInterface'],
                    EBU: ['Filtered Bandwidth Utilization', 'MarkingBuInterface'], 
                    RLP: ['Filtered Radio Link', 'MarkingRlInterface']}

intermediate_link_level_columns = ['dest_tp_intermediate_1', 'source_tp_intermediate_1', 'NodeA_2', 'dest_tp_intermediate_2', 'link_active_intermediate_1', 
                                   'link_active_intermediate_2', 'link_name_intermediate_1', 'link_name_intermediate_2', 'source_tp_intermediate_2', 'NodeB_2', 
                                   'Filter Col', 'Rand Var', 'Rand Var 2', 'Destination_Node_Name', 'Link Data Flag', 'Link_Name', 'Source_TP', 'Dest_TP', 'Link_Active',
                                   'DESTINATION_INTF','DESTINATION_NODE', 'SOURCE_INTF', 'SOURCE_NODE', 'DESTINATION_INTF (2)', 'DESTINATION_NODE (2)', 'SOURCE_INTF (2)', 'SOURCE_NODE (2)']

def check_marked_row_counting(page):
    """
    Returns integer of marked rows count
    Arguments:
        page {obj} -- page object
    Returns:
        Document.ActiveMarkingSelectionReference.GetSelection(data_table).IncludedRowCount {int} -- marked rows count
    """

    for visual in page.Visuals:
        if visual.TypeId == VisualTypeIdentifiers.LineChart:
            visual = visual.As[LineChart]()
            data_table = visual.Data.DataTableReference 
 
            return Document.ActiveMarkingSelectionReference.GetSelection(data_table).IncludedRowCount


def get_table_plotting(filtered_data_page_name):
    """
    Returns table plot object based on received filtered data page name
    Arguments:
        filtered_data_page_name {String} -- filtered data page name
    Returns:
        visual.As[TablePlot]() {obj} -- table plot object
    """

    page = get_pages(filtered_data_page_name)
    for visual in page.Visuals:
        if str(visual.TypeId) == "TypeIdentifier:Spotfire.Table":
            return visual.As[TablePlot]()


def get_pages(page_name):
    """
    Returns page object based on received page name
    Arguments:
       page_name {String} -- page name string
    Returns:
        page {obj} -- page object
    """

    for page in Document.Pages: 
        if page.Title == page_name: 
            return page
      

def remove_interm_link_level_columns(table_plot_visualization):
    """
    Removes intermediate link level columns from table plot in filtered data page
    Arguments:
        table_plot_visualization {obj} -- table plot visualization
    """

    data_table_ref = table_plot_visualization.Data.DataTableReference
    columns = table_plot_visualization.TableColumns
    for column in intermediate_link_level_columns:
        columns.Remove(data_table_ref.Columns.Item[column])
    
                   
page = Document.ActivePageReference
						  
			 
filtered_data_page_name = filtered_page_name_mapping[page.Title]
									   

aggregation = Document.Properties[agg_doc_property_name_mapping[page.Title]]
table_plot_visualization = get_table_plotting(filtered_data_page_name)
active_visual = Document.ActiveVisualReference
vis = active_visual.As[VisualContent]()
markings = markings_mapping[page.Title]

if check_marked_row_counting(page) == 0:
    table_plot_visualization.Data.Filterings.Remove(Document.Data.Markings[markings[1]])
    table_plot_visualization.Data.Filterings.Remove(Document.Data.Markings[markings[0]])
elif Document.Properties['ActiveVisualReference'] == 'barchart' and check_marked_row_counting(page) != 0:
    table_plot_visualization.Data.Filterings.Remove(Document.Data.Markings[markings[0]])
    table_plot_visualization.Data.Filterings.Add(Document.Data.Markings[markings[1]])
else:
    table_plot_visualization.Data.Filterings.Remove(Document.Data.Markings[markings[0]])
    table_plot_visualization.Data.Filterings.Add(Document.Data.Markings[markings[0]])

remove_interm_link_level_columns(table_plot_visualization)
Document.ActivePageReference = get_pages(filtered_data_page_name)