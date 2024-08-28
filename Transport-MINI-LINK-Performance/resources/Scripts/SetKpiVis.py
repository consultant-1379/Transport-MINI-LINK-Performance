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
# Name    : SetKpiVis.py
# Date    : 16/05/2023
# Revision: 2.0
# Purpose : Configures KPI chart and its' tiles based on KPI and aggregation function filter selection
#
# Usage   : Transport Report
#

from Spotfire.Dxp.Data import DataValueCursor, IndexSet, DataProperty, DataType, DataPropertyClass,RowSelection, IndexSet, LimitingMarkingsEmptyBehavior
from Spotfire.Dxp.Application.Filters import CheckBoxFilter
from Spotfire.Dxp.Application.Visuals import VisualTypeIdentifiers,BarChart,VisualContent,LineChart,TablePlot, AxisRange,Visualization,KpiChart
from System.Drawing import Color
from Spotfire.Dxp.Application.Visuals.ConditionalColoring import RuleComparisonOperator, ConditionValue
from System import DateTime

Ethernet_Traffic = 'Ethernet Traffic'
Ethernet_Bandwidth_Utilization = 'Ethernet Bandwidth Utilization'
Radio_Link_Performance = 'Radio Link Performance'

agg_doc_property_name_mapping = {Ethernet_Traffic: 'AggregationTR', Ethernet_Bandwidth_Utilization: 'AggregationBU', Radio_Link_Performance: 'AggregationRL'}
page_name_doc_proper_name_mapping = {Ethernet_Traffic: 'TrafficKpi', Ethernet_Bandwidth_Utilization: 'BandwidthUtilizationKPI', Radio_Link_Performance: 'RadioLinkPerformanceKpi'}
container_dt_name_mapping = {Ethernet_Traffic: 'IL_DC_E_IPTRANSPORT_ETH_TRAFFIC_', Ethernet_Bandwidth_Utilization: 'IL_DC_E_IPTRANSPORT_ETH_BANDWIDTH_', Radio_Link_Performance: 'IL_DC_E_IPTRANSPORT_RADIOLINKG826_'}

bu_kpi_name_mapping = {'Bw0To5': 'Seconds (Interval 0-5%)', 'Bw5To10': 'Seconds (Interval 5-10%)', 'Bw10To15': 'Seconds Interval (10-15%)', 'Bw15To20': 'Seconds Interval (15-20%)', 
                    'Bw20To25': 'Seconds (Interval 20-25%)', 'Bw25To30': 'Seconds (Interval 25-30%)', 'Bw30To35': 'Seconds (Interval 30-35%)', 'Bw35To40': 'Seconds (Interval 35-40%)', 
                    'Bw40To45': 'Seconds (Interval 40-45%)', 'Bw45To50': 'Seconds (Interval 45-50%)', 'Bw50To55': 'Seconds (Interval 50-55%)', 'Bw55To60': 'Seconds (Interval 55-60%)', 
                    'Bw60To65': 'Seconds (Interval 60-65%)', 'Bw65To70': 'Seconds (Interval 65-70%)', 'Bw70To75': 'Seconds (Interval 70-75%)', 'Bw75To80': 'Seconds (Interval 75-80%)', 
                    'Bw80To85': 'Seconds (Interval 80-85%)', 'Bw85To90': 'Seconds (Interval 85-90%)', 'Bw90To95': 'Seconds (Interval 90-95%)', 'Bw95To100': 'Seconds (Interval 95-100%)'}

bu_kpi_exceptions = ['BwAvg', 'BwMax', 'BwMin', 'Peak_Utilization']
rl_tr_kpi_exceptions = ['SNIR_Max', 'SNIR_Min', 'XPI_Max', 'XPI_Min', 'ESR', 'SESR', 'ESR_Calculated', 'SESR_Calculated', 'Link Quality', 'Link Availability', 'RxLevelMin', 'RxLevelMax', 'TxLevelMin', 'TxLevel', 'TxLevelMax', 'RxLevel']
bu_kpi_exceptions_name_mapping = {'BwAvg': 'Average Bandwidth per Node', 'BwMax': 'Max Bandwidth per Node', 'BwMin': 'Min Bandwidth per Node', 'Peak_Utilization':'Peak Utilization (%) per Node'}
kpi_expressions_dict = {'rl_tr': 'Sum([{kpi}]) as [Total {kpi_name_processed} per Node]', 'rl_ex': 'Avg([{kpi}]) as [{kpi_name_processed} per Node]', 
                        'rl_ex_min': 'Min([{kpi}]) as [{kpi_name_processed} per Node]', 'rl_ex_max': 'Max([{kpi}]) as [{kpi_name_processed} per Node]',
                        'bu': 'Sum({kpi}) as [Total {kpi_name_processed} ]', 'bu_avg': 'Avg({kpi}) as [{kpi_name_processed}]', 'bu_max': 'Max({kpi}) as [{kpi_name_processed}]',
                        'bu_min': 'Min({kpi}) as [{kpi_name_processed}]'}
reset_filters_initial_pages = [Ethernet_Traffic, Ethernet_Bandwidth_Utilization, Radio_Link_Performance]


