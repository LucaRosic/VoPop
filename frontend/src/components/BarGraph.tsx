import {Bar, Line } from 'react-chartjs-2'
import { BarElement } from 'chart.js'
import {Chart as ChartJS} from 'chart.js'
import api from "../api"

ChartJS.register(
  BarElement
  );

const getData = async (index : number, prodId : number = 61) => {

  console.log("retrieving data")
  try {
    const res = await api.get(`/api/product/dashboard/sentiment/${prodId}/`);
    const apiData = res.data;
    console.log(apiData);
    return apiData[index]
  } catch (error) {
    console.log(error);
  }
}



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
      stacked: false,
      
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
  'December'
]

const month_shift = (list_to_shift : number[]|string[]) => {
  
  var today = new Date();
  var this_month = today.getMonth();
  var right_side = list_to_shift.slice(0,this_month+1)
  var left_side = list_to_shift.slice(this_month+1)

  return left_side.concat(right_side)
}

const data =
  {
    labels: months,
    datasets: [
    {
      label: "Positive",
      data: month_shift(await getData(0)),
      backgroundColor: '#1c8000'
    },
    {
      label: "Negative",
      data: month_shift(await getData(1)),
      backgroundColor: '#eb3434'
    },
    {
      label: "Neutral",
      data: month_shift(await getData(2)),
      backgroundColor: '#db8412',
      
    },
    ]
  }

var pos = await getData(0)
var neg = await getData(1)
var neu = await getData(2)
var nps = []
for (let i = 0; i < pos.length; i++){
  nps[i] = (pos[i]/(pos[i]+neg[i]+neu[i]) - neg[i]/(pos[i]+neg[i]+neu[i]))*100
}



const lineData =
{
  labels: month_shift(months),
  datasets: [
    {
      label: "NPS",
      data: month_shift(nps),
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
      <br />
      <Line data={lineData} options={lineOptions}/>
    </div>
    </div>
  )
}

export default BarGraph;