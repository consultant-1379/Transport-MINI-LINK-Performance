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
# Name    : RefreshData.py
# Date    : 22/05/2022
# Revision: 2.0
# Purpose : Based on filters selection, fetches/refreshes data for the corresponding DoD data table
#
# Usage   : Transport Report
#

from Spotfire.Dxp.Framework.ApplicationModel import NotificationService
from Spotfire.Dxp.Framework.ApplicationModel import ProgressService, ProgressCanceledException
from Spotfire.Dxp.Application import Filters as filters
from Spotfire.Dxp.Application.Filters import CheckBoxFilter
from Spotfire.Dxp.Application.Visuals import VisualTypeIdentifiers,BarChart,VisualContent,LineChart,TablePlot, AxisRange,Visualization,KpiChart
from Spotfire.Dxp.Data.Import import DataTableDataSource
from Spotfire.Dxp.Data import AddRowsSettings
from Spotfire.Dxp.Data import DataValueCursor, DataProperty, DataType, DataPropertyClass,RowSelection, IndexSet, LimitingMarkingsEmptyBehavior
from datetime import datetime
import time
from System import DateTime
ethernet_traffic = "Ethernet Traffic"
ethernet_b_u = "Ethernet Bandwidth Utilization"
radio_l_p = "Radio Link Performance"
agg_doc_property_name_mapping = {ethernet_traffic: 'AggregationTR', ethernet_b_u: 'AggregationBU', radio_l_p: 'AggregationRL'}
page_to_dt_mapping = {ethernet_traffic: 'IL_DC_E_IPTRANSPORT_ETH_TRAFFIC_', ethernet_b_u: 'IL_DC_E_IPTRANSPORT_ETH_BANDWIDTH_', radio_l_p: 'IL_DC_E_IPTRANSPORT_RADIOLINKG826_'}
target_table_mapping = {ethernet_traffic: 'IL_DC_E_IPTRANSPORT_ETH_TRAFFIC_', ethernet_b_u: 'IL_DC_E_IPTRANSPORT_ETH_BANDWIDTH_', radio_l_p: 'IL_DC_E_IPTRANSPORT_RADIOLINKG826_'}
areas_dict = {'IL_DC_E_IPTRANSPORT_ETH_TRAFFIC_DAY_DOD': {'NodeNameTable': 'DISTINCTED_NODES_TRAFFIC_DAY', 'DateIdTable': 'DISTINCTED_DATE_ID_TRAFFIC_DAY', 'DateIdMax': 'DateIdMaxTrafficDay', 'DateIdMin': 'DateIdMinTrafficDay', 'SelectedNodes': 'NodesTrafficDay'}, 
              'IL_DC_E_IPTRANSPORT_ETH_BANDWIDTH_DAY_DOD': {'NodeNameTable': 'DISTINCTED_NODES_BANDWIDTH_UTILIZATION_DAY', 'DateIdTable': 'DISTINCTED_DATE_ID_BANDWIDTH_UTILIZATION_DAY', 'DateIdMax': 'DateIdMaxBandwidthDay', 'DateIdMin': 'DateIdMinBandwidthDay', 'SelectedNodes': 'NodesBandwidthDay'}, 
              'IL_DC_E_IPTRANSPORT_RADIOLINKG826_DAY_DOD': {'NodeNameTable': 'DISTINCTED_NODES_RADIO_LINK_PERFORMANCE_DAY', 'DateIdTable': 'DISTINCTED_DATE_ID_RADIO_LINK_PERFORMANCE_DAY', 'DateIdMax': 'DateIdMaxRadioDay', 'DateIdMin': 'DateIdMinRadioDay', 'SelectedNodes': 'NodesRadioDay'}, 
              'IL_DC_E_IPTRANSPORT_ETH_TRAFFIC_RAW_DOD': {'NodeNameTable': 'DISTINCTED_NODES_TRAFFIC_RAW', 'DateIdTable': 'DISTINCTED_DATE_ID_TRAFFIC_RAW', 'DateIdMax': 'DateIdMaxTrafficRaw', 'DateIdMin': 'DateIdMinTrafficRaw', 'SelectedNodes': 'NodesTrafficRaw'}, 
              'IL_DC_E_IPTRANSPORT_ETH_BANDWIDTH_RAW_DOD': {'NodeNameTable': 'DISTINCTED_NODES_BANDWIDTH_UTILIZATION_RAW', 'DateIdTable': 'DISTINCTED_DATE_ID_BANDWIDTH_UTILIZATION_RAW', 'DateIdMax': 'DateIdMaxBandwidthRaw', 'DateIdMin': 'DateIdMinBandwidthRaw', 'SelectedNodes': 'NodesBandwidthRaw'}, 
              'IL_DC_E_IPTRANSPORT_RADIOLINKG826_RAW_DOD': {'NodeNameTable': 'DISTINCTED_NODES_RADIO_LINK_PERFORMANCE_RAW', 'DateIdTable': 'DISTINCTED_DATE_ID_RADIO_LINK_PERFORMANCE_RAW', 'DateIdMax': 'DateIdMaxRadioRaw', 'DateIdMin': 'DateIdMinRadioRaw', 'SelectedNodes': 'NodesRadioRaw'}}
