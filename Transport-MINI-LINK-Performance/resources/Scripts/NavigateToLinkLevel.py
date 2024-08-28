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
# Name    : NavigateToLinkLevel.py
# Date    : 16/05/2023
# Revision: 1.0
# Purpose : Navigating user from node level page to the corresponding link level page
#
# Usage   : Transport Report
#

from Spotfire.Dxp.Data import DataValueCursor
from Spotfire.Dxp.Application.Filters import CheckBoxFilter, ListBoxFilter
from Spotfire.Dxp.Application.Visuals import VisualTypeIdentifiers, BarChart

Ethernet_Traffic = 'Ethernet Traffic'
Ethernet_Bandwidth_Utilization = 'Ethernet Bandwidth Utilization'
Radio_Link_Performance = 'Radio Link Performance'

link_level_page_name_mapping = {Ethernet_Traffic: 'Ethernet Traffic Link Level', Ethernet_Bandwidth_Utilization: 'Ethernet Bandwidth Utilization Link Level', Radio_Link_Performance: 'Radio Link Performance Link Level'}
agg_doc_property_name_mapping = {Ethernet_Traffic: 'AggregationTR', Ethernet_Bandwidth_Utilization: 'AggregationBU', Radio_Link_Performance: 'AggregationRL'}
link_level_page_name_mapping = {Ethernet_Traffic: 'Ethernet Traffic Link Level', Ethernet_Bandwidth_Utilization: 'Ethernet Bandwidth Utilization Link Level', Radio_Link_Performance: 'Radio Link Performance Link Level'}
page_to_dt_mapping = {Ethernet_Traffic: 'IL_DC_E_IPTRANSPORT_ETH_TRAFFIC_', Ethernet_Bandwidth_Utilization: 'IL_DC_E_IPTRANSPORT_ETH_BANDWIDTH_', Radio_Link_Performance: 'IL_DC_E_IPTRANSPORT_RADIOLINKG826_'}
node_names_excluding_link_level_nodes_doc_prop_mapping = {Ethernet_Traffic: 'NodeNamesExcludingLinkLevelNodesTr', 
                                                          Ethernet_Bandwidth_Utilization: 'NodeNamesExcludingLinkLevelNodesBu', 
                                                          Radio_Link_Performance: 'NodeNamesExcludingLinkLevelNodesRl'}
node_names_to_distincted_node_names_dt_mapping = {Ethernet_Traffic: 'DISTINCTED_NODES_TRAFFIC_', 
                                                  Ethernet_Bandwidth_Utilization: 'DISTINCTED_NODES_BANDWIDTH_UTILIZATION_', 
                                                  Radio_Link_Performance: 'DISTINCTED_NODES_RADIO_LINK_PERFORMANCE_'}
no_link_data_nodes_doc_prop_mapping = {Ethernet_Traffic: 'NoLinkDataNodesTr', 
                                       Ethernet_Bandwidth_Utilization: 'NoLinkDataNodesBu', 
                                       Radio_Link_Performance: 'NoLinkDataNodesRl'}
link_name_data_availability_flag_doc_prop_mapping = {Ethernet_Traffic: 'LinkNameDataAvailabilityTr', Ethernet_Bandwidth_Utilization: 'LinkNameDataAvailabilityBu', Radio_Link_Performance: 'LinkNameDataAvailabilityRl'}
interface_type_doc_property_name_mapping = {Ethernet_Traffic: 'NetworkTypeTraffic', Ethernet_Bandwidth_Utilization: 'NetworkTypeBandwidthUtilization'}
markings_mapping = {Ethernet_Traffic: ['MarkingTr'], Ethernet_Bandwidth_Utilization: ['MarkingBu'], Radio_Link_Performance: ['MarkingRl']}


def get_node_names_excluding_link_level_nodes(page_title, aggregation):
    """
    Returns list of all node names from DISTINCTED_NODES table Node_Name filter
    Arguments:
        page_title {String} -- required page title
        aggregation {String} -- aggregation level
    Returns:
        node_names {list} -- list of all node names from DISTINCTED_NODES table Node_Name filter
    """

    table = Document.Data.Tables[node_names_to_distincted_node_names_dt_mapping[page_title] + aggregation]
    source_node_name_filter = Document.FilteringSchemes[0][table][table.Columns["Node_Name"]].As[ListBoxFilter]()
    node_names = []
    if not source_node_name_filter.IncludeAllValues:
        for value in source_node_name_filter.SelectedValues:
            node_names.append(value)
            
    return node_names


