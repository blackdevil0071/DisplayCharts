$(document).ready(function () {
  const modal = $("#chartModal");
  const closeModal = $(".close");

  $("#chooseChartBtn").click(function () {
    modal.show();
  });

  closeModal.click(function () {
    modal.hide();
  });

  $("#submitChartType").click(function () {
    const chartType = $("#chartType").val();
    if (chartType) {
      sessionStorage.setItem("chartType", chartType);
      $.post(
        "/set-chart-type",
        JSON.stringify({ chartType: chartType }),
        function () {
          window.location.href = "chart.html";
        }
      );
    } else {
      alert("Please select a chart type.");
    }
  });

  $(window).click(function (event) {
    if ($(event.target).is(modal)) {
      modal.hide();
    }
  });

  if (window.location.pathname === "/chart.html") {
    $.get(
      "/chart-data",
      function (response) {
        if (response.error) {
          $("#errorMsg").text(response.error);
          $("#myChart").hide();
        } else {
          const ctx = $("#myChart")[0].getContext("2d");
          new Chart(ctx, {
            type: sessionStorage.getItem("chartType"),
            data: {
              labels: response.labels,
              datasets: [
                {
                  label: "Sample Data",
                  data: response.data,
                  borderColor: "rgb(161, 158, 158)",
                  backgroundColor: "rgba(161, 158, 158, 0.5)",
                  hoverBorderColor: "white",
                  hoverBackgroundColor: "white"
                },
              ],
            },
            options: {
              responsive: true,
              maintainAspectRatio: false,
              scales: {
                x: {
                  ticks: {
                    color: "rgb(161, 158, 158)",
                    font: {
                      size: window.innerWidth < 600 ? 10 : 12, // Adjust font size based on screen width
                    },
                  },
                },
                y: {
                  ticks: {
                    color: "rgb(161, 158, 158)",
                    font: {
                      size: window.innerWidth < 600 ? 10 : 12, // Adjust font size based on screen width
                    },
                  },
                },
              },
              plugins: {
                tooltip: {
                  backgroundColor: "rgba(255, 255, 255, 0.9)", // Light color for tooltip background
                  titleColor: "#333", // Dark color for tooltip title text
                  bodyColor: "#333", // Dark color for tooltip body text
                  callbacks: {
                    label: function (tooltipItem) {
                      return tooltipItem.label + ': ' + tooltipItem.formattedValue; // Custom label format
                    },
                  },
                },
                legend: {
                  labels: {
                    color: "rgb(161, 158, 158)",
                    font: {
                      size: window.innerWidth < 600 ? 10 : 12, // Adjust font size based on screen width
                    },
                  },
                },
              },
              hover: {
                mode: 'nearest',
                intersect: true
              }
            },
          });
        }
      },
      "json"
    );
  }
});
