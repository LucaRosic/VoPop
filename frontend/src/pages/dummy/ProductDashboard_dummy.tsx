import { useNavigate } from "react-router-dom";
import NavbarTop from "../../components/NavbarTop";
import Footer from "../../components/Footer";
import { ProductCard_dummy } from "../../components/dummy/ProductCard_dummy";

export const ProductDashboard_dummy = () => {
  /*
    Create a dummy product dashboard page using dummy data. This page is to work
    without needing any connection established with backend server
  */

  const navigate = useNavigate();

  const navFunc = (prodId : number) => {
    navigate('/product-info-dummy', { state: { prodId: prodId, meaning : 'test' } }); 
  }

  const productsList = [0,1,2,3];

  return (
    <>
      <NavbarTop title="VoPop" urlScraperCallback={(arg:string) => (console.log(arg))}/>
      <div className="flex flex-col gap-8 bg-[#FBF5F3]">
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
