import { useLocation, useNavigate } from "react-router-dom";
import BarGraph from "../components/BarGraph.tsx";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler,
} from "chart.js";
import { Button } from "@mui/material";
// MUI ICONS -------------------
import ArrowBackIosNewIcon from "@mui/icons-material/ArrowBackIosNew";
import StarBorderIcon from '@mui/icons-material/StarBorder';
import StarHalfIcon from '@mui/icons-material/StarHalf';
import StarIcon from '@mui/icons-material/Star';
// ---------------
import api from "../api.ts";
import { useEffect, useState } from "react";
import ReactMarkdown from "react-markdown";
import LineGraph from "../components/LineGraph.tsx";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

ChartJS.defaults.color = "#fff";

export const ProductInfoPage = () => {
  /*
    Page to render more in-depth information about the product.

    This page shows sentiment graph and full review summary.
  */

  const { state } = useLocation(); // Get state information passed
  
  // If state information about page is not given, take back to dashboard
  if (state === null) {
    return (
      <>
        <h2>No give state.</h2>
        <p>
          <a href="/dashboard">Dashboard</a>
        </p>
      </>
    );
  }

  const { prodId } = state;
  const [productSummary, setProductSummary] = useState<string>("");
  const [productData, setProductData] = useState<any>({});
  const [productRating, setProductRating] = useState<number>(0);

  const getProductInformation = async () => {
    // API calls with product id
    /*
      API endpoints:
        - product/dashboard/sentiment/<int:product_id>/
        - product/dashboard/meta/<int:product_id>/
        - product/dashboard/summ/<int:product_id>/
    */

    console.log("Calling META api:");
    try {
      const res = await api.get(`/api/product/dashboard/meta/${prodId}/`);
      console.log("Obtaining META:")
      console.log(res.data);
      setProductData(res.data[0]);
    } catch (error) {
      console.log(error);
    }

    console.log("Calling Summary api:");
    try {
      const res = await api.get(`/api/product/dashboard/summ/${prodId}/`);
      console.log(res.data);
      setProductSummary(res.data[0]["summary"]);
      setProductRating(Number(res.data[0]["avg_rating"]))
    } catch (error) {
      console.log(error);
    }

  }

  // On page entry, get product information based on product id
  useEffect(() => {
    console.log(`Product ID: ${prodId}`);
    getProductInformation();
  }, []);

  /*
    Things to add to product info page:
      - Star rating
      - Emoji sentiment (along with average sentiment score)
  */

  const navigate = useNavigate();
  // Using react router -> States will persist I think!
  const backToDashboard = () => {
    console.log("Going back to Dashboard!");
    navigate("/dashboard")
  }


  const renderStars = (productRating : number) => {
    
    const numFullStars = Math.trunc(productRating);
    const remainder = productRating % 1;
    const numHalfStars = remainder >= 0.5 ? 1 : 0; // If decimal remainder is above or equal 0.5, you have half star
    const numEmptyStars = 5 - numFullStars - numHalfStars; // Fill the rest out

    return (
      <>
      {[...Array(numFullStars).keys()].map(key => <StarIcon key={key}/>)}
      {[...Array(numHalfStars).keys()].map(key => <StarHalfIcon key={key}/>)}
      {[...Array(numEmptyStars).keys()].map(key => <StarBorderIcon key={key}/>)}
      </>
    )
  }

  const renderSourceLogo = (category: string) => {
    if (category === "Amazon") {
      return <img className="h-[50px]" src="/images/amazon_icon.png" />
    } else if (category === "AliExpress") {
      return <img className="h-[50px]" src="/images/aliexpress_icon.png" />
    }
  }

  return (
    // =========================
    <div className="flex h-[100vh]">
      
      {/* Sidebar left */}
      {/* ------ */}
      <div className="w-1/3 bg-[#FBF5F3] border-2 border-gray-900 flex flex-col items-center gap-4 py-4 overflow-y-auto">
        <div className="self-start ml-2">
          <Button
            className="rounded-none bg-black shadow-none"
            variant="contained"
            startIcon={<ArrowBackIosNewIcon />}
            onClick={backToDashboard}
          >
            Dashboard
          </Button>
        </div>

        {/* Product information */}
        <div className="product-snippet flex flex-col w-[80%] bg-gray-900 text-white shadow-[10px_10px_0px_0px_rgba(35,106,114)]">
          <h1 className="text-xl text-center">{productData["name"]}</h1>
          <img
            className="w-[100%] h-64 object-cover border-2 border-gray-900"
            src={productData["image"]}
          ></img>
        </div>

        {/* Star rating */}
        <div>
          {renderStars(productRating)}
        </div>

        {/* Source logo */}
        <div className="flex flex-row items-center gap-4">
          <span className="font-bold">SOURCE:</span> {renderSourceLogo(productData["category"])}
        </div>

      </div>
      {/* ------ */}

      {/* Sidebar right */}
      {/* ------ */}
      <div className="w-2/3 bg-[rgba(35,106,114)] flex flex-col gap-4 p-4 items-center overflow-y-auto border-4 border-gray-900">
        <div className="bg-gray-900 pb-4 w-[80%] flex flex-col items-center border-2 border-gray-900 justify-between shadow-[10px_10px_0px_0px_rgba(251,245,243)] gap-1">
          <h1 className="text-xl bg-gray-900 text-white">
            <button className="hover:bg-gray-800 p-1 text-3xl">Product Sentiment</button>
          </h1>

          {/* Sentiment Graph */}
          <div className="bg-gray-900 w-[100%] flex flex-col items-center">
            <BarGraph productId={prodId} />
            <LineGraph productId={prodId} />
          </div>
        </div>
        
        <div className="bg-gray-900 py-2 px-8 pb-4 w-[80%] flex flex-col items-center border-2 border-gray-900 justify-between shadow-[10px_10px_0px_0px_rgba(251,245,243)] gap-1">
          
          {/* Review Summary */}
          <ReactMarkdown children={productSummary} className="text-white text-sm px-2 mt-4" />
        </div>
        {/* ------ */}
        
      </div>
    </div>
  );
};