def get_all_and_primary_nodes_marked(target_data_table, page_title, aggregation):
    """
    Returns list of all node names(selected in the bar chart and the ones without link level data)
    Also, list of node names that are marked in the bar chart
    Arguments:
        target_data_table {obj} -- data table object
        page_title {String} -- required page title
        aggregation {String} -- aggregation level
    Returns:
        all_nodes {list} -- list of all nodes names(destination + marked in the bar chart)
        primary_node_names_marked {list} -- list of node names marked in the bar chart
    """

    source_node_name_cursor = DataValueCursor.CreateFormatted(target_data_table.Columns["Node_Name"])
    destination_node_name_cursor = DataValueCursor.CreateFormatted(target_data_table.Columns["Destination_Node_Name"])
    markings = Document.ActiveMarkingSelectionReference.GetSelection(target_data_table)
    primary_node_names_marked = []
    destination_node_names = []

    for _ in target_data_table.GetRows(markings.AsIndexSet(),destination_node_name_cursor,source_node_name_cursor):
        source_node_name = source_node_name_cursor.CurrentValue
        destination_node_name = destination_node_name_cursor.CurrentValue
        if source_node_name != str.Empty and source_node_name not in primary_node_names_marked: 
            primary_node_names_marked.Add(source_node_name)
        if destination_node_name != str.Empty:
            destination_node_names.Add(destination_node_name)

    destination_node_names = list(set(destination_node_names))
    Document.Properties[node_names_excluding_link_level_nodes_doc_prop_mapping[page_title]] = ",".join(get_node_names_excluding_link_level_nodes(page_title, aggregation))
    all_nodes = destination_node_names + primary_node_names_marked

    return all_nodes, primary_node_names_marked


def set_link_data_flag_filter(target_data_table):
    """
    Filters out nodes that do not have link level data
    Arguments:
        target_data_table {obj} -- data table object
    """
    
    link_data_flag_filter = Document.FilteringSchemes[0].Item[target_data_table]["Link Data Flag"].As[CheckBoxFilter]()

    for _ in link_data_flag_filter.Values:
        link_data_flag_filter.Uncheck(0)


def navigate_to_page(link_level_page_name):
    """
    Navigates user to required page based on received page title
    Arguments:
        link_level_page_name {String} -- required page title
    """

    page = get_page(link_level_page_name)
    Document.ActivePageReference = page


def get_page(page_name):
    """
    Returns page object based on received page name string
    Arguments:
        page_name {String} -- required page name
    Returns:
        page {obj} -- page object
    """

    for page in Document.Pages: 
        if page.Title == page_name: 
            return page


def get_data_table(aggregation, page_title):
    """
    Returns data table object based on current page title and aggregation level
    Arguments:
        aggregation {String} -- aggregation level
        page_title {String} -- current page title
    Returns:
        target_data_table {obj} -- data table object
    """

    table_name = page_to_dt_mapping[page_title] + aggregation + "_DOD"
    if Document.Properties['EsrSesrFlag'] == 'fetched':
        target_data_table = Document.Data.Tables[table_name + '_FETCHED']
    else:
        target_data_table = Document.Data.Tables[table_name]

    return target_data_table


def get_filtering_condition(page_title, node):
    """
    Returns filtering condition to filter for required columns in PM data table
    Arguments:
        page_title {String} -- required page title
        node {String} -- node name
    Returns:
        filtering_condition {obj} -- row filtering condition
    """

    if 'Radio Link Performance' not in page_title:
        interface_type = Document.Properties[interface_type_doc_property_name_mapping[page.Title] + aggregation]
        filtering_condition = target_data_table.Select("Node_Name='" + node + "' AND MOC='" + interface_type + "'")
    else:
        filtering_condition = target_data_table.Select("Node_Name='"+node+"'")

    return filtering_condition


def check_node_link_data_availability(primary_node_names_marked, target_data_table, page_title):
    """
    Returns list of node names that do not have link level data
    Arguments:
        primary_node_names_marked {list} -- list of node names marked in node level bar chart
        target_data_table {target_data_table} -- data table object
        page_title {String} -- current page title
    Returns:
        nodes_without_link_data {list} -- list of node names that do not have link level data
    """

    nodes_without_link_data = []
    for node in primary_node_names_marked:
        link_availability_flags_list = []
        filtering_condition = get_filtering_condition(page_title, node)
        cursor = DataValueCursor.CreateFormatted(target_data_table.Columns["Link_Name"])
        for _ in target_data_table.GetRows(filtering_condition.AsIndexSet(),cursor):
            if cursor.CurrentValue not in link_availability_flags_list:
                link_availability_flags_list.append(cursor.CurrentValue)

        if all(p == 'No Link Data' for p in link_availability_flags_list) and node not in nodes_without_link_data:
            nodes_without_link_data.append(node)

    if nodes_without_link_data:
        Document.Properties[no_link_data_nodes_doc_prop_mapping[page_title]] = ", \n".join(nodes_without_link_data) + "\n "

    return nodes_without_link_data


def get_nodes_from_filtered_data(target_data_table):
    """
    Returns list of node names from filtered data
    Arguments:
        target_data_table {target_data_table} -- data table object
    Returns:
        nodes_from_filtered_data {list} -- list of node names from filtered data
    """

    nodes_from_filtered_data = []
    source_nodes = []
    data_filtering_selection = Document.Data.Filterings["Filtering scheme"]	
    filtering_scheme = Document.FilteringSchemes[data_filtering_selection]
    filter_collection = filtering_scheme[target_data_table]
    filtered_rows = filter_collection.FilteredRows
    source_node_name_cursor = DataValueCursor.CreateFormatted(target_data_table.Columns["Node_Name"])
    destination_node_name_cursor = DataValueCursor.CreateFormatted(target_data_table.Columns["Destination_Node_Name"])
    for _ in target_data_table.GetRows(filtered_rows, source_node_name_cursor, destination_node_name_cursor):
        source_node = source_node_name_cursor.CurrentValue
        destination_node = destination_node_name_cursor.CurrentValue
        if source_node not in nodes_from_filtered_data:
            nodes_from_filtered_data.append(source_node)
            if source_node not in source_nodes:
                source_nodes.append(source_node)
        if destination_node not in nodes_from_filtered_data and destination_node != '':
            nodes_from_filtered_data.append(destination_node)

    return nodes_from_filtered_data, source_nodes


