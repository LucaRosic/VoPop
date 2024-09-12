import DummyData from "../../DummyData";

//--------------
// MUI ui stuff:
import ArrowForwardIcon from "@mui/icons-material/ArrowForward";
import DeleteIcon from "@mui/icons-material/Delete";
import { styled } from "@mui/material/styles";
//--------------

interface Props {
  productId: number;
  onClick?: () => void;
}

// Look into MUI typography for better text

export const ProductCard_dummy = ({
  productId,
  onClick = () => null,
}: Props) => {
  const productInfo = DummyData(productId);

  // Style arrow icon
  const StyledArrowForwardIcon = styled(ArrowForwardIcon)(() => ({
    fontSize: "2rem", // Adjust the size as needed
    // Add other custom styles here
  }));

  /*
    TODO:
      - Get rid of the rounded beta corners
      - Add a dark black border
      - Add a shadow (rectangle the same)
  */

  return (
    <div
      className="product-card bg-slate-100 w-[60vw] h-60 px-8 pr-2 py-4 flex gap-4 border-2 
      border-gray-400 select-none transform hover:scale-[1.02] hover:shadow-[10px_10px_0px_-5px_rgba(35,106,114)] transition-all shadow-[10px_10px_0px_0px_rgba(35,106,114)]"
      onClick={onClick}
    >
      {/* Shadow for the product card */}

      <div className="product-snippet flex flex-col w-[20vw] h-[100%] bg-gray-900 text-white">
        <h1 className="text-xl text-center">{productInfo.title}</h1>
        <img
          className="w-[100%] h-[80%] object-cover border-2 border-gray-900"
          src={productInfo.img}
        ></img>
      </div>

      <div className="cx-info-brief flex flex-col justify-between w-[70%]">
        <div className="flex justify-center items-center">
          <div className="bg-gray-900 text-white text-center flex items-center p-1 w-full justify-center">
            <span className="text-lg">Customer Sentiment </span>
            <StyledArrowForwardIcon fontSize="large"></StyledArrowForwardIcon>
            <span className="text-5xl mb-1">{productInfo.sentimoji}</span>
          </div>
        </div>

        <fieldset className="px-2 border-2 border-gray-900 border-solid bg-slate-200">
          <legend className="float-none w-auto px-3 text-center text-lg bg-gray-900 text-white">
            Brief Summary ✨
          </legend>
          <p className="text-sm font-medium">{productInfo.brief}</p>
        </fieldset>
      </div>

      <div className="updated-delete flex flex-col justify-between items-center">
        <p className="text-xs text-center text-gray-400">
          Last Updated {productInfo.lastUpdated}
        </p>
        <div
          className="bg-red-600 border-2 hover:bg-red-800 border-red-800 p-2"
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
