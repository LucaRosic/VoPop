import { Line } from 'react-chartjs-2'
import { BarElement } from 'chart.js'
import {Chart as ChartJS} from 'chart.js'
import api from "../api"
import { useEffect, useState } from 'react';

ChartJS.register(
  BarElement
);

interface Props {
  productId? : number;
}

const LineGraph = ({productId=61} : Props) => {
  // ============================


  const getData = async (index : number, prodId : number = 61) => {

    console.log("retrieving data")
    try {
      const res = await api.get(`/api/product/dashboard/sentiment/${prodId}/`);
      const apiData = res.data;
      console.log(apiData);
      return apiData[index]
    } catch (error) {
      console.log(error);
      return Promise.reject("API for sentiment failed.");
    }
  }

  const lineOptions = {
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
    
    let today = new Date();
    let this_month = today.getMonth();
    let right_side = list_to_shift.slice(0,this_month+1)
    let left_side = list_to_shift.slice(this_month+1)

    return left_side.concat(right_side)
  }

  const calculateLineData = async () => {
    try{
      const pos = await getData(0, productId)
      const neg = await getData(1, productId)
      const neu = await getData(2, productId)
      const nps = []
      for (let i = 0; i < pos.length; i++){
        nps[i] = (pos[i]/(pos[i]+neg[i]+neu[i]) - neg[i]/(pos[i]+neg[i]+neu[i]))*100
      }

      // return linedata;
      return {
        labels: month_shift(months),
        datasets: [
          {
            label: "NPS",
            data: month_shift(nps),
            backgroundColor: '#286c74',
            borderColor: '#286c74',
            tension: 0.1

          }, 
        ]
      }
    } catch (error) {
      console.log(error)
      return undefined;
    }
    

  }

  
  const [lineData, setLineData] = useState<any>(undefined);
  useEffect(() => {
    calculateLineData().then((value) => setLineData(value));
  }, [])



  const graphStyle = {
    minHeight: '20rem',
    minWidth: '600px',
    width: '100%',
    border: '1px solid #C4C4C4',
    borderRadius: '0.375rem',
    padding: '1rem',
  }

  if (lineData === undefined) {
    return (<div className='h-48 flex items-center p-4'>Error Getting Sentiment Data</div>)
  } else {
    return (
    <div>
    <div style={graphStyle}>
      <Line data={lineData} options={lineOptions}/>
    </div>
    </div>
    )
  }
  
  
}

export default LineGraph;