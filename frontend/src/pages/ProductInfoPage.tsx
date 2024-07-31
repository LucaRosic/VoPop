import { useLocation } from "react-router-dom";

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
    </>
    
  )
}