interface_type_doc_property_name_mapping = {ethernet_traffic: 'NetworkTypeTraffic', ethernet_b_u: 'NetworkTypeBandwidthUtilization'}
ps = Application.GetService[ProgressService]()
notify = Application.GetService[NotificationService]() 
filtering_scheme_var = "Filtering scheme"

def set_line_chart_x_axis_expression(page, agg_flag):

    for vis in page.Visuals:
        if vis.TypeId == VisualTypeIdentifiers.LineChart:
            chart = vis.As[LineChart]()
            chart.XAxis.Expression = 'DATETIME_ID' if agg_flag == 'RAW' else 'DATE_ID'


def update_esr_sesr_flag(table_name):

    table = Document.Data.Tables[table_name]
    cursor = DataValueCursor.CreateFormatted(table.Columns["ESR Check"])
    val_data = []
    for _ in table.GetRows(cursor):
        value = cursor.CurrentValue
        if value not in val_data:
            val_data.Add(value)

    if 'Not a null value' in val_data:
        Document.Properties['EsrSesrFlag'] = 'fetched'
    else:
        Document.Properties['EsrSesrFlag'] = 'calculated'
        

def set_node_name_filter(current_page, aggregation,node_names_to_filter):

    if Document.Properties['EsrSesrFlag'] == 'fetched':
        target_data_table = Document.Data.Tables[target_table_mapping[current_page.Title] + aggregation + '_DOD_FETCHED']
    else:
        target_data_table = Document.Data.Tables[target_table_mapping[current_page.Title] + aggregation + '_DOD']

    node_name_filter = Document.FilteringSchemes[0].Item[target_data_table]["Node_Name"].As[CheckBoxFilter]()

    for value in node_name_filter.Values:
        node_name_filter.Uncheck(value)
        
    for node in node_names_to_filter:
        for _ in node_name_filter.Values:
            node_name_filter.Check(node)

    
