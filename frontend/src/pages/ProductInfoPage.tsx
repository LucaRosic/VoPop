import { useLocation } from "react-router-dom";
import BarGraph from "../components/BarGraph.tsx"
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, Filler } from "chart.js";

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, Filler);

export const ProductInfoPage = () => {

  const {state} = useLocation();
  if (state === null) {
    return (<h2>No give state.</h2>)
  }
  const {product} = state;
  
    return (
    <>  
      <p>{product.title}</p>
      <p>{product.id}</p>
      <a href="/dashboard">Go Back</a>    
      <BarGraph/>
    </>
  )
}
