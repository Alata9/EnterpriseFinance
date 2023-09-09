google.charts.load('current', {'packages':['corechart']});
    google.charts.setOnLoadCallback(IncomeStructure);
    google.charts.setOnLoadCallback(PaymentsStructure);
    google.charts.setOnLoadCallback(IncomeDynamics);
    google.charts.setOnLoadCallback(PaymentsDynamics);
    google.charts.setOnLoadCallback(CashFlowDynamics);


    function IncomeStructure() {

        var data = new google.visualization.DataTable();
            data.addColumn('string', 'Items');
            data.addColumn('number', 'Amount');
            data.addRows({{ receipts_structure|safe }});

        var options = {
           title: 'Income structure',
           'width':350,
           'height':200,
           'is3D': true,
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
           title: 'Payments structure',
           'width':350,
           'height':200,
           'is3D': true,
           'legend': 'right'
           };

        var chart = new google.visualization.PieChart(document.getElementById('chart_payments_structure'));
        chart.draw(data, options);
    }


    function IncomeDynamics() {
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'Period');
        data.addColumn('number', 'Amount');
        data.addRows({{ receipts_dynamics|safe }});

        var options = {
          title: 'Receipts dynamics',
          curveType: 'function',
          legend: { position: 'bottom' }
        };

        var chart = new google.visualization.ColumnChart(document.getElementById('chart_income_dynamics'));
        chart.draw(data, options);
      }


    function PaymentsDynamics() {
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'Period');
        data.addColumn('number', 'Amount');
        data.addRows({{ payments_dynamics|safe }});

        var options = {
          title: 'Payments dynamics',
          curveType: 'function',
          legend: { position: 'bottom' }
        };

        var chart = new google.visualization.ColumnChart(document.getElementById('chart_payments_dynamics'));
        chart.draw(data, options);
      }


    function CashFlowDynamics() {
<!--        var data = new google.visualization.DataTable();-->
<!--        data.addColumn('string', 'Period');-->
<!--        data.addColumn('number', 'Amount');-->
<!--        data.addRows({{ cf_dynamics|safe }});-->

        var data = google.visualization.arrayToDataTable([
          ['Month', 'Income', 'Payments', 'Cash Flow', ],
          ['2004/05',  165,      938,         522,  ],
          ['2005/06',  135,      1120,        -599,  ],
          ['2006/07',  157,      1167,        587,  ],
          ['2007/08',  1390,      1110,        615,  ],
          ['2008/09',  136,      691,         -629,  ],
          ['2004/10',  165,      938,         522,  ],
          ['2005/11',  135,      1120,        -599,  ],
          ['2006/12',  157,      1167,        587,  ],
          ['2007/08',  1390,      1110,        615,  ],
          ['2008/09',  136,      691,         -629,  ]
        ]);

        var options = {
          title : 'Cash Flow Dynamics',
          vAxis: {title: 'Cups'},
          hAxis: {title: 'Month'},
          seriesType: 'bars',
          series: {2: {type: 'line'}}
        };

        var chart = new google.visualization.ComboChart(document.getElementById('chart_cash_flow_dynamics'));
        chart.draw(data, options);
      }