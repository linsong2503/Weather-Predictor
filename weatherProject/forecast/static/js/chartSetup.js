// document.addEventListener('DOMContentLoaded', () => {
//   const chartElement = document.getElementById('chart');
//   if (!chartElement) {
//     console.error('Chart not found');
//     return;
//   }
//   const ctx = chartElement.getContext('2d');
//   const gradient = ctx.createLinearGradient(0, -10, 0, 100);
//   gradient.addColorStop(0, 'rgba(250,0,0,1)');
//   gradient.addColorStop(1, 'rgba(136,255,0,1)');

//   const forecastItems = document.querySelectorAll('.forecast-item');
//   const temps = [];
//   const times = [];

//   forecastItems.forEach(item => {
//     const time = item.querySelector('.forecast-time').textContent;
//     const temp = item.querySelector('.forecast-temperatureValue').textContent;
//     const hump = item.querySelector('.forecast-humidityValue').textContent;

//     if (time && temp && hump) {
//       temps.push(temp);
//       times.push(time);
//     }
//   });
//   if (times.length === 0 || temps.length === 0) {
//     console.error('Invalid time or temp');
//     return;
//   }

//   new Chart(ctx, {
//     type: 'line',
//     data: {
//       labels: times,
//       datasets: [
//         {
//           label: 'Celcius Degree',
//           data: temps,
//           borderColor: gradient,
//           borderWidth: 2,
//           tension: 0.4,
//           pointRadius: 2,
//         },
//       ],
//     },
//     options: {
//       plugins: {
//         legend: {
//           display: false,
//         },
//       },
//       scales: {
//         x: {
//           display: false,
//           grid: { drawOnChartArea: false },
//         },
//         y: {
//           display: false,
//           grid: { drawOnChartArea: false },
//         },
//       },
//       animation: {
//         duration: 750,
//       },
//     },
//   });
// });

// document.addEventListener('DOMContentLoaded', () => {
//   const chartElement = document.getElementById('chart');
//   if (!chartElement) {
//     console.error('Chart not found');
//     return;
//   }

//   const ctx = chartElement.getContext('2d');
//   const gradient = ctx.createLinearGradient(0, -10, 0, 100);
//   gradient.addColorStop(0, 'rgba(250,0,0,1)');
//   gradient.addColorStop(1, 'rgba(136,255,0,1)');

//   const forecastItems = document.querySelectorAll('.forecast-item');
//   const temps = [];
//   const times = [];

//   forecastItems.forEach((item) => {
//     const timeEl = item.querySelector('.forecast-time');
//     const tempEl = item.querySelector('.forecast-temperatureValue');

//     if (timeEl && tempEl) {
//       const time = timeEl.textContent;
//       const temp = parseFloat(tempEl.textContent);
//       if (time && !isNaN(temp)) {
//         times.push(time);
//         temps.push(temp);
//       }
//     }
//   });

//   if (times.length === 0 || temps.length === 0) {
//     console.error('Invalid time or temp');
//     return;
//   }

//   new Chart(ctx, {
//     type: 'line',
//     data: {
//       labels: times,
//       datasets: [{
//         label: 'Celsius Degree',
//         data: temps,
//         borderColor: gradient,
//         borderWidth: 2,
//         tension: 0.4,
//         pointRadius: 2,
//       }],
//     },
//     options: {
//       responsive: true,
//       maintainAspectRatio: false,
//       plugins: {
//         legend: { display: false },
//       },
//       scales: {
//         x: { display: false, grid: { drawOnChartArea: false } },
//         y: { display: false, grid: { drawOnChartArea: false } },
//       },
//       animation: { duration: 750 },
//     },
//   });
// });
