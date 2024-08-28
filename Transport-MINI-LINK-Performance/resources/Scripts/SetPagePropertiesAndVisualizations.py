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
# Name    : SetPagePropertiesAndVisualizations.py
# Date    : 16/05/2023
# Revision: 2.0
# Purpose : Sets node/interface level page properties and visualizations based on filter selections
#
# Usage   : Transport Report
#
from Spotfire.Dxp.Data import AddRowsSettings
from Spotfire.Dxp.Data.Import import DataTableDataSource
from Spotfire.Dxp.Data import RowSelection, IndexSet
from Spotfire.Dxp.Application.Visuals import VisualTypeIdentifiers, BarChart,LineChart,TablePlot,Visualization
from System import DateTime
import re
Ethernet_Traffic = 'Ethernet Traffic'
Ethernet_Bandwidth_Utilization = 'Ethernet Bandwidth Utilization'
Radio_Link_Performance = 'Radio Link Performance'
agg_doc_property_name_mapping = {Ethernet_Traffic: 'AggregationTR', Ethernet_Bandwidth_Utilization: 'AggregationBU', Radio_Link_Performance: 'AggregationRL'}
filtered_page_name_mapping = {Ethernet_Traffic: 'TRAFFIC_FILTERED', Ethernet_Bandwidth_Utilization: 'BANDWIDTH_FILTERED', Radio_Link_Performance: 'RADIO_LINK_FILTERED'}
interface_filtered_page_name_mapping = {Ethernet_Traffic: 'TRAFFIC_INTERFACE_FILTERED', Ethernet_Bandwidth_Utilization: 'BANDWIDTH_INTERFACE_FILTERED', Radio_Link_Performance: 'RADIO_LINK_INTERFACE_FILTERED'}
link_level_filtered_page_name_mapping = {Ethernet_Traffic: 'TRAFFIC_LINK_LEVEL_FILTERED', Ethernet_Bandwidth_Utilization: 'BANDWIDTH_LINK_LEVEL_FILTERED', Radio_Link_Performance: 'RADIO_LINK_LINK_LEVEL_FILTERED'}
page_to_dt_mapping = {Ethernet_Traffic: 'IL_DC_E_IPTRANSPORT_ETH_TRAFFIC_', Ethernet_Bandwidth_Utilization: 'IL_DC_E_IPTRANSPORT_ETH_BANDWIDTH_', Radio_Link_Performance: 'IL_DC_E_IPTRANSPORT_RADIOLINKG826_'}
kpi_list_mapping = {Ethernet_Traffic: 'TrafficKpi', Ethernet_Bandwidth_Utilization: 'BandwidthUtilizationKpi', Radio_Link_Performance: 'RadioLinkPerformanceKpi'}
columns_sequence_bu_tr = {'RAW': ['DATE_ID', 'DATETIME_ID', 'PERIOD_DURATION', 'OSS_ID', 'Node_Name', 'MOID', 'TRANS_MODE', 'NETWORK_TYPE'],
                          'DAY': ['DATE_ID', 'PERIOD_DURATION', 'OSS_ID', 'Node_Name', 'MOID', 'TRANS_MODE', 'NETWORK_TYPE']}
columns_sequence_rl = {'RAW': ['DATE_ID', 'DATETIME_ID', 'PERIOD_DURATION', 'OSS_ID', 'Node_Name', 'MOID'],
                       'DAY': ['DATE_ID', 'PERIOD_DURATION', 'OSS_ID', 'Node_Name', 'MOID']}
columns_sequence_dict = {'RADIO_LINK_FILTERED': columns_sequence_rl,
                         'BANDWIDTH_FILTERED': columns_sequence_bu_tr,
                         'TRAFFIC_FILTERED': columns_sequence_bu_tr}
columns_to_adjust_width_bu = ['PERIOD_DURATION', 'NETWORK_TYPE']
columns_to_adjust_width_tr = ['PERIOD_DURATION', 'NETWORK_TYPE', 'Broadcast_Packets', 'Discarded_Packets', 'Multicast_Packets', 'Unicast_Packets']
columns_to_adjust_width_rl = ['PERIOD_DURATION', 'QAM1024_Light', 'QAM1024_Strong', 'QAM128_Strong', 'QAM2048_Light', 'QAM2048_Strong', 'QAM256_Strong', 'QAM4096_Light', 'QAM4096_Strong', 'QAM512_Strong']
columns_to_adjust_width_dict = {'RADIO_LINK_FILTERED': columns_to_adjust_width_rl,
                                'BANDWIDTH_FILTERED': columns_to_adjust_width_bu,
                                'TRAFFIC_FILTERED': columns_to_adjust_width_tr}