def remove_filters_and_markings(current_page, aggregation):

    if Document.Properties['EsrSesrFlag'] == 'fetched':
        target_data_table = Document.Data.Tables[target_table_mapping[current_page.Title] + aggregation + '_DOD_FETCHED']
    else:
        target_data_table = Document.Data.Tables[target_table_mapping[current_page.Title] + aggregation + '_DOD']
    filter_col_filter = Document.FilteringSchemes[0].Item[target_data_table]["Filter Col"].As[CheckBoxFilter]()
    for _ in filter_col_filter.Values:
        filter_col_filter.Check('True')

    page = get_page(current_page.Title)
    for visualization in page.Visuals:
        if visualization.TypeId == VisualTypeIdentifiers.BarChart:
            visualization = visualization.As[Visualization]()
            for filtering in visualization.Data.Filterings:
                if filtering.Name == "MarkingHolder":
                    visualization.Data.Filterings.Remove(Document.Data.Markings["MarkingHolder"])
            visualization.Data.Filterings.Remove(Document.Data.Markings["MarkingHolder"])
            visualization.Data.Filterings.Remove(Document.Data.Markings["MarkingHolder"])
            visualization.Data.Filterings.Remove(Document.Data.Markings["MarkingHolder"])
            visualization.Data.Filterings.Remove(Document.Data.Markings["MarkingHolder"])
            visualization.Data.Filterings.Remove(Document.Data.Markings["MarkingHolder"])


def set_date_time(area_dict):

    date_time_table = Document.Data.Tables[area_dict['DateIdTable']]
    date_id_cursor = DataValueCursor.CreateFormatted(date_time_table.Columns["DATE_ID"])
    data_filtering_selection = Document.Data.Filterings[filtering_scheme_var]
    filtering_scheme = Document.FilteringSchemes[data_filtering_selection]
    filter_collection = filtering_scheme[date_time_table]
    filtered_rows = filter_collection.FilteredRows
    date_ids = []
    for _ in date_time_table.GetRows(filtered_rows,date_id_cursor):
        date_ids.Add(datetime.strptime(date_id_cursor.CurrentValue, "%d/%m/%Y"))
    
    date_ids.sort()
    if not date_ids:
        Document.Properties[area_dict['DateIdMax']] = '2010-01-01'
        Document.Properties[area_dict['DateIdMin']] = '2010-01-01'
    else:
        Document.Properties[area_dict['DateIdMax']] = str(date_ids[-1]).split(' ')[0]
        Document.Properties[area_dict['DateIdMin']] = str(date_ids[0]).split(' ')[0]
        

def get_link_missing_node_names(node_names,data_table_name):
    """
    Returns list of link missing node names. It can be either source or destination nodes based on the user selection in the node name filter
    Arguments:
        node_names {list} -- node names selected by the user in the node name filter
    Returns:
        link_missing_node_names {list} -- list of link missing node names
    """

    node_names_data_table = Document.Data.Tables[data_table_name]
    source_node_name_cursor = DataValueCursor.CreateFormatted(node_names_data_table.Columns["Source_Node_Name"])
    destination_node_name_cursor = DataValueCursor.CreateFormatted(node_names_data_table.Columns["Destination_Node_Name"])
    link_missing_node_names = []

    for node in node_names:
        for _ in node_names_data_table.GetRows(destination_node_name_cursor,source_node_name_cursor):
            destination_node_name = destination_node_name_cursor.CurrentValue
            source_node_name = source_node_name_cursor.CurrentValue
            if (node == source_node_name) and (destination_node_name not in link_missing_node_names):
                link_missing_node_names.Add(destination_node_name)
            elif (node == destination_node_name) and (source_node_name not in link_missing_node_names):
                link_missing_node_names.Add(source_node_name)

    return link_missing_node_names	


def get_node_names(area_dict,data_table_name):
    """
    Returns list of filtered nodes from DISTINCTED_NODES data table
    Arguments:
        area_dict {dict} -- dictionary which holds area's attributes
    Returns:
        node_names {list} -- list of filtered nodes from DISTINCTED_NODES data table including nodes that are missing in the link
    """

    node_names_data_table = Document.Data.Tables[area_dict['NodeNameTable']]
    node_name_cursor = DataValueCursor.CreateFormatted(node_names_data_table.Columns["Node_Name"])
    data_filtering_selection = Document.Data.Filterings[filtering_scheme_var]
    filtering_scheme = Document.FilteringSchemes[data_filtering_selection]
    filter_collection = filtering_scheme[node_names_data_table]
    filtered_rows = filter_collection.FilteredRows
    node_names = []
    for _ in node_names_data_table.GetRows(filtered_rows,node_name_cursor):
        node_names.Add(node_name_cursor.CurrentValue)
    
    if not node_names:
        node_names.Add('default')

    Document.Properties[area_dict['SelectedNodes']] = list(set(node_names + get_link_missing_node_names(node_names,data_table_name)))

    return node_names


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


