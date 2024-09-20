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
import ArrowBackIosNewIcon from "@mui/icons-material/ArrowBackIosNew";
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

  return (
    // =========================
    <div className="flex h-[100vh]">
      
      {/* Sidebar left */}
      {/* ------ */}
      <div className="w-1/3 bg-[#FBF5F3] border-2 border-gray-900 flex flex-col items-center gap-4 py-4">
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
      </div>
      {/* ------ */}

      {/* Sidebar right */}
      {/* ------ */}
      <div className="w-2/3 bg-[rgba(35,106,114)] flex flex-col gap-4 p-4 items-center overflow-y-auto border-4 border-gray-900">
        <div className="bg-gray-900 flex flex-col items-center border-2 border-gray-900 justify-between shadow-[10px_10px_0px_0px_rgba(251,245,243)] gap-1">
          <h1 className="text-xl bg-gray-900 text-white">
            <button className="hover:bg-gray-800 p-1">Product Sentiment</button>
          </h1>

          {/* Sentiment Graph */}
          <div className="bg-slate-100">
            <BarGraph productId={prodId} />
            <LineGraph productId={prodId} />
          </div>
          

          {/* Review Summary */}
          <ReactMarkdown children={productSummary} className="text-white text-sm px-2 mt-4" />
        </div>
        {/* ------ */}
        
      </div>
    </div>
  );
};
