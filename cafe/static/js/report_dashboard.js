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
                    text: 'Bestseller Chart'
                },
                tooltip: {
                    boxPadding: 3
                }
            }
        }
    });
}

