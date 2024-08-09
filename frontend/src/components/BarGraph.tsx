import {Bar, Line } from 'react-chartjs-2'
import { BarElement } from 'chart.js'
import {Chart as ChartJS} from 'chart.js'

ChartJS.register(
  BarElement
  );

 export const barOptions = {
  responsive: true,
  plugins: {
    legend: {
      display: true,
    },
    title: {
      display: true,
      text: "Review counts from past 12 months"
    },
    colors: {
      enabled: true,
    },
    
    

  },
  scales: {
    x: {
      display: false,
      stacked: false
    },
    y: {
      grid: {
        display: true,
      },
      border: {
        display: true,
      },
      ticks: {
        display: true,
      },
    },
  },
 }

 export const lineOptions = {
  responsive: true,
  plugins: {
    legend: {
      display: false,
    },
    title: {
      display: true,
      text: "NPS from past 12 months",
    },
    colors: {
      enabled: true,
    },
    

  },
  scales: {
    x: {
      display: true,
    },
    y: {
      display:true,
      min: -100,
      max: 100,
      grid: {
        display: true,
      },
      border: {
        display: true,
      },
      ticks: {
        display: true,
      },
    },
  },
 }
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

const data =
  {
    labels: months,
    datasets: [
    {
      label: "Positive",
      data: [...Array(12)].map(e=>~~(Math.random()*80)),
      backgroundColor: '#1c8000'
    },
    {
      label: "Negative",
      data: [...Array(12)].map(e=>~~(Math.random()*80)),
      backgroundColor: '#eb3434'
    },
    {
      label: "Neutral",
      data: [...Array(12)].map(e=>~~(Math.random()*80)),
      backgroundColor: '#db8412',
      
    },
    ]
  }
  
const lineData =
{
  labels: months,
  datasets: [
    {
      label: "NPS",
      data: [...Array(12)].map(e=>~~(Math.random()*100)),
      backgroundColor: '#db8412',
      borderColor: '#0b13a3',
      tension: 0.1

    }, 
  ]
}


const BarGraph = () => {
  const graphStyle = {
    minHeight: '20rem',
    minWidth: '600px',
    width: '100%',
    border: '1px solid #C4C4C4',
    borderRadius: '0.375rem',
    padding: '1rem',
  }

  return (
    <div>
    <div style={graphStyle}>
      <Bar data={data} options={barOptions} />
      <Line data={lineData} options={lineOptions}/>
    </div>
    </div>
  )
}

export default BarGraph;