# ********************************************************************
# Ericsson Inc.                                                 SCRIPT
# ********************************************************************
#
#
# (c) Ericsson Inc. 2022 - All rights reserved.
#
# The copyright to the computer program(s) herein is the property
# of Ericsson Inc. The programs may be used and/or copied only with
# the written permission from Ericsson Inc. or in accordance with the
# terms and conditions stipulated in the agreement/contract under
# which the program(s) have been supplied.
#
# ********************************************************************
# Name    :  ResetFiltersAndMarkings.py
# Date    :  10/11/2022
# Revision:  1.0
# Purpose :  Resets filters, markings, sliders, document properties to the default values when 'Reset All Markings and Filters' button clicked in the home page
#
# Usage   :  Transport Report
#

from Spotfire.Dxp.Data import DataValueCursor, IndexSet, DataProperty, DataType, DataPropertyClass,RowSelection, IndexSet
from Spotfire.Dxp.Application.Filters import CheckBoxFilter
from System.Collections.Generic import List,  Dictionary
from Spotfire.Dxp.Application.Visuals import VisualTypeIdentifiers,BarChart,VisualContent,LineChart,TablePlot, AxisRange,Visualization
from Spotfire.Dxp.Application import Filters as filters


reset_tables_list = ['IL_DC_E_IPTRANSPORT_ETH_TRAFFIC_RAW_DOD', 'IL_DC_E_IPTRANSPORT_ETH_TRAFFIC_DAY_DOD', 'IL_DC_E_IPTRANSPORT_ETH_BANDWIDTH_RAW_DOD', 'IL_DC_E_IPTRANSPORT_ETH_BANDWIDTH_DAY_DOD', 
                     'IL_DC_E_IPTRANSPORT_RADIOLINKG826_RAW_DOD', 'IL_DC_E_IPTRANSPORT_RADIOLINKG826_DAY_DOD', 'IL_DC_E_IPTRANSPORT_RADIOLINKG826_RAW_DOD_FETCHED', 'IL_DC_E_IPTRANSPORT_RADIOLINKG826_DAY_DOD_FETCHED']
aggregation_mapping = {'IL_DC_E_IPTRANSPORT_ETH_TRAFFIC_RAW_DOD': 'AggregationTR', 'IL_DC_E_IPTRANSPORT_ETH_TRAFFIC_DAY_DOD': 'AggregationTR', 'IL_DC_E_IPTRANSPORT_ETH_BANDWIDTH_RAW_DOD': 'AggregationBU', 
                       'IL_DC_E_IPTRANSPORT_ETH_BANDWIDTH_DAY_DOD': 'AggregationBU', 'IL_DC_E_IPTRANSPORT_RADIOLINKG826_RAW_DOD': 'AggregationRL', 'IL_DC_E_IPTRANSPORT_RADIOLINKG826_DAY_DOD': 'AggregationRL', 
                       'IL_DC_E_IPTRANSPORT_RADIOLINKG826_RAW_DOD_FETCHED': 'AggregationRL', 'IL_DC_E_IPTRANSPORT_RADIOLINKG826_DAY_DOD_FETCHED': 'AggregationRL'}
aggregation_function_mapping = {'IL_DC_E_IPTRANSPORT_ETH_TRAFFIC_RAW_DOD': 'AggregationFunctionTR', 'IL_DC_E_IPTRANSPORT_ETH_TRAFFIC_DAY_DOD': 'AggregationFunctionTR', 'IL_DC_E_IPTRANSPORT_ETH_BANDWIDTH_RAW_DOD': 'AggregationFunctionBU', 
                                'IL_DC_E_IPTRANSPORT_ETH_BANDWIDTH_DAY_DOD': 'AggregationFunctionBU', 'IL_DC_E_IPTRANSPORT_RADIOLINKG826_RAW_DOD': 'AggregationFunctionRL', 'IL_DC_E_IPTRANSPORT_RADIOLINKG826_DAY_DOD': 'AggregationFunctionRL',
                                'IL_DC_E_IPTRANSPORT_RADIOLINKG826_RAW_DOD_FETCHED': 'AggregationFunctionRL', 'IL_DC_E_IPTRANSPORT_RADIOLINKG826_DAY_DOD_FETCHED': 'AggregationFunctionRL'}
network_type_mapping = {'IL_DC_E_IPTRANSPORT_ETH_TRAFFIC_RAW_DOD': 'NetworkTypeTrafficRAW', 'IL_DC_E_IPTRANSPORT_ETH_TRAFFIC_DAY_DOD': 'NetworkTypeTrafficDAY', 'IL_DC_E_IPTRANSPORT_ETH_BANDWIDTH_RAW_DOD': 'NetworkTypeBandwidthUtilizationRAW', 
                       'IL_DC_E_IPTRANSPORT_ETH_BANDWIDTH_DAY_DOD': 'NetworkTypeBandwidthUtilizationDAY'}