reset_filters_initial_pages = [Ethernet_Traffic, Ethernet_Bandwidth_Utilization, Radio_Link_Performance]
reset_filters_interface_pages = {Ethernet_Traffic: 'Ethernet Traffic Interface', Ethernet_Bandwidth_Utilization: 'Ethernet Bandwidth Utilization Interface', Radio_Link_Performance: 'Radio Link Performance Interface'}
line_bar_chart_title_substring_mapping = {Ethernet_Traffic: 'Traffic', Ethernet_Bandwidth_Utilization: 'BandwidthUtilization', Radio_Link_Performance: 'RadioLinkPerformance'}
line_bar_chart_title_substring_interface_mapping = {Ethernet_Traffic: 'TrafficInterface', Ethernet_Bandwidth_Utilization: 'BandwidthUtilizationInterface', Radio_Link_Performance: 'RadioLinkPerformanceInterface'}
aggregation_function_mapping = {'Avg': 'average', 'Min': 'min', 'Max': 'max'}
agg_function_doc_property_name_mapping = {Ethernet_Traffic: 'AggregationFunctionTR', Ethernet_Bandwidth_Utilization: 'AggregationFunctionBU', Radio_Link_Performance: 'AggregationFunctionRL'}
date_time_column_mapping = {'RAW': 'DATETIME_ID', 'DAY': 'DATE_ID'}
aggregation_name_mapping = {'RAW': '(ROP)', 'DAY': '(DAY)'}
chart_flags = ['bar', 'line']
column_exceptions = ['ROWSTATUS', 'DATETIME_ID', 'RemoveRows', 'Filter Col', 'ESR Check', 'Rand Var', 'Rand Var 2']
esr_sesr_list = ['ESR_Calculated', 'SESR_Calculated', 'ESR_Fetched', 'SESR_Fetched', 'ESR', 'SESR']
def get_bar_or_line_chart(page, chart_flag):
    if chart_flag == 'bar':
        for vis in page.Visuals:
            if vis.TypeId == VisualTypeIdentifiers.BarChart:
               return vis.As[BarChart]()
    else:
        for vis in page.Visuals:
            if vis.TypeId == VisualTypeIdentifiers.LineChart:
                return vis.As[LineChart]()
def get_bar_or_line_chart_properties(pages_list, agg_flag):
    for chart_flag in chart_flags:
        current_page = pages_list[0]
        charts_list = []
        for page in pages_list:
            chart = get_bar_or_line_chart(page, chart_flag)
            charts_list.append(chart)
        
        properties_dict = {}
        if current_page.Title == Radio_Link_Performance and Document.Properties['EsrSesrFlag'] == 'fetched':
            properties_dict = {'dt':Document.Data.Tables[page_to_dt_mapping[current_page.Title] + agg_flag +'_DOD_FETCHED'],'interface_dt':Document.Data.Tables[page_to_dt_mapping[current_page.Title] + agg_flag +'_DOD_FETCHED'],
                               'x_axis_expression':date_time_column_mapping[agg_flag],'y_axis_expression':'$map("avg($esc(${' + kpi_list_mapping[current_page.Title] + agg_flag + 'Fetched}))", ",")'}
        else:
            properties_dict = {'dt':Document.Data.Tables[page_to_dt_mapping[current_page.Title] + agg_flag +'_DOD'],'interface_dt':Document.Data.Tables[page_to_dt_mapping[current_page.Title] + agg_flag +'_DOD'],
                               'x_axis_expression':date_time_column_mapping[agg_flag],'y_axis_expression':'$map("avg($esc(${' + kpi_list_mapping[current_page.Title] + agg_flag + '}))", ",")'}
        set_bar_line_chart_properties(charts_list, properties_dict, chart_flag)
def set_bar_line_chart_properties(charts_list, properties_dict, chart_flag):
    chart_counter = 0
    for chart in charts_list:
        if chart_counter == 0:
            chart.Data.DataTableReference = properties_dict['dt']
        else:
            chart.Data.DataTableReference = properties_dict['interface_dt']
        chart.YAxis.Expression = properties_dict['y_axis_expression']
        chart_counter += 1
        if chart_flag == 'line':
            chart.XAxis.Expression = properties_dict['x_axis_expression']
def set_page_properties(pages_list):
    current_page = pages_list[0]
    aggregation = Document.Properties[agg_doc_property_name_mapping[current_page.Title]]
    aggregation_function = Document.Properties[agg_function_doc_property_name_mapping[current_page.Title]]
    if aggregation == 'RAW':
        get_bar_or_line_chart_properties(pages_list,'RAW')
    else:
        get_bar_or_line_chart_properties(pages_list, 'DAY')
    Document.Properties['LineChartTitleSubstring' + line_bar_chart_title_substring_mapping[current_page.Title]] = aggregation_name_mapping[aggregation]
    Document.Properties['LineChartTitleSubstring' + line_bar_chart_title_substring_interface_mapping[current_page.Title]] = aggregation_name_mapping[aggregation]
    Document.Properties['BarChartTitleSubstring' + line_bar_chart_title_substring_mapping[current_page.Title]] = aggregation_function
    Document.Properties['BarChartTitleSubstring' + line_bar_chart_title_substring_interface_mapping[current_page.Title]] = aggregation_function
    
