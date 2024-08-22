import "./css/product-card.css";
//--------------
// MUI ui stuff:
import ArrowForwardIcon from "@mui/icons-material/ArrowForward";
import DeleteIcon from "@mui/icons-material/Delete";
import { styled } from "@mui/material/styles";
//--------------

interface Props {
  productId?: number;
  productTitle: string;
  productImg: string;
  productOverview: string;
  lastUpdated: string;
  sentimentScore: number;
  onClick?: () => void;
}

// Look into MUI typography for better text

export const ProductCard = ({ productTitle, productImg, productOverview, lastUpdated, sentimentScore, onClick = () => null }: Props) => {

  // Style arrow icon
  const StyledArrowForwardIcon = styled(ArrowForwardIcon)(() => ({
    fontSize: "2rem", // Adjust the size as needed
    // Add other custom styles here
  }));

  const convertSentimentscoreToEmoji = (score : number) => {
    /*
      - <= 0.75 ( *vomit* )
      - <= 0.8 ( :c )
      - <= 0.85 ( :/ )
      - <= 0.9 ( :) )
      - <= 0.95 ( *sunglasses* )
    */

    let emoji = "🤷"
    if (score <= 0.75) {
      emoji = "🤮";
    } else if (score <= 0.8) {
      emoji = "😒";
    } else if (score <= 0.85) {
      emoji = "😐";
    } else if (score <= 0.9) {
      emoji = "😊";
    } else if (score <= 0.95) {
      emoji = "😎";
    }

    return emoji;

  }

  const convertDate = (date : string) => {
    // Function to convert yyyy-mm-dd to dd/mm/yy like a normal person

    const dateSplit = date.split("-");
    const convertedDate = `${dateSplit[2]}/${dateSplit[1]}/${dateSplit[0].slice(2,4)}`
    return convertedDate;
  }

 
  return (
    <div
      className="product-card bg-slate-100 w-[60vw] h-60 px-8 pr-2 py-4 flex gap-4 border-2 
      border-gray-400 select-none transform hover:scale-[1.02] hover:shadow-[10px_10px_0px_-5px_rgba(35,106,114)] transition-all shadow-[10px_10px_0px_0px_rgba(35,106,114)]"
      onClick={onClick}
    >
      {/* Shadow for the product card */}

      {/* Product title and image */}
      <div className="product-snippet flex flex-col w-[30%] h-[100%] bg-gray-900 text-white">
        <h1 className="text-xl text-center">{productTitle}</h1>
        <img
          className="w-[100%] h-[80%] object-cover border-2 border-gray-900"
          src={productImg}
        ></img>
      </div>

      {/* Product sentiment emoji and brief summary */}
      <div className="cx-info-brief flex flex-col justify-between w-[70%]">
        <div className="flex justify-center items-center">
          <div className="bg-gray-900 text-white text-center flex items-center p-1 w-full justify-center">
            <span className="text-lg">Customer Sentiment </span>
            <StyledArrowForwardIcon fontSize="large"></StyledArrowForwardIcon>
            <span className="text-5xl mb-1">{convertSentimentscoreToEmoji(sentimentScore)}</span>
          </div>
        </div>

        <fieldset className="px-2 border-2 border-gray-900 border-solid bg-slate-200">
          <legend className="float-none w-auto px-3 text-center text-lg bg-gray-900 text-white">
            Brief Summary ✨
          </legend>
          <p className="text-sm font-medium">{productOverview}</p>
        </fieldset>
      </div>

      <div className="updated-delete flex flex-col justify-between items-center">
        <p className="text-xs text-center text-gray-400">
          Last Updated <br></br> {convertDate(lastUpdated)}
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

