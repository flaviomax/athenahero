// Global parameters:
// do not resize the chart canvas when its container does (keep at 600x400px)
Chart.defaults.global.responsive = true;

function basicChart({canvasId, legend, labels, values, chartType}) {
    var chartData = {
        labels : labels,
        datasets : [{
            label: legend,
            fill: true,
            lineTension: 0.1,
            backgroundColor: "rgba(75,192,192,0.4)",
            borderColor: "rgba(75,192,192,1)",
            borderCapStyle: 'butt',
            borderDash: [],
            borderDashOffset: 0.0,
            borderJoinStyle: 'miter',
            pointBorderColor: "rgba(75,192,192,1)",
            pointBackgroundColor: "#fff",
            pointBorderWidth: 1,
            pointHoverRadius: 5,
            pointHoverBackgroundColor: "rgba(75,192,192,1)",
            pointHoverBorderColor: "rgba(220,220,220,1)",
            pointHoverBorderWidth: 2,
            pointRadius: 1,
            pointHitRadius: 10,
            data : values,
            spanGaps: false
        }]
    }
  
 // get chart canvas
    var ctx = document.getElementById(canvasId).getContext("2d");
    
    // create the chart using the chart canvas
    var testChart = new Chart(ctx, {
        type: chartType,
        data: chartData,
    });
}