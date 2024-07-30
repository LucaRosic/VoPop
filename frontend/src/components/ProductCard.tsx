import "./css/product-card.css";

interface Props {
  productTitle: string;
  productImg: string;
  productId: number;
  onClick?: () => void;
}

export const ProductCard = ({
  productTitle,
  productImg,
  productId,
  onClick = () => null,
}: Props) => {
  return (
    <div className="product-card-container" onClick={onClick}>
      <h1>{productTitle}</h1>
      <img className="product-image" src={productImg}></img>
    </div>
  );
};

/*
- A div for the card
- There is product title
- There is product image


*/
