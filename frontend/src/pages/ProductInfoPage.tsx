import { useLocation} from "react-router-dom";
import BarGraph from "../components/BarGraph.tsx"
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, Filler } from "chart.js";
import DummyData from "../DummyData.ts";
import { Button } from "@mui/material";
import ArrowBackIosNewIcon from '@mui/icons-material/ArrowBackIosNew';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, Filler);

export const ProductInfoPage = () => {

  const {state} = useLocation();
  // If state is not given:
  if (state === null) {
    return (
      <>
        <h2>No give state.</h2>
        <p><a href='/dummy'>Dashboard</a></p>
      </>
    )
  }
  const {prodId} = state;
  const productInfo = DummyData(prodId); // Get the product data information
  
    return (
      <div className="flex h-[100vh]">
        {/* Sidebar left */}
        <div className="w-1/3 bg-slate-800 flex flex-col items-center gap-4 py-4">
          {/* <button className="self-start bg-gray-900 text-white px-8 py-1"><ArrowBackIosNewIcon /> Dashboard</button> */}
          <div className="self-start ml-2">
            <Button 
              className="rounded-none bg-black"
              variant="contained" 
              startIcon={<ArrowBackIosNewIcon />}
              href="/dummy"
            >
              Dashboard
            </Button>
          </div>
          
          {/* Product information */}
          <div className="product-snippet flex flex-col w-[80%] bg-gray-900 text-white shadow-[10px_10px_0px_0px_rgba(35,106,114)]">
            <h1 className="text-xl text-center">{productInfo.title}</h1>
            <img
              className="w-[100%] h-64 object-cover border-2 border-gray-900"
              src={productInfo.img}
            ></img>
          </div>
        </div>

        {/* Sidebar right */}
        <div className="w-2/3 bg-slate-100 flex flex-col gap-4 p-4 items-center overflow-y-auto">
          <span className="text-xl bg-gray-900 px-4 py-2 text-white">Product Sentiment</span>
          <div className="bg-white rounded-lg"><BarGraph /></div>
        </div>
      </div>

    // <>  
    //   <p>{productInfo.title}</p>
    //   <p>{prodId}</p>
    //   <img
    //       className="w-[60%] h-[40%] object-cover rounded-lg shadow-sm dark:shadow-gray-800"
    //       src={productInfo.img}
    //     ></img>
    //   <a href="/dashboard">Go Back</a>    
    //   <BarGraph/>
    // </>
  )
}
