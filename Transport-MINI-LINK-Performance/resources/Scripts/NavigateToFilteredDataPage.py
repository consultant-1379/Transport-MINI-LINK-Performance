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
# Name    : NavigateToFilteredDataPage.py
# Date    : 18/05/2023
# Revision: 1.0
# Purpose : Navigating user from node level page to filtered data page
#
# Usage   : Transport Report
#

from Spotfire.Dxp.Data import DataValueCursor, IndexSet, DataProperty, DataType, DataPropertyClass
from Spotfire.Dxp.Application.Visuals import VisualTypeIdentifiers,BarChart,VisualContent,LineChart,TablePlot

RLP='Radio Link Performance'
ET='Ethernet Traffic'
EBU='Ethernet Bandwidth Utilization'
agg_doc_property_name_mapping = {ET: 'AggregationTR', EBU: 'AggregationBU', RLP: 'AggregationRL'}
filtered_page_name_mapping = {ET: 'TRAFFIC_FILTERED', EBU: 'BANDWIDTH_FILTERED', RLP: 'RADIO_LINK_FILTERED'}

markings_mapping = {ET: ['Filtered Traffic', 'MarkingTr'],
                    EBU: ['Filtered Bandwidth Utilization', 'MarkingBu'],  
                    RLP: ['Filtered Radio Link', 'MarkingRl']}

intermediate_link_level_columns = ['dest_tp_intermediate_1', 'source_tp_intermediate_1', 'NodeA_2', 'dest_tp_intermediate_2', 'link_active_intermediate_1', 
                                   'link_active_intermediate_2', 'link_name_intermediate_1', 'link_name_intermediate_2', 'source_tp_intermediate_2', 'NodeB_2', 
                                   'Filter Col', 'Rand Var', 'Rand Var 2', 'Destination_Node_Name', 'Link Data Flag', 'Link_Name', 'Source_TP', 'Dest_TP', 'Link_Active',
                                   'DESTINATION_INTF','DESTINATION_NODE', 'SOURCE_INTF', 'SOURCE_NODE', 'DESTINATION_INTF (2)', 'DESTINATION_NODE (2)', 'SOURCE_INTF (2)', 'SOURCE_NODE (2)']


def navigate_to_page(filtered_dt_page_name):
    """
    Navigates user to required page based on received page title
    Arguments:
        filtered_dt_page_name {String} -- required page name
    """

    page = get_page(filtered_dt_page_name)
    Document.Properties['ActiveVisualReference'] = ''
    Document.ActivePageReference = page


def check_marked_rows_count(page):
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


def get_table_plot(filtered_dt_page_name):
    """
    Returns table plot object based on received filtered data page name
    Arguments:
        filtered_dt_page_name {String} -- filtered data page name
    Returns:
        visual.As[TablePlot]() {obj} -- table plot object
    """

    page = get_page(filtered_dt_page_name)
    for visual in page.Visuals:
        if str(visual.TypeId) == "TypeIdentifier:Spotfire.Table":
            return visual.As[TablePlot]()


def get_page(page_name):
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
      

def remove_intermediate_link_level_columns(table_plot_vis):
    """
    Removes intermediate link level columns from table plot in filtered data page
    Arguments:
        table_plot_vis {obj} -- table plot visualization
    """

    data_table_ref = table_plot_vis.Data.DataTableReference
    columns = table_plot_vis.TableColumns
    for column in intermediate_link_level_columns:
        columns.Remove(data_table_ref.Columns.Item[column])
    
                   
page = Document.ActivePageReference
filtered_dt_page_name = ''
markings = []
filtered_dt_page_name = filtered_page_name_mapping[page.Title]
markings = markings_mapping[page.Title]

aggregation = Document.Properties[agg_doc_property_name_mapping[page.Title]]
table_plot_vis = get_table_plot(filtered_dt_page_name)
active_visual = Document.ActiveVisualReference
vis = active_visual.As[VisualContent]()

if check_marked_rows_count(page) == 0:
    table_plot_vis.Data.Filterings.Remove(Document.Data.Markings[markings[1]])
    table_plot_vis.Data.Filterings.Remove(Document.Data.Markings[markings[0]])
elif Document.Properties['ActiveVisualReference'] == 'barchart' and check_marked_rows_count(page) != 0:
    table_plot_vis.Data.Filterings.Remove(Document.Data.Markings[markings[0]])
    table_plot_vis.Data.Filterings.Add(Document.Data.Markings[markings[1]])
else:
    table_plot_vis.Data.Filterings.Remove(Document.Data.Markings[markings[0]])
    table_plot_vis.Data.Filterings.Add(Document.Data.Markings[markings[0]])

remove_intermediate_link_level_columns(table_plot_vis)
navigate_to_page(filtered_dt_page_name)