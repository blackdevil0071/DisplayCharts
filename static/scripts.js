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
    console.log(chartType);
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
      console.log(event.target);
      modal.hide();
    }
  });

  if (window.location.pathname === "/chart.html") {
    const chartType = sessionStorage.getItem("chartType");
    if (!chartType) {
      $("#errorMsg").text("Please select the chart type from the home page.");
      return;
    }

    $.get(
      "/chart-data",
      function (response) {
        if (response.error) {
          $("#errorMsg").text(response.error);
          console.log(response.error);
          $("#myChart").hide();
        } else {
          const ctx = $("#myChart")[0].getContext("2d");
          console.log(ctx);
          new Chart(ctx, {
            type: chartType,
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
                      size: window.innerWidth < 600 ? 10 : 12,
                    },
                  },
                },
                y: {
                  ticks: {
                    color: "rgb(161, 158, 158)",
                    font: {
                      size: window.innerWidth < 600 ? 10 : 12,
                    },
                  },
                },
              },
              plugins: {
                tooltip: {
                  backgroundColor: "rgba(255, 255, 255, 0.9)",
                  titleColor: "#333",
                  bodyColor: "#333",
                  callbacks: {
                    label: function (tooltipItem) {
                      return tooltipItem.label + ': ' + tooltipItem.formattedValue;
                    },
                  },
                },
                legend: {
                  labels: {
                    color: "rgb(161, 158, 158)",
                    font: {
                      size: window.innerWidth < 600 ? 10 : 12,
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
