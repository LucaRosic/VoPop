import { useNavigate } from "react-router-dom";
import { ProductCard } from "../components/ProductCard";
import NavbarTop from "../components/NavbarTop";

export const ProductDashboard = () => {
  const navigate = useNavigate();

  const navFunc = (prodId : number) => {
    navigate('/product-info', { state: { prodId: prodId, meaning : 'test' } }); 
  }

  const productsList = [0,1,2];
  return (
    <>
      {/* <h1 className="text-center">Product Dashboard</h1> */}
      <NavbarTop title="Product Dashboard"/>
      <div className="flex flex-col items-center gap-4 px-32">
        {productsList.map((product) => (
          <ProductCard
            key={product}
            productId={product}
            onClick={() => navFunc(product)}
          />
        ))}
      </div>
      <p>
        <a href="/home">Back Home</a>
      </p>
    </>
  );
};
