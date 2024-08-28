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
# Name    : ActiveVisualBarChart.py
# Date    : 21/07/2022
# Revision: 1.0
# Purpose : Sets document property flag value to determine which visualization (barchart or linechart) is currently active.
#
# Usage   : Transport Report
#

from Spotfire.Dxp.Application.Visuals import VisualTypeIdentifiers,BarChart,VisualContent,LineChart
active_visual = Document.ActiveVisualReference
vis = active_visual.As[VisualContent]()
if vis.TypeId in [VisualTypeIdentifiers.LineChart, VisualTypeIdentifiers.BarChart]:
    Document.Properties['ActiveVisualReference'] = 'barchart' if vis.TypeId == VisualTypeIdentifiers.BarChart else 'linechart'


