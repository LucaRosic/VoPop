import { useLocation } from "react-router-dom";
import BarGraph from "../components/BarGraph.tsx"
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, Filler } from "chart.js";
import DummyData from "../DummyData.ts";

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, Filler);

export const ProductInfoPage = () => {

  const {state} = useLocation();
  if (state === null) {
    return (<h2>No give state.</h2>)
  }
  const {prodId} = state;
  const productInfo = DummyData(prodId);
  
    return (
    <>  
      <p>{productInfo.title}</p>
      <p>{prodId}</p>
      <a href="/dashboard">Go Back</a>    
      <BarGraph/>
    </>
  )
}
