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
  onClick?: () => void;
}

// Look into MUI typography for better text

export const ProductCard = ({ productId, onClick = () => null }: Props) => {
  const productInfo = DummyData(productId);

  // Style arrow icon
  const StyledArrowRightAltIcon = styled(ArrowRightAltIcon)(() => ({
    fontSize: "50px", // Adjust the size as needed
    // Add other custom styles here
  }));

  return (
    <div
      className="product-card bg-gradient-to-t from-slate-100 via-slate-300 to-slate-100 w-[60vw] h-60 rounded-lg px-8 pr-0 py-4 flex shadow-sm dark:shadow-gray-800 gap-4 border-2 
      border-gray-200 transform hover:scale-[1.02] transition-transform"
      onClick={onClick}
    >
      <div className="product-snippet flex flex-col w-[20vw]">
        <h1 className="text-xl text-center">{productInfo.title}</h1>
        <img
          className="w-[100%] h-[80%] object-cover rounded-lg shadow-sm dark:shadow-gray-800"
          src={productInfo.img}
        ></img>
      </div>

      <div className="cx-info-brief flex flex-col justify-between w-[70%]">
        <div className="flex justify-center mt-2 items-center">
          <div className="bg-gray-700 rounded-lg text-white text-center flex items-center p-1 w-full justify-center">
            <span className="text-lg">Customer Sentiment</span>
            <StyledArrowRightAltIcon fontSize="large"></StyledArrowRightAltIcon>
            <span className="text-5xl">{productInfo.sentimoji}</span>
          </div>
        </div>

        <fieldset className="px-3 border rounded-lg shadow-sm dark:shadow-gray-800 bg-slate-200">
          <legend className="float-none w-auto px-3 text-center text-lg bg-gray-700 text-white rounded-lg pb-1">
            Brief Summary ✨
          </legend>
          <p>{productInfo.brief}</p>
        </fieldset>
      </div>

      <div className="updated-delete flex flex-col items-center">
        <p className="text-xs text-center text-gray-400">
          Last Updated {productInfo.lastUpdated}
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
