/* globals Chart:false */
document.addEventListener("DOMContentLoaded", function() {
    console.log(labels);
    console.log(data);
});

(() => {
  'use strict'

  // Graphs
  const ctx = document.getElementById('myChart')
  // eslint-disable-next-line no-unused-vars
  const myChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        data: data,
        backgroundColor: '#007bff',
        pointBackgroundColor: '#007bff'
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
  })
})()