def get_filtered_data_page_table(page):
    
    aggregation = Document.Properties[agg_doc_property_name_mapping[page.Title]]
    if page.Title == Radio_Link_Performance and Document.Properties['EsrSesrFlag'] == 'fetched':
        data_table = Document.Data.Tables[page_to_dt_mapping[page.Title] + aggregation + '_DOD_FETCHED']
    else:
        data_table = Document.Data.Tables[page_to_dt_mapping[page.Title] + aggregation + '_DOD']
    set_filtered_data_page_table(page, data_table, aggregation)
def get_interface_link_filtered_data_page_names(page):
    """
    Returns list of interface/link level page names based on current page name
    Arguments:
        page {obj} -- page object
    Returns:
        interface_link_filtered_data_page_names {list} -- list of interface/link level page names
    """
    interface_link_filtered_data_page_names = []
    interface_page_name = interface_filtered_page_name_mapping[page.Title]
    link_level_page_name = link_level_filtered_page_name_mapping[page.Title]
    interface_link_filtered_data_page_names.Add(interface_page_name)
    interface_link_filtered_data_page_names.Add(link_level_page_name)
    return interface_link_filtered_data_page_names
def set_filtered_data_page_table(page, data_table, aggregation):
    page_name = filtered_page_name_mapping[page.Title]
    interface_link_filtered_data_page_names = get_interface_link_filtered_data_page_names(page)
    set_interface_link_filtered_data_page_table(interface_link_filtered_data_page_names, data_table, aggregation)
    page = get_page(page_name)
    for vis in page.Visuals:
        if vis.Title == 'FilteredDataVis':
            table_plot_chart = vis.As[TablePlot]()
            vis = vis.As[Visualization]()
            vis.Data.DataTableReference = data_table
            set_columns_order(aggregation, data_table, vis, page_name)
            set_columns_width(table_plot_chart, page_name)
    
def set_interface_link_filtered_data_page_table(interface_link_filtered_data_page_names, data_table, aggregation):
    for page_name in interface_link_filtered_data_page_names:
        page = get_page(page_name)
        for vis in page.Visuals:
            if vis.Title == 'FilteredDataVis':
                table_plot_chart = vis.As[TablePlot]()
                vis = vis.As[Visualization]()
                vis.Data.DataTableReference = data_table
                if 'INTERFACE' in page_name:
                    set_columns_order(aggregation, data_table, vis, page_name.replace("INTERFACE_",""))
                    set_columns_width(table_plot_chart, page_name.replace("INTERFACE_",""))
                else:
                    set_columns_order(aggregation, data_table, vis, page_name.replace("LINK_LEVEL_",""))
                    set_columns_width(table_plot_chart, page_name.replace("LINK_LEVEL_",""))
def set_columns_order(aggregation, data_table, visual, filtered_dt_page_name):
    visual.TableColumns.Clear()
    for col in columns_sequence_dict[filtered_dt_page_name][aggregation]:
        for column in data_table.Columns:
            if column.Name == col:
                visual.TableColumns.Add(column)
    call_set_columns_order2(aggregation, data_table, visual, filtered_dt_page_name)
def call_set_columns_order2(aggregation, data_table, visual, filtered_dt_page_name):
Refactor this function to reduce its Cognitive Complexity from 23 to the 15 allowed.Why is this an issue?

27 days ago
L203
Code Smell

Critical

Open

Not assigned
13min effort

Comment

brain-overload
    for column in data_table.Columns:
        if column.Name not in columns_sequence_dict[filtered_dt_page_name][aggregation] and column.Name not in column_exceptions:
            if column.Name not in esr_sesr_list:
                visual.TableColumns.Add(column)
            else:
                if Document.Properties['EsrSesrFlag'] == 'calculated':
                    if 'Fetched' not in column.Name:
                        visual.TableColumns.Add(column)
                else:
                    if 'Calculated' not in column.Name:
                        visual.TableColumns.Add(column)
def set_columns_width(table_plot_chart, filtered_dt_page_name):
    for col in table_plot_chart.TableColumns:
        if col.Name in columns_to_adjust_width_dict[filtered_dt_page_name]:
		    col.Width = 130
def refresh_data_flow(initial_page):
    pages_list = []
    interface_page = get_page(initial_page.Title + ' Interface')
    link_level_page = get_page(initial_page.Title + ' Link Level')
    pages_list.extend([initial_page,interface_page,link_level_page])
    set_page_properties(pages_list)
    get_filtered_data_page_table(initial_page)
    
def reset_filters_markings_flow():
    pages_list = []
    for reset_filters_page in reset_filters_initial_pages:
        initial_page = get_page(reset_filters_page)
        interface_page = get_page(reset_filters_interface_pages[initial_page.Title])
        link_level_page = get_page(initial_page.Title + ' Link Level')
        pages_list.extend([initial_page,interface_page,link_level_page])
        get_bar_or_line_chart_properties(pages_list, 'RAW')
def get_page(page_name):
   for page in Document.Pages: 
      if page.Title == page_name: 
         return page 
initial_page = Document.ActivePageReference
if initial_page.Title != 'Home':
    refresh_data_flow(initial_page)
else:
    reset_filters_markings_flow()
Document.Properties['SetKpiVisScriptTrigger'] = DateTime.UtcNow