def add_kpi_chart_tile(chart, page, kpi, aggregation, kpi_type_flag):

    kpi_content = chart.KpiCollection.AddNew()
    kpi_chart_tile = kpi_content.Visualization
    if page.Title ==Ethernet_Traffic:
		kpi_chart_tile.Data.Filterings.Add(Document.Data.Markings["MarkingTr"])
		kpi_chart_tile.Data.LimitingMarkingsEmptyBehavior = LimitingMarkingsEmptyBehavior.ShowAll
    elif page.Title ==Ethernet_Bandwidth_Utilization:
		kpi_chart_tile.Data.Filterings.Add(Document.Data.Markings["MarkingBu"])
		kpi_chart_tile.Data.LimitingMarkingsEmptyBehavior = LimitingMarkingsEmptyBehavior.ShowAll
    elif page.Title ==Radio_Link_Performance:
		kpi_chart_tile.Data.Filterings.Add(Document.Data.Markings["MarkingRl"])
		kpi_chart_tile.Data.LimitingMarkingsEmptyBehavior = LimitingMarkingsEmptyBehavior.ShowAll
    if page.Title == Radio_Link_Performance and Document.Properties['EsrSesrFlag'] == 'fetched':
        kpi_chart_tile.Data.DataTableReference = Document.Data.Tables[container_dt_name_mapping[page.Title] + aggregation + '_DOD_FETCHED']
    else:
        kpi_chart_tile.Data.DataTableReference = Document.Data.Tables[container_dt_name_mapping[page.Title] + aggregation + '_DOD']
    if 'bu' not in kpi_type_flag:
        kpi_chart_tile.YAxis.Expression = kpi_expressions_dict[kpi_type_flag].format(kpi=kpi, kpi_name_processed=kpi.replace('_',' '))
    elif kpi not in bu_kpi_exceptions:
        kpi_chart_tile.YAxis.Expression = kpi_expressions_dict[kpi_type_flag].format(kpi=kpi, kpi_name_processed=bu_kpi_name_mapping[kpi])
    else:
        kpi_chart_tile.YAxis.Expression = kpi_expressions_dict[kpi_type_flag].format(kpi=kpi, kpi_name_processed=bu_kpi_exceptions_name_mapping[kpi])

    set_coloring(kpi, kpi_chart_tile)
    set_x_tile_axes_expressions(kpi_chart_tile)
       

def set_coloring(kpi, kpi_chart_tile):

    kpi_chart_tile.ColorAxis.Expression = 'Sum(['+kpi+'])'
    kpi_chart_tile.ShowSparkline = False
    kpi_visualization_coloring = kpi_chart_tile.ColorAxis.Coloring
    kpi_visualization_coloring.Clear()
    color_rule = kpi_visualization_coloring.AddThresholdColorRule(RuleComparisonOperator.GreaterOrEqual, ConditionValue.CreateLiteral(-1000000000), Color.FromArgb(160, 160, 160))
    color_rule.ManualDisplayName = "All values"


def set_x_tile_axes_expressions(kpi_chart_tile):

    kpi_chart_tile.XAxis.Expression = 'Node_Name'
    kpi_chart_tile.TileAxis.Expression = '<[Node_Name]>'


def bandwidth_tile_handling(aggregation, chart, kpi, page):

   if kpi in bu_kpi_exceptions:
      if 'Avg' in kpi:
         add_kpi_chart_tile(chart, page, kpi, aggregation, kpi_type_flag='bu_avg')
      elif 'Max' in kpi or 'Peak' in kpi:
         add_kpi_chart_tile(chart, page, kpi, aggregation, kpi_type_flag='bu_max')
      else:
         add_kpi_chart_tile(chart, page, kpi, aggregation, kpi_type_flag='bu_min')
   else:
      add_kpi_chart_tile(chart, page, kpi, aggregation, kpi_type_flag='bu')


def configure_kpi_chart_vis(page, aggregation):

   for vis in page.Visuals:
      if vis.TypeId == VisualTypeIdentifiers.KpiChart:
         chart = vis.As[KpiChart]()
         chart.KpiCollection.Clear()
         kpi_doc_prop = ''
         if page.Title == Radio_Link_Performance and Document.Properties['EsrSesrFlag'] == 'fetched':
            kpi_doc_prop = Document.Properties[page_name_doc_proper_name_mapping[page.Title] + aggregation + 'FETCHED']
            call_configure_kpi_chart(kpi_doc_prop,page, aggregation,chart)
         else:
            kpi_doc_prop = Document.Properties[page_name_doc_proper_name_mapping[page.Title] + aggregation]
            call_configure_kpi_chart(kpi_doc_prop,page, aggregation,chart)
			
def call_configure_kpi_chart(kpi_doc_prop, page, aggregation, chart):

	for kpi in kpi_doc_prop:
		if 'Bandwidth' in page.Title:
			bandwidth_tile_handling(aggregation, chart, kpi, page) 
		elif kpi not in rl_tr_kpi_exceptions:
			add_kpi_chart_tile(chart, page, kpi, aggregation, kpi_type_flag = 'rl_tr')
		elif 'Min' in kpi:
			add_kpi_chart_tile(chart, page, kpi, aggregation, kpi_type_flag = 'rl_ex_min')
		elif 'Max' in kpi:
			add_kpi_chart_tile(chart, page, kpi, aggregation, kpi_type_flag = 'rl_ex_max')
		else:
			add_kpi_chart_tile(chart, page, kpi, aggregation, kpi_type_flag = 'rl_ex')
                

def refresh_data_flow(initial_page):

    aggregation = Document.Properties[agg_doc_property_name_mapping[initial_page.Title]]               
    configure_kpi_chart_vis(initial_page,aggregation)


def reset_filters_markings_flow():

    for reset_filters_page in reset_filters_initial_pages:
        initial_page = get_page(reset_filters_page)
        configure_kpi_chart_vis(initial_page,'RAW')


def get_page(page_name):

   for page in Document.Pages: 
      if page.Title == page_name: 
         return page


initial_page = Document.ActivePageReference

if initial_page.Title != 'Home':
    refresh_data_flow(initial_page)
else:
    reset_filters_markings_flow()

Document.Properties['SetAggregationFunctionScriptTrigger'] = DateTime.UtcNow