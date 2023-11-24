    google.charts.load('current', {'packages':['corechart']});
    google.charts.setOnLoadCallback(CashFlowDynamics);
    google.charts.setOnLoadCallback(CashFlowBar);

    google.charts.load('current', {'packages':['table']});
    google.charts.setOnLoadCallback(TableBalancesAccount);
    google.charts.setOnLoadCallback(TableCashFlow);


    function CashFlowBar() {
        var data = new google.visualization.DataTable();
            data.addColumn('string', 'Items');
            data.addColumn('number', 'Amount');
            data.addRows(cfBarData);

        var options = {
           'width':400,
           'height':210,
           colors: ['#FFA500'],
           legend: { position: 'none' }
           };

        var chart = new google.visualization.BarChart(document.getElementById('cf_bar'));
        chart.draw(data, options);
    }


    function CashFlowDynamics() {
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'Period');
        data.addColumn('number', 'Receipts');
        data.addColumn('number', 'Payments');
        data.addColumn('number', 'Cash Flow');
        data.addRows(cfDynamicsData);

        var options = {
          height:280,
          vAxis: {title: 'Amount'},
          hAxis: {title: 'Period'},
          colors: ['#00CED1', '#FF4500', '2F4F4F'],
          seriesType: 'bars',
          series: {2: {type: 'line'}},
          legend: { position: 'bottom' }
        };

        var chart = new google.visualization.ComboChart(document.getElementById('chart_cash_flow_dynamics'));
        chart.draw(data, options);
      }


      function TableBalancesAccount() {
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'Account');
        data.addColumn('number', 'Amount');
        data.addColumn('string', 'Currency');
        data.addRows(accountBalancesData);

        var table = new google.visualization.Table(document.getElementById('table_balances_account'));

        table.draw(data, {showRowNumber: true, width: '100%', height: '100%'});
      }


      function TableCashFlow() {
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'Item');
        data.addColumn('number', 'Operating');
        data.addColumn('number', 'Investment');
        data.addColumn('number', 'Financing');
        data.addColumn('number', 'Total');
        data.addRows(cfTableData);


        var table = new google.visualization.Table(document.getElementById('cf_table'));

        table.draw(data, {showRowNumber: true, width: '100%', height: '100%'});
      }