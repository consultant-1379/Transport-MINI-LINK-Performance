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
# Name    : SetAggregationFunction.py
# Date    : 19/05/2023
# Revision: 2.0
# Purpose : Sets aggregation function to the bar and line charts in node/interface level pages
#
# Usage   : Transport Report
#

from Spotfire.Dxp.Application.Visuals import VisualTypeIdentifiers, BarChart,LineChart,TablePlot,Visualization
from System import DateTime

Ethernet_Traffic = 'Ethernet Traffic'
Ethernet_Bandwidth_Utilization = 'Ethernet Bandwidth Utilization'
Radio_Link_Performance = 'Radio Link Performance'
Ethernet_Traffic_Interface = 'Ethernet Traffic Interface'
Ethernet_Traffic_Link_Level = 'Ethernet Traffic Link Level'
Ethernet_Bandwidth_Utilization_Interface = 'Ethernet Bandwidth Utilization Interface'
Ethernet_Bandwidth_Utilization_Link_Level = 'Ethernet Bandwidth Utilization Link Level'
Radio_Link_Performance_Interface = 'Radio Link Performance Interface'
Radio_Link_Performance_Link_Level  = 'Radio Link Performance Link Level'
agg_doc_property_name_mapping = {Ethernet_Traffic: 'AggregationTR', Ethernet_Bandwidth_Utilization: 'AggregationBU', Radio_Link_Performance: 'AggregationRL'}
agg_function_doc_property_name_mapping = {Ethernet_Traffic: 'AggregationFunctionTR', Ethernet_Bandwidth_Utilization: 'AggregationFunctionBU', Radio_Link_Performance: 'AggregationFunctionRL'}
page_to_dt_mapping = {Ethernet_Traffic: 'IL_DC_E_IPTRANSPORT_ETH_TRAFFIC_', Ethernet_Bandwidth_Utilization: 'IL_DC_E_IPTRANSPORT_ETH_BANDWIDTH_', Radio_Link_Performance: 'IL_DC_E_IPTRANSPORT_RADIOLINKG826_', 
                      Ethernet_Traffic_Interface: 'IL_DC_E_IPTRANSPORT_ETH_TRAFFIC_', Ethernet_Bandwidth_Utilization_Interface: 'IL_DC_E_IPTRANSPORT_ETH_BANDWIDTH_', Radio_Link_Performance_Interface: 'IL_DC_E_IPTRANSPORT_RADIOLINKG826_',
                      Ethernet_Traffic_Link_Level : 'IL_DC_E_IPTRANSPORT_ETH_TRAFFIC_', Ethernet_Bandwidth_Utilization_Link_Level: 'IL_DC_E_IPTRANSPORT_ETH_BANDWIDTH_', Radio_Link_Performance_Link_Level: 'IL_DC_E_IPTRANSPORT_RADIOLINKG826_'}
kpi_list_mapping = {Ethernet_Traffic: 'TrafficKpi', Ethernet_Bandwidth_Utilization: 'BandwidthUtilizationKpi', Radio_Link_Performance: 'RadioLinkPerformanceKpi', 
                    Ethernet_Traffic_Interface: 'TrafficKpi', Ethernet_Bandwidth_Utilization_Interface: 'BandwidthUtilizationKpi', Radio_Link_Performance_Interface: 'RadioLinkPerformanceKpi',
                    Ethernet_Traffic_Link_Level: 'TrafficKpi', Ethernet_Bandwidth_Utilization_Link_Level: 'BandwidthUtilizationKpi', Radio_Link_Performance_Link_Level: 'RadioLinkPerformanceKpi'}
aggregation_function_mapping = {'Avg': 'average', 'Min': 'min', 'Max': 'max'}
interface_page_name_mapping = {Ethernet_Traffic: 'Ethernet Traffic Interface', Ethernet_Bandwidth_Utilization: 'Ethernet Bandwidth Utilization Interface', Radio_Link_Performance: 'Radio Link Performance Interface'}
link_level_page_name_mapping = {Ethernet_Traffic: Ethernet_Traffic_Link_Level, Ethernet_Bandwidth_Utilization: 'Ethernet Bandwidth Utilization Link Level', Radio_Link_Performance: 'Radio Link Performance Link Level'}
bar_chart_title_substring_mapping = {Ethernet_Traffic: 'Traffic', Ethernet_Bandwidth_Utilization: 'BandwidthUtilization', Radio_Link_Performance: 'RadioLinkPerformance'}
bar_chart_title_substring_interface_mapping = {Ethernet_Traffic_Interface: 'TrafficInterface', Ethernet_Bandwidth_Utilization_Interface: 'BandwidthUtilizationInterface', Radio_Link_Performance_Interface: 'RadioLinkPerformanceInterface',
                                               Ethernet_Traffic_Link_Level: 'TrafficInterface', Ethernet_Bandwidth_Utilization_Link_Level: 'BandwidthUtilizationInterface', Radio_Link_Performance_Link_Level: 'RadioLinkPerformanceInterface'}
