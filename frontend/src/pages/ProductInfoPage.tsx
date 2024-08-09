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
        <p><a href='/dashboard'>Dashboard</a></p>
      </>
    )
  }
  const {prodId} = state;
  const productInfo = DummyData(prodId); // Get the product data information
  
    return (
      <div className="flex h-[100vh]">
        {/* Sidebar left */}
        <div className="w-1/3 bg-slate-800 flex flex-col items-center gap-4">
          <div className="self-start mt-2 ml-2">
            <Button 
              variant="contained" 
              startIcon={<ArrowBackIosNewIcon />}
              href="/dashboard"
            >
              Dashboard
            </Button>
          </div>
          

          <span className="text-xl bg-white px-4 py-2 rounded-lg">{productInfo.title}</span>
          <img
            className="object-cover w-[60%] h-64 rounded-lg"
            src={productInfo.img}
          >
          </img>
        </div>

        {/* Sidebar right */}
        <div className="w-2/3 bg-slate-100 flex flex-col gap-4 pt-16 items-center">
          <span className="text-xl bg-slate-800 px-4 py-2 rounded-lg text-white">Product Sentiment</span>
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
