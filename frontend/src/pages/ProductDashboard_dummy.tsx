import { useNavigate } from "react-router-dom";
import NavbarTop from "../components/NavbarTop";
import Footer from "../components/Footer";
import { ProductCard_dummy } from "../components/ProductCard_dummy";

export const ProductDashboard_dummy = () => {
  const navigate = useNavigate();

  const navFunc = (prodId : number) => {
    navigate('/product-info-dummy', { state: { prodId: prodId, meaning : 'test' } }); 
  }

  const productsList = [0,1,2,3];

  return (
    <>
      <NavbarTop title="VoPop"/>
      <div className="flex flex-col gap-8 bg-[rgba(255,241,201)]">
        <div 
          className="flex flex-col items-center gap-4 px-32 pt-4"
        >
          {productsList.map((product) => (
            <ProductCard_dummy
              key={product}
              productId={product}
              onClick={() => navFunc(product)}
            />
          ))}
        </div>
        <Footer />
      </div>
    </>
  );
};