aggregation_level_name_mapping = {'RAW': 'ROP', 'DAY': 'DAY'}
pages_to_reset = [Ethernet_Traffic, Ethernet_Bandwidth_Utilization, Radio_Link_Performance]
map = '$map("'
esc = '($esc(${'
def get_line_charts_properties(pages_list, agg_flag, aggregation_function):
    for page in pages_list:
        for vis in page.Visuals:
            if vis.TypeId == VisualTypeIdentifiers.LineChart:
                chart = vis.As[LineChart]()
                properties_dict = {}
                if Radio_Link_Performance in page.Title and Document.Properties['EsrSesrFlag'] == 'fetched':
                    properties_dict = {'dt':Document.Data.Tables[page_to_dt_mapping[page.Title] + agg_flag +'_DOD_FETCHED'],
                                       'y_axis_expression': map + aggregation_function + esc + kpi_list_mapping[page.Title] + agg_flag + 'Fetched}))", ",")'}
                else:
                    properties_dict = {'dt':Document.Data.Tables[page_to_dt_mapping[page.Title] + agg_flag +'_DOD'],
                                       'y_axis_expression': map + aggregation_function + esc + kpi_list_mapping[page.Title] + agg_flag + '}))", ",")'}
                set_bar_line_chart_properties(chart, properties_dict)
def get_bar_charts_properties(pages_list, agg_flag, aggregation_function):
    for page in pages_list:
        for vis in page.Visuals:
            if vis.TypeId == VisualTypeIdentifiers.BarChart:
                chart = vis.As[BarChart]()
                properties_dict = {}
                if 'Radio_Link_Performance' in page.Title and Document.Properties.get('EsrSesrFlag') == 'fetched':
                    dt_key = page_to_dt_mapping[page.Title] + agg_flag + '_DOD_FETCHED'
                    y_axis_expression = generate_y_axis_expression(aggregation_function, page.Title, agg_flag, True)
                else:
                    dt_key = page_to_dt_mapping[page.Title] + agg_flag + '_DOD'
                    y_axis_expression = generate_y_axis_expression(aggregation_function, page.Title, agg_flag, False)
                properties_dict = {'dt': Document.Data.Tables[dt_key], 'y_axis_expression': y_axis_expression}
                set_bar_line_chart_properties(chart, properties_dict)
        set_title_substring(page, aggregation_function)
def generate_y_axis_expression(aggregation_function, page_title, agg_flag, fetched):
    kpi_mapping = kpi_list_mapping[page_title]
    y_axis_expression_suffix = 'Fetched' if fetched else ''
    return '$map("{0}($esc(${{{1}{2}{3}}}))", ",")'.format(aggregation_function, kpi_mapping, agg_flag, y_axis_expression_suffix)
def set_bar_line_chart_properties(chart, properties_dict):
    pass #Logic for setting bar line chart properties
def set_title_substring(page, aggregation_function):
    if 'Interface' not in page.Title and 'Link Level' not in page.Title:
        title_key = bar_chart_title_substring_mapping.get(page.Title, aggregation_function)
    else:
        title_key = bar_chart_title_substring_interface_mapping.get(page.Title, aggregation_function)
    Document.Properties['BarChartTitleSubstring' + title_key] = aggregation_function
def set_bar_line_chart_properties(chart, properties_dict):
    chart.Data.DataTableReference = properties_dict['dt']
    chart.YAxis.Expression = properties_dict['y_axis_expression']
def refresh_data_flow(pages_list):
    agg_flag = Document.Properties[agg_doc_property_name_mapping[pages_list[0].Title]]
    aggregation_function = Document.Properties[agg_function_doc_property_name_mapping[pages_list[0].Title]]
    interface_page = get_page(interface_page_name_mapping[pages_list[0].Title])
    link_level_page = get_page(link_level_page_name_mapping[pages_list[0].Title])
    pages_list.append(interface_page)
    pages_list.append(link_level_page)
    get_bar_charts_properties(pages_list, agg_flag, aggregation_function)
    get_line_charts_properties(pages_list, agg_flag, aggregation_function)
    
def reset_filters_markings_flow(pages_list):
    for pg in pages_to_reset:
        pages_list[0] = get_page(pg)
        interface_page = get_page(interface_page_name_mapping[pages_list[0].Title])
        pages_list.append(interface_page)
        get_bar_charts_properties(pages_list, 'RAW', 'Avg')
        get_line_charts_properties(pages_list, 'RAW', 'Avg')
def get_page(page_name):
   for page in Document.Pages: 
      if page.Title == page_name: 
         return page
page = Document.ActivePageReference
pages_list = [page]
if page.Title != 'Home':
    refresh_data_flow(pages_list) 
else:
    reset_filters_markings_flow(pages_list)