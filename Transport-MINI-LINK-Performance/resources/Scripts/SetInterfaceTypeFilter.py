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
# Name    : SetInterfaceTypeFilter.py
# Date    : 21/07/2022
# Revision: 1.0
# Purpose : Sets MOC (interface type) filter value to LAN/WAN
#
# Usage   : Transport Report
#

from Spotfire.Dxp.Application.Filters import CheckBoxFilter
from System import DateTime

EthernetTraffic='Ethernet Traffic'
EthernetBandwidthUtilization='Ethernet Bandwidth Utilization'
RadioLinkPerformance='Radio Link Performance'
container_dt_name_mapping = {EthernetTraffic: 'IL_DC_E_IPTRANSPORT_ETH_TRAFFIC_', EthernetBandwidthUtilization: 'IL_DC_E_IPTRANSPORT_ETH_BANDWIDTH_'}
interface_type_doc_property_name_mapping = {EthernetTraffic: 'NetworkTypeTraffic', EthernetBandwidthUtilization: 'NetworkTypeBandwidthUtilization'}
trigger_doc_proper_name_mapping = {EthernetTraffic: 'SetKpiVisScriptTriggerTr', EthernetBandwidthUtilization: 'SetKpiVisScriptTriggerBu'}
agg_doc_property_name_mapping = {EthernetTraffic: 'AggregationTR', EthernetBandwidthUtilization: 'AggregationBU', RadioLinkPerformance: 'AggregationRL'}
reset_filters_initial_pages = ['Ethernet Traffic', 'Ethernet Bandwidth Utilization']


def refresh_data_flow(page):

    aggregation = Document.Properties[agg_doc_property_name_mapping[page.Title]]
    target_data_table = Document.Data.Tables[container_dt_name_mapping[page.Title] + aggregation + '_DOD']
    interface_type_filter = Document.FilteringSchemes[0].Item[target_data_table]["MOC"].As[CheckBoxFilter]()

    for value in interface_type_filter.Values:
        interface_type_filter.Uncheck(value)
        interface_type_filter.Check(Document.Properties[interface_type_doc_property_name_mapping[page.Title] + aggregation])
    Document.Properties['SetKpiVisScriptTrigger'] = DateTime.UtcNow


def reset_filters_markings_flow():

    for reset_filters_page in reset_filters_initial_pages:
        page = get_page(reset_filters_page)
        target_data_table = Document.Data.Tables[container_dt_name_mapping[page.Title] + 'RAW_DOD']
        interface_type_filter = Document.FilteringSchemes[0].Item[target_data_table]["MOC"].As[CheckBoxFilter]()

        for value in interface_type_filter.Values:
            interface_type_filter.Uncheck(value)
            interface_type_filter.Check(Document.Properties[interface_type_doc_property_name_mapping[page.Title] + 'RAW'])


def get_page(page_name):

   for page in Document.Pages: 
      if page.Title == page_name: 
         return page


page = Document.ActivePageReference

if page.Title != 'Home':
    refresh_data_flow(page)
else:
    reset_filters_markings_flow()
    