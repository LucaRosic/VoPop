import { useLocation } from "react-router-dom";
import BarGraph from "../components/BarGraph.tsx"
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, Filler } from "chart.js";
import DummyData from "../DummyData.ts";

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
        <div className="w-1/3 bg-green-100 flex flex-col items-center">
        <span className="text-xl">{productInfo.title}</span>
        <img
          className="object-cover w-[60%] h-64 rounded-lg"
          src={productInfo.img}
        >
        </img>
        </div>

        {/* Sidebar right */}
        <div className="w-2/3 bg-red-200 flex flex-col items-center">
          <span className="">Sentiment</span>
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
