import {Bar } from 'react-chartjs-2'
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

const BarGraph = ({productId=61} : Props) => {
  // ============================

  const getData = async (prodId : number = 61) => {

    console.log("retrieving data")
    try {
      const res = await api.get(`/api/product/dashboard/sentiment/${prodId}/`);
      const apiData = res.data;
      console.log(apiData);
      return apiData
    } catch (error) {
      console.log(error);
      return Promise.reject("API for sentiment failed.");
    }
  }

  const barOptions = {
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
        display: true,
        stacked: true,
        
      },
      
      y: {
        stacked: true,
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

  const getGraphData = (sentimentData : number[][]) => {
    try {
      const data =
      {
        labels: month_shift(months),
        datasets: [
        {
          label: "Positive",
          data: month_shift(sentimentData[0]),
          backgroundColor: '#1c8000'
        },
        {
          label: "Negative",
          data: month_shift(sentimentData[1]),
          backgroundColor: '#eb3434'
        },
        {
          label: "Neutral",
          data: month_shift(sentimentData[2]),
          backgroundColor: '#db8412',
          
        },
        ]
      };
      return data;
    } catch (error) {
      console.log(error);
      return undefined;
    }
    
  }

  const [data, setData] = useState<any>(undefined);

  useEffect(() => {
    getData(productId).then((res) => {
      console.log("GETTING SENTIMENT DATA");
      setData(getGraphData(res));
    })
  }, [])
  // useEffect(() => {
  //   getGraphData().then((value) => setData(value));
  //   calculateLineData().then((value) => setLineData(value));
  // }, [])



  const graphStyle = {
    minHeight: '20rem',
    minWidth: '600px',
    width: '100%',
    border: '1px solid #C4C4C4',
    borderRadius: '0.375rem',
    padding: '1rem',
  }

  console.log(`DATA: ${data}`);
  if (data === undefined) {
    return (<div className='h-48 flex items-center p-4'>Error Getting Sentiment Data</div>)
  } else {
    return (
    <div>
    <div style={graphStyle}>
      <Bar data={data} options={barOptions} />
    </div>
    </div>
    )
  }
  
  
}

export default BarGraph;