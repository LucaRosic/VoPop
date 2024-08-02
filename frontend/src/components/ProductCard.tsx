import "./css/product-card.css";
import DummyData from "../DummyData";

interface Props {
  productId: number;
  onClick?: () => void;
}

export const ProductCard = ({ productId, onClick = () => null }: Props) => {
  const productInfo = DummyData(productId);

  return (
    // <div className="product-card-container" onClick={onClick}>
    //   <h1>{productTitle}</h1>
    //   <img className="product-image" src={productImg}></img>
    // </div>

    <div
      className="product-card bg-slate-100 w-4/5 rounded-lg px-8 py-4 flex shadow-sm dark:shadow-gray-800 gap-4"
      onClick={onClick}
    >
      <div className="product-snippet flex flex-col w-64">
        <h1 className="w-64 text-xl text-center">{productInfo.title}</h1>
        <img
          className="w-64 h-48 object-cover rounded-lg shadow-sm dark:shadow-gray-800"
          src={productInfo.img}
        ></img>
      </div>

      <div className="cx-info-brief flex flex-col w-3/5">
        <p>Test</p>
        <fieldset className="px-3 border rounded-lg shadow-sm dark:shadow-gray-800">
          <legend className="float-none w-auto px-3 text-center text-xl bg-black text-white rounded-lg">Brief Summary ✨</legend>
          <p>{productInfo.brief}</p>
        </fieldset>
        

        
        
      </div>

      <div className="updated-delete"></div>
    </div>
  );
};

/*
- A div for the card
- There is product title
- There is product image


*/
