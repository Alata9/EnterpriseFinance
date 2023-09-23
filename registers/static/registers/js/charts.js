document.addEventListener('DOMContentLoaded', function()
{

        google.charts.load('current', {'packages':['corechart']});
        google.charts.setOnLoadCallback(IncomeStructure);
        google.charts.setOnLoadCallback(PaymentsStructure);
        google.charts.setOnLoadCallback(rpDynamics);
        google.charts.setOnLoadCallback(CashFlowDynamics);

        google.charts.load('current', {'packages':['table']});
        google.charts.setOnLoadCallback(TableBalances);
        google.charts.setOnLoadCallback(CFTable);


        function IncomeStructure() {

        var data = new google.visualization.DataTable();
        data.addColumn('string', 'Items');
        data.addColumn('number', 'Amount');
        data.addRows({{ receipts_structure|safe }});

        var options = {
        'width':350,
        'height':200,
        'is3D': false,
        'legend': 'right'
        };

        var chart = new google.visualization.PieChart(document.getElementById('chart_income_structure'));
        chart.draw(data, options);
        }



        function PaymentsStructure() {

        var data = new google.visualization.DataTable();
        data.addColumn('string', 'Items');
        data.addColumn('number', 'Amount');
        data.addRows({{ payments_structure|safe }});

        var options = {
        'width':350,
        'height':200,
        'is3D': false,
        'legend': 'right'
        };

        var chart = new google.visualization.PieChart(document.getElementById('chart_payments_structure'));
        chart.draw(data, options);
        }


        function rpDynamics() {
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'Period');
        data.addColumn('number', 'Receipts');
        data.addColumn('number', 'Payments');
        data.addRows({{ rp_dynamics |safe }});

        var options = {
          curveType: 'function',
          legend: { position: 'bottom' }
        };

        var chart = new google.visualization.LineChart(document.getElementById('chart_rp_dynamics'));
        chart.draw(data, options);
        }


        function CashFlowDynamics() {
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'Period');
        data.addColumn('number', 'Receipts');
        data.addColumn('number', 'Payments');
        data.addColumn('number', 'Cash Flow');
        data.addRows({{ cf_dynamics|safe }});

        var options = {
          vAxis: {title: 'Amount'},
          hAxis: {title: 'Period'},
          seriesType: 'bars',
          series: {2: {type: 'line'}},
          legend: { position: 'bottom' }
        };

        var chart = new google.visualization.ComboChart(document.getElementById('chart_cash_flow_dynamics'));
        chart.draw(data, options);
        }


        function TableBalances() {
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'Currency');
        data.addColumn('number', 'Amount');
        data.addRows([
          ['USD',  10000],
          ['EUR',  8000],
          ['ILS',  12456],
          ['RUB',  450000]
        ]);

        var table = new google.visualization.Table(document.getElementById('table_balances'));

        table.draw(data, {showRowNumber: true, width: '100%', height: '100%'});
        }


        function CFTable() {
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'Item');
        data.addColumn('number', 'Cash flow');
        data.addRows({{ cf_table|safe }});


        var table = new google.visualization.Table(document.getElementById('cf_table'));

        table.draw(data, {showRowNumber: true, width: '100%', height: '100%'});
        }

});
