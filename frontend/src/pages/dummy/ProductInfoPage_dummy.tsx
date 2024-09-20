import { useLocation, useNavigate } from "react-router-dom";
import ReactMarkdown from 'react-markdown';
import BarGraph from "../../components/BarGraph.tsx";
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
import DummyData, { GetMarkdownReview } from "../../DummyData.ts";
import { Button } from "@mui/material";
import ArrowBackIosNewIcon from "@mui/icons-material/ArrowBackIosNew";

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

export const ProductInfoPage_dummy = () => {
  /*
    This is a product information dummy page. This page is to work without
    needing any established connection with the backend server.
  */

  const { state } = useLocation();
  // If state is not given:
  if (state === null) {
    return (
      <>
        <h2>No give state.</h2>
        <p>
          <a href="/dummy">Dashboard</a>
        </p>
      </>
    );
  }
  const { prodId } = state;
  const productInfo = DummyData(prodId); // Get the product data information

  const markdownReview = GetMarkdownReview();

  const navigate = useNavigate();
  const backToDashboard = () => {
    navigate("/dummy")
  }

  return (
    <div className="flex h-[100vh]">
      {/* Sidebar left */}
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
          <h1 className="text-xl text-center">{productInfo.title}</h1>
          <img
            className="w-[100%] h-64 object-cover border-2 border-gray-900"
            src={productInfo.img}
          ></img>
        </div>
      </div>

      {/* Sidebar right */}
      <div className="w-2/3 bg-[rgba(35,106,114)] flex flex-col gap-4 p-4 items-center overflow-y-auto border-4 border-gray-900">
        <div className="bg-gray-900 flex flex-col items-center border-2 border-gray-900 justify-between shadow-[10px_10px_0px_0px_rgba(251,245,243)] gap-1">
          <h1 className="text-xl bg-gray-900 text-white">
            <button className="hover:bg-gray-800 p-1">Product Sentiment</button>
          </h1>

          {/* Sentiment Graph */}
          <div className="bg-slate-100">
            <BarGraph />
          </div>

          {/* Review Summary */}
          <ReactMarkdown children={markdownReview} className="text-white text-sm px-2 mt-4" />
        </div>
      </div>
    </div>
  );
};
