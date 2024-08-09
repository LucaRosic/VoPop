// import ReactDOM from 'react-dom'
// import React from 'react'
import {Bar} from 'react-chartjs-2'
import {Chart, registerables} from 'chart.js'
// import {Chart as ChartJS} from 'chart.js'

Chart.register(...registerables)

export const options = {
  responsive: true,
  plugins: {
    legend: {
      display: false,
    },
    title: {
      display: false,
    },
    colors: {
      enabled: true,
    },

  },
  scales: {
    x: {
      display: false,
    },
    y: {
      grid: {
        display: true,
      },
      border: {
        display: false,
      },
      ticks: {
        display: false,
      },
    },
  },
}

const graphData = Array.from({length: 40}, () =>
  Math.floor(Math.random() * 100),
)

const months = [
  'January',
  'February',
  'March',
  'April',
  'May',
  'June',
  'July',
  'August',
  'September',
  'October',
  'November',
  'December',
]
const labels = graphData.map((_, index) => months[index % 12])
export const data = {
  labels,
  datasets: [
    {
      backgroundColor: '#5052ff',
      data: graphData,
      barPercentage: 1,
      borderRadius: 100,
      borderSkipped: false,
    },
  ],
}

const BarGraph = () => {
  const graphStyle = {
    minHeight: '10rem',
    maxWidth: '540px',
    width: '100%',
    border: '1px solid #C4C4C4',
    borderRadius: '0.375rem',
    padding: '1rem',
  }

  return (
    <div style={graphStyle}>
      <Bar data={data} options={options} />
    </div>
  )
}

export default BarGraph;