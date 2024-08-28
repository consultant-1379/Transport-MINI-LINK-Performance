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
# Name    : ReturnToPage.py
# Date    : 03/09/2022
# Revision: 1.0
# Purpose : Navigating user from filtered data page to node level page
#
# Usage   : Transport Report
#

from Spotfire.Dxp.Data import DataValueCursor, IndexSet, DataProperty, DataType, DataPropertyClass,RowSelection, IndexSet
from Spotfire.Dxp.Application.Filters import CheckBoxFilter
from Spotfire.Dxp.Application.Visuals import VisualTypeIdentifiers,BarChart,VisualContent,LineChart,TablePlot, AxisRange,Visualization

page_mapping = {'TRAFFIC_FILTERED': 'Ethernet Traffic', 'BANDWIDTH_FILTERED': 'Ethernet Bandwidth Utilization', 'RADIO_LINK_FILTERED': 'Radio Link Performance'}

markings_mapping = {'TRAFFIC_FILTERED': ['Filtered Traffic', 'MarkingTr'], 
                    'BANDWIDTH_FILTERED': ['Filtered Bandwidth Utilization', 'MarkingBu'], 
                    'RADIO_LINK_FILTERED': ['Filtered Radio Link', 'MarkingRl']}


def get_table_plot(page):

    for visual in page.Visuals:
        if visual.Title == "FilteredDataVis":
            return visual.As[TablePlot]()


def get_page(page_name):

   for page in Document.Pages: 
      if page.Title == page_name: 
         return page


page = Document.ActivePageReference
table_plot_vis = get_table_plot(page)
markings = markings_mapping[page.Title]

for marking in markings:
    table_plot_vis.Data.Filterings.Remove(Document.Data.Markings[marking])

Document.ActivePageReference = get_page(page_mapping[page.Title])