def set_link_data_flag_filter(target_data_table):
    """
    Filters/adds nodes that have/do not have link level data
    Arguments:
        target_data_table {obj} -- data table object
    """
    
    link_data_flag_filter = Document.FilteringSchemes[0].Item[target_data_table]["Link Data Flag"].As[CheckBoxFilter]()

    for value in link_data_flag_filter.Values:
        link_data_flag_filter.Check(value)


def set_interface_type_filter(page):
    """
    Sets PM data table interface type filter based on interface type drop-down value
    Arguments:
        target_data_table {obj} -- data table object
    """

    aggregation = Document.Properties[agg_doc_property_name_mapping[page.Title]]
    target_data_table = Document.Data.Tables[target_table_mapping[page.Title] + aggregation + '_DOD']
    interface_type_filter = Document.FilteringSchemes[0].Item[target_data_table]["MOC"].As[CheckBoxFilter]()

    for value in interface_type_filter.Values:
        interface_type_filter.Uncheck(value)
        interface_type_filter.Check(Document.Properties[interface_type_doc_property_name_mapping[page.Title] + aggregation])


def refresh_data():
    """
    Child function to main(). Function used to:
        Refresh PM data based on current page title and selected aggregation
        Set node level line chart properties
        Set node level node name/link data flag/interface type filters 
        Trigger 'SetPagePropertiesAndVisualizations.py' to run
    """
    
    page = Document.ActivePageReference
    aggregation = Document.Properties[agg_doc_property_name_mapping[page.Title]]
    ps.CurrentProgress.ExecuteSubtask('Starting query')
    area_dict = areas_dict[page_to_dt_mapping[page.Title] + aggregation + "_DOD"]
    #set_date_time(area_dict)
    Document.Data.Tables[page_to_dt_mapping[page.Title] + aggregation + "_TCIMNODES"+ "_DOD"].ReloadAllData()
    data_table_name=page_to_dt_mapping[page.Title] + aggregation + "_TCIMNODES"+ "_DOD"
    node_names_to_filter = get_node_names(area_dict,data_table_name)
    Document.Data.Tables[page_to_dt_mapping[page.Title] + aggregation + "_DOD"].ReloadAllData()
    Document.Data.Tables[page_to_dt_mapping[page.Title] + aggregation + "_TCIM"+ "_DOD"].ReloadAllData()
    remove_filters_and_markings(page, aggregation)
    set_line_chart_x_axis_expression(page, aggregation)
    set_node_name_filter(page, aggregation, node_names_to_filter)
    set_link_data_flag_filter(Document.Data.Tables[page_to_dt_mapping[page.Title] + aggregation + "_DOD"])
    if 'RADIOLINK' in page_to_dt_mapping[page.Title] + aggregation + "_DOD":
        table_name = page_to_dt_mapping[page.Title] + aggregation + "_DOD"
        update_esr_sesr_flag(table_name)
    else:
        set_interface_type_filter(page)
    Document.Properties['GenerateVisualizationsDataTrigger'] = DateTime.UtcNow


def main():
    """
    Entry Point of script, call to refresh data for DoD data tables
    """
    try:
        refresh_data()
    except Exception as e:
        msg = "Something Went Wrong"
        notify.AddWarningNotification("Exception","Error in fetching data",msg)
        print("Exception: ", e)


ps.ExecuteWithProgress('Fetching data', 'Please be patient, this can take several minutes...', main)