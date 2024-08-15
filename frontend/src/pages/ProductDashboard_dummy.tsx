import { useNavigate } from "react-router-dom";
import { ProductCard } from "../components/ProductCard";
import NavbarTop from "../components/NavbarTop";
import Footer from "../components/Footer";

export const ProductDashboard = () => {
  const navigate = useNavigate();

  const navFunc = (prodId : number) => {
    navigate('/product-info', { state: { prodId: prodId, meaning : 'test' } }); 
  }

  const productsList = [0,1,2,3];

  return (
    <>
      <NavbarTop title="Product Dashboard"/>
      <div 
        className="flex flex-col items-center gap-4 px-32 pt-4"
      >
        {productsList.map((product) => (
          <ProductCard
            key={product}
            productId={product}
            onClick={() => navFunc(product)}
          />
        ))}
      </div>
      <Footer />
    </>
  );
};
