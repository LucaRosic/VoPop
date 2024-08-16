import "./css/product-card.css";
import DummyData from "../DummyData";

//--------------
// MUI ui stuff:
import ArrowRightAltIcon from "@mui/icons-material/ArrowRightAlt";
import DeleteIcon from "@mui/icons-material/Delete";
import { styled } from "@mui/material/styles";
//--------------

interface Props {
  productId: number;
  productTitle: string;
  productImg: string;
  productOverview: string;
  lastUpdated: string;
  onClick?: () => void;
}

// Look into MUI typography for better text

export const ProductCard = ({ productTitle, productImg, productOverview, lastUpdated, onClick = () => null }: Props) => {

  // Style arrow icon
  const StyledArrowRightAltIcon = styled(ArrowRightAltIcon)(() => ({
    fontSize: "50px", // Adjust the size as needed
    // Add other custom styles here
  }));

 
  return (
    <div
      className="product-card bg-slate-100 w-[60vw] h-60 rounded-lg px-8 pr-4 py-4 flex justify-between shadow-sm dark:shadow-gray-800 gap-2 border-2 
      border-gray-200 select-none transform hover:scale-[1.02] transition-transform"
      onClick={onClick}
    > 
      <div className="product-snippet flex flex-col w-[30%] h-[100%]">
        <h1 className="text-xl text-center">{productTitle}</h1>
        <img
            className="w-[100%] h-[80%] object-cover rounded-lg shadow-sm dark:shadow-gray-800"
          src={productImg}
        ></img>
      </div>

      <div className="cx-info-brief flex flex-col justify-between w-[65%]">
        <div className="flex justify-center mt-2 items-center">
          <div className="bg-gray-700 rounded-lg text-white text-center flex items-center p-1 w-full justify-center">
            <span className="text-lg">Customer Sentiment</span>
            <StyledArrowRightAltIcon fontSize="large"></StyledArrowRightAltIcon>
            <span className="text-5xl mb-1">{"None"}</span>
          </div>
        </div>

        <fieldset className="px-3 border rounded-lg shadow-sm dark:shadow-gray-800 bg-slate-200">
          <legend className="float-none w-auto px-3 text-center text-lg bg-gray-700 text-white rounded-lg pb-1">
            Brief Summary ✨
          </legend>
          <p className="text-sm">{productOverview}</p>
        </fieldset>
      </div>

      <div className="updated-delete flex flex-col items-center">
        <p className="text-xs text-center text-gray-400">
          Last Updated<br />{lastUpdated}
        </p>
        <div
          className="bg-red-600 border-2 hover:bg-red-800 border-red-800 p-2 rounded-lg"
          onClick={() => null}
        >
          <DeleteIcon></DeleteIcon>
        </div>
      </div>
    </div>
  );
};

/*
- A div for the card
- There is product title
- There is product image


*/
