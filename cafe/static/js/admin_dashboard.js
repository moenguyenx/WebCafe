var myChart; // Declare myChart as a global variable

// Function to create the initial Chart.js chart
function createChart() {
    const ctx = document.getElementById('myChart');
    myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: [],
            datasets: [{
                data: [],
                backgroundColor: ['rgba(54, 162, 235, 0.75)'],
                borderColor: ['rgba(54, 162, 235, 1.5)'],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                    display: false
                },
                title: {
                    display: true,
                    text: 'Revenue Chart'
                },
                tooltip: {
                    boxPadding: 3
                }
            }
        }
    });
}

// Function to make an AJAX request and update the data
function updateData() {
    $.ajax({
        url: '/get_admin_data',
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            // Data retrieval successful
            totalRevenue = data.total_revenue;
            todayRevenue = data.today_revenue;
            labels = JSON.parse(data.labels);
            chartData = JSON.parse(data.data);

            // Use the retrieved data as needed
            console.log('Total Revenue:', totalRevenue);
            console.log('Today\'s Revenue:', todayRevenue);
            console.log('Labels:', labels);
            console.log('Chart Data:', chartData);

            // Update existing Chart.js chart with new data
            updateChart();
            // Update HTML
            updateHTML();
        },
        error: function (error) {
            // Handle errors
            console.error('Error retrieving data:', error);
        }
    });
}

// Function to update the existing Chart.js chart with new data
function updateChart() {
    // Update chart data
    myChart.data.labels = labels;
    myChart.data.datasets[0].data = chartData;

    // Update chart options if needed
    // myChart.options = ...

    // Update the chart
    myChart.update();
}

// Function to update HTML content of the div
function updateHTML() {
  // Update HTML content of the div
  $('.container-fluid .row .col-md-6:nth-child(1) h1').text('Today\'s revenue: ' + todayRevenue + '₫');
  $('.container-fluid .row .col-md-6:nth-child(2) h1').text('Total revenue: ' + totalRevenue + '₫');
}

// Initial data retrieval and chart creation
createChart();
updateData();

// Set up a periodic update every 5 seconds
setInterval(updateData, 5000);
