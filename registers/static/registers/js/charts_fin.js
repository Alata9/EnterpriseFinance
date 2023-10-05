    google.charts.load('current', {'packages':['corechart']});
    google.charts.setOnLoadCallback(DebitPortfolio);
    google.charts.setOnLoadCallback(LoanPortfolio);
    google.charts.setOnLoadCallback(CashFlowFinanceDynamics);

    google.charts.load('current', {'packages':['table']});
    google.charts.setOnLoadCallback(BorrowersTable);
    google.charts.setOnLoadCallback(LendersTable);



    function DebitPortfolio() {

    var data = new google.visualization.DataTable();
        data.addColumn('string', 'Borrowers');
        data.addColumn('number', 'Amount');
        data.addRows(debit_portfolioData);

    var options = {
       'width':350,
       'height':200,
       colors: ['#008B8B', '#20B2AA', '#00CED1', '#40E0D0', '#AFEEEE'],
       'legend': 'right'
       };

    var chart = new google.visualization.PieChart(document.getElementById('debit_portfolio'));
    chart.draw(data, options);
}


    function LoanPortfolio() {

    var data = new google.visualization.DataTable();
        data.addColumn('string', 'Lenders');
        data.addColumn('number', 'Amount');
        data.addRows(loan_portfolioData);

    var options = {
       'width':350,
       'height':200,
       colors: ['#FF4500', '#FF8C00', '#FFA500', '#FFD700', '#FFFF00'],
       'legend': 'right'
       };

    var chart = new google.visualization.PieChart(document.getElementById('loan_portfolio'));
    chart.draw(data, options);
}


    function BorrowersTable() {
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'Borrower');
        data.addColumn('number', 'Debit');
        data.addColumn('number', 'Credit');
        data.addColumn('number', 'Receipts');
        data.addColumn('number', 'Payments');
        data.addColumn('number', 'Debit');
        data.addColumn('number', 'Credit');
        data.addRows(borrowers_tableData);


        var table = new google.visualization.Table(document.getElementById('borrowers_table'));

        table.draw(data, {showRowNumber: true, width: '100%', height: '100%'});
      }


    function LendersTable() {
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'Lenders');
        data.addColumn('number', 'Debit');
        data.addColumn('number', 'Credit');
        data.addColumn('number', 'Receipts');
        data.addColumn('number', 'Payments');
        data.addColumn('number', 'Debit');
        data.addColumn('number', 'Credit');
        data.addRows(lenders_tableData);


        var table = new google.visualization.Table(document.getElementById('lenders_table'));

        table.draw(data, {showRowNumber: true, width: '100%', height: '100%'});
      }



    function CashFlowFinanceDynamics() {
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'Period');
        data.addColumn('number', 'Receipts');
        data.addColumn('number', 'Payments');
        data.addColumn('number', 'Cash Flow');
        data.addRows(cf_fin_dynamicsData);

        var options = {
          height:280,
//          vAxis: {title: 'Amount'},
//          hAxis: {title: 'Period'},
          colors: ['#00CED1', '#FF4500', '2F4F4F'],
          seriesType: 'bars',
          series: {2: {type: 'line'}},
          legend: { position: 'bottom' }
        };

        var chart = new google.visualization.ComboChart(document.getElementById('cf_fin_dynamics'));
        chart.draw(data, options);
      }