function createBarChart(canvasId, labels, data, labelName) {
    new Chart(document.getElementById(canvasId), {
        type: "bar",
        data: {
            labels: labels,
            datasets: [{
                label: labelName,
                data: data
            }]
        }
    });
}

function createPieChart(canvasId, labels, data) {
    new Chart(document.getElementById(canvasId), {
        type: "pie",
        data: {
            labels: labels,
            datasets: [{
                data: data
            }]
        }
    });
}
