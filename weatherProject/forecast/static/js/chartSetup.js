document.addEventListener('DOMContentLoaded', () => {
  const chart = document.getElementById('chart');
  if (!chart) {
    console.error('Chart not found');
    return;
  }
  const ctx = chart.getContext('2d');
  const gradient = ctx.createLinearGradient(0,-10,0,100);
  gradient.addColorStop(0, 'rgba(250,0,255,1)');
  gradient.addColorStop(1, 'rgba(136,255,255,1)');

  const forecastItems = document.querySelectorAll('.forecast-item');
  const temps = [];
  const times = [];

  forecastItems.forEach(item => {
    const time = item.querySelector('.forecast-time').textContent;
    const temp = item.querySelector('.forecast-temperatureValue').textContent;
    const hump = item.querySelector('.forecast-humidityValue').textContent;

    if (time && temp && hump) {
      temps.push(temp);
      times.push(time);
    }
  });
  if (times.length === 0 || temps.length === 0) {
    console.error('Invalid time or temp');
    return;
  }

  new Chart(ctx, {
    type: 'line',
    data: {
      labels: times,
      datasets: [
        {
          label: 'Celcius Degree',
          data: temps,
          borderColor: gradient,
          borderWidth: 2,
          tension: 0.4,
          pointRadius: 2,
        },
      ],
    },
    options: {
      plugins: {
        legend: {
          display: false,
        },
      },
      scales: {
        x: {
          display: false,
          grid: { drawOnChartArea: false },
        },
        y: {
          display: false,
          grid: { drawOnChartArea: false },
        },
      },
      animation: {
        duration: 750,
      },
    },
  });
});