reset_pages_list = ['Ethernet Traffic', 'Ethernet Bandwidth Utilization', 'Radio Link Performance']
filter_indexes = {'Ethernet Traffic': [0, 4], 'Ethernet Bandwidth Utilization': [6, 7], 'Radio Link Performance': [13, 14]}


def reset_marking_and_filtering(): 
	
    for data_table in Document.Data.Tables: 
        for marking in Document.Data.Markings: 
            rows = RowSelection(IndexSet(data_table.RowCount,  False))
            marking.SetSelection(rows,  data_table)
                
        for filter_scheme in Document.FilteringSchemes: 
            filter_scheme.ResetAllFilters()


def reset_sliders(): 

    for page in Application.Document.Pages: 
        for visualization in page.Visuals: 
            if visualization.TypeId == VisualTypeIdentifiers.BarChart: 
                current_chart = visualization.As[BarChart]()
                current_chart.XAxis.ZoomRange = AxisRange(None, None)
            elif visualization.TypeId == VisualTypeIdentifiers.LineChart: 
                current_chart = visualization.As[LineChart]()
                current_chart.XAxis.ZoomRange = AxisRange(None, None)


def reset_doc_properties(): 

    for table in reset_tables_list: 
        if 'RADIOLINKG826' not in table: 
            target_data_table = Document.Data.Tables[table]
            network_type_filter_raw = Document.FilteringSchemes[0].Item[target_data_table]["MOC"].As[CheckBoxFilter]()
            for value in network_type_filter_raw.Values: 
                network_type_filter_raw.Uncheck(value)
                network_type_filter_raw.Check('LAN')

        Document.Properties[aggregation_mapping[table]] = 'RAW'
        Document.Properties[aggregation_function_mapping[table]] = 'Avg'
        if 'RADIOLINKG826' not in table: 
            Document.Properties[network_type_mapping[table]] = 'LAN'

    Document.Properties['BandwidthUtilizationKpiRAW'] = 'BwAvg'
    Document.Properties['BandwidthUtilizationKpiDAY'] = 'BwAvg'
    Document.Properties['TrafficKpiRAW'] = 'Unicast_Packets'
    Document.Properties['TrafficKpiDAY'] = 'Unicast_Packets'
    Document.Properties['RadioLinkPerformanceKpiRAW'] = 'BB'
    Document.Properties['RadioLinkPerformanceKpiRAWFetched'] = 'BB'
    Document.Properties['RadioLinkPerformanceKpiDAY'] = 'BB'
    Document.Properties['RadioLinkPerformanceKpiDAYFetched'] = 'BB'


def reset_node_filter(): 

    for reset_page_title in reset_pages_list:
        page = get_page(reset_page_title) 
        filters_panel = page.FilterPanel
        filter_raw = filters_panel.TableGroups[filter_indexes[page.Title][1]].GetFilter("Node_Name")
        filter_day = filters_panel.TableGroups[filter_indexes[page.Title][0]].GetFilter("Node_Name")
        list_box_filter_raw = filter_raw.FilterReference.As[filters.ListBoxFilter]()
        list_box_filter_day = filter_day.FilterReference.As[filters.ListBoxFilter]()
        set_selection = set()
        list_box_filter_raw.IncludeAllValues = False
        list_box_filter_raw.SetSelection(set_selection)
        list_box_filter_day.IncludeAllValues = False
        list_box_filter_day.SetSelection(set_selection)


def reset_filter_col(): 

    for table in reset_tables_list: 
        target_data_table = Document.Data.Tables[table]
        filter_col_filter = Document.FilteringSchemes[0].Item[target_data_table]["Filter Col"].As[CheckBoxFilter]()
        for _ in filter_col_filter.Values: 
            filter_col_filter.Uncheck('True')


def add_marking_holder(): 

    for reset_page_title in reset_pages_list:
        page = get_page(reset_page_title)
        for visualization in page.Visuals: 
            if visualization.TypeId == VisualTypeIdentifiers.BarChart: 
                visualization = visualization.As[Visualization]()
                visualization.Data.Filterings.Add(Document.Data.Markings["MarkingHolder"])


def get_page(page_name):

   for page in Document.Pages: 
      if page.Title == page_name: 
         return page


reset_marking_and_filtering()
reset_sliders()
reset_doc_properties()
reset_node_filter()
reset_filter_col()
add_marking_holder()