def set_node_name_filter(nodes_for_filter, target_data_table):
    """
    Sets node name filter (checkbox) based on passed nodes list
    Arguments:
        nodes_for_filter {list} -- list of node names to set in checkbox filter
        target_data_table {obj} -- data table object
    """
    
    node_name_filter = Document.FilteringSchemes[0].Item[target_data_table]["Node_Name"].As[CheckBoxFilter]()

    for value in node_name_filter.Values:
        node_name_filter.Uncheck(value)

    for node in nodes_for_filter:
        for _ in node_name_filter.Values:
            node_name_filter.Check(node)


def remove_filter_column_filter(target_data_table):
    """
    Unchecks filter column filter to not display data when no nodes selected
    Arguments:
        target_data_table {obj} -- data table object
    """

    filter_col_filter = Document.FilteringSchemes[0].Item[target_data_table]["Filter Col"].As[CheckBoxFilter]()
    for _ in filter_col_filter.Values:
        filter_col_filter.Uncheck('True')


def get_link_level_bar_chart_vis(link_level_page_name):
    """
    Returns bar chart object based on received page title string
    Arguments:
        link_level_page_name {String} -- link level page name
    Returns:
        visual.As[BarChart]() {obj} -- bar chart object
    """

    page = get_page(link_level_page_name)
    for visual in page.Visuals:
        if visual.TypeId == VisualTypeIdentifiers.BarChart:
            return visual.As[BarChart]()
        

def remove_link_level_bar_chart_marking(page_title):
    """
    Removes marking for barchart in link level page
    Arguments:
        page_title {String} -- current page name
    """

    link_level_page_name = link_level_page_name_mapping[page_title]
    link_level_bar_chart_vis = get_link_level_bar_chart_vis(link_level_page_name)
    loop_guard = 0
    filter_count = link_level_bar_chart_vis.Data.Filterings.Count
    while filter_count > 0 and loop_guard <= 5: #Spotfire specific issue seen before. Marking not always removed if 'Remove' called only once. For handling scenario when all nodes selected in the barchart 
                                                #have link topology table(in node level page), all markings limiting data must be removed for barchart in link level page
        link_level_bar_chart_vis.Data.Filterings.Remove(Document.Data.Markings[markings[0]])
        filter_count = link_level_bar_chart_vis.Data.Filterings.Count
        loop_guard += 1


def set_destination_node_name_filter(nodes_for_filter, target_data_table):
    """
    Sets destination node name filter (checkbox) based on passed nodes list
    Arguments:
        nodes_for_filter {list} -- list of node names to set in checkbox filter
        target_data_table {obj} -- data table object
    """
    
    destination_node_name_filter = Document.FilteringSchemes[0].Item[target_data_table]["Destination_Node_Name"].As[CheckBoxFilter]()

    for value in destination_node_name_filter.Values:
        destination_node_name_filter.Uncheck(value)

    for node in nodes_for_filter:
        for _ in destination_node_name_filter.Values:
            destination_node_name_filter.Check(node)


page = Document.ActivePageReference
markings = markings_mapping[page.Title]
aggregation = Document.Properties[agg_doc_property_name_mapping[page.Title]]
target_data_table = get_data_table(aggregation, page.Title)
link_level_page_name = link_level_page_name_mapping[page.Title]
all_nodes_for_filter, primary_node_names_marked = get_all_and_primary_nodes_marked(target_data_table,page.Title,aggregation)
nodes_without_link_data = check_node_link_data_availability(primary_node_names_marked, target_data_table, page.Title)
nodes_from_filtered_data, source_nodes = get_nodes_from_filtered_data(target_data_table)

if nodes_without_link_data: #Handling scenario when some/all nodes selected in the barchart do not have link topology table
    Document.Properties[link_name_data_availability_flag_doc_prop_mapping[page.Title]] = 'True'
elif not nodes_without_link_data and not all_nodes_for_filter and not primary_node_names_marked: #Handling scenario when no nodes selected in the barchart
    remove_filter_column_filter(target_data_table)
    navigate_to_page(link_level_page_name)
else: #Handling scenario when all nodes selected in the barchart have link topology table
    set_link_data_flag_filter(target_data_table)
    set_node_name_filter(all_nodes_for_filter,target_data_table)
    set_destination_node_name_filter(all_nodes_for_filter,target_data_table)
    remove_link_level_bar_chart_marking(page.Title)
    navigate_to_page(link_level_page_name)