google.charts.load('current', {'packages':['corechart']});
    google.charts.setOnLoadCallback(IncomeStructure);
    google.charts.setOnLoadCallback(PaymentsStructure);
    google.charts.setOnLoadCallback(rpDynamics);
    google.charts.setOnLoadCallback(IncomeBar);
    google.charts.setOnLoadCallback(PaymentsBar);
    google.charts.setOnLoadCallback(TopCustomers);
    google.charts.setOnLoadCallback(TopSuppliers);



    function IncomeStructure() {

    var data = new google.visualization.DataTable();
        data.addColumn('string', 'Items');
        data.addColumn('number', 'Amount');
        data.addRows({{ receipts_structure|safe }});

    var options = {
       'width':350,
       'height':200,
       colors: ['#008B8B', '#20B2AA', '#00CED1', '#40E0D0', '#AFEEEE'],
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
       colors: ['#FF4500', '#FF8C00', '#FFA500', '#FFD700', '#FFFF00'],
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
          colors: ['#008B8B', '#FF4500'],
          legend: { position: 'bottom' }
        };

    var chart = new google.visualization.LineChart(document.getElementById('chart_rp_dynamics'));
    chart.draw(data, options);
  }


      function IncomeBar() {

    var data = new google.visualization.DataTable();
        data.addColumn('string', 'Items');
        data.addColumn('number', 'Amount');
        data.addRows({{ receipts_structure|safe }});

    var options = {
       'width':350,
       'height':200,
       colors: ['#008B8B'],
       legend: {position: 'none'},
       hAxis: {minValue:0}
       };

    var chart = new google.visualization.BarChart(document.getElementById('chart_income_bar'));
    chart.draw(data, options);
}

function PaymentsBar() {

    var data = new google.visualization.DataTable();
        data.addColumn('string', 'Items');
        data.addColumn('number', 'Amount');
        data.addRows({{ payments_bar|safe }});

    var options = {
       'width':350,
       'height':200,
       colors: ['FF4500'],
       legend: {position: 'none'},
       hAxis: {minValue:0}
       };

    var chart = new google.visualization.BarChart(document.getElementById('chart_payments_bar'));
    chart.draw(data, options);
}


function TopCustomers() {

    var data = new google.visualization.DataTable();
        data.addColumn('string', 'Items');
        data.addColumn('number', 'Amount');
        data.addRows({{ top_customers|safe }});

    var options = {
       'width':350,
       'height':200,
       colors: ['#00CED1'],
       legend: {position: 'none'},
       hAxis: {minValue:0}
       };

    var chart = new google.visualization.BarChart(document.getElementById('chart_top_customers'));
    chart.draw(data, options);
}

function TopSuppliers() {

    var data = new google.visualization.DataTable();
        data.addColumn('string', 'Items');
        data.addColumn('number', 'Amount');
        data.addRows({{ top_suppliers|safe }});

    var options = {
       'width':350,
       'height':200,
       colors: ['FF8C00'],
       legend: {position: 'none'},
       hAxis: {minValue:0}
       };

    var chart = new google.visualization.BarChart(document.getElementById('chart_top_suppliers'));
    chart.draw(data, options);
}
