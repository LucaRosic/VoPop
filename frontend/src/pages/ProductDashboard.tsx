import { useNavigate } from "react-router-dom";
import { ProductCard } from "../components/ProductCard";
import NavbarTop from "../components/NavbarTop";
import Footer from "../components/Footer";
import { useEffect, useState } from "react";
import api from "../api";

export const ProductDashboard = () => {
  const navigate = useNavigate();

  const navFunc = (prodId : number) => {
    navigate('/product-info', { state: { prodId: prodId, meaning : 'test' } }); 
  }

  const productsList = [0,1,2,3];

  // First do an API request to get product info

  const [loading, setLoading] = useState<boolean>(true);

  const getProductInfo = async () => {
    setLoading(true);
    try {
      const res = await api.get("/api/product/home/");
      return res.data // Filled object
    } catch (error) {
      console.log(error);
      return {}; // Empty object
    } finally {
      setLoading(false);
    }
  }

  // let productData = {}; // Default nothing in product data object
  const [productData, setProductData] = useState<any>({});
  useEffect(() => {
    getProductInfo()
      .then((res) => {setProductData(res)})
  }, [])

  const renderProductCards = () => {
    if (loading === true) {
      return <h3>Page Loading...</h3>
    } else {
      console.log(productData);
      try{
          return (
            productData.map((productInfo : any) => {
              return(
                <ProductCard
                  key={productInfo["product"]["id"]}
                  productTitle={productInfo["product"]["name"].slice(0,20)}
                  productImg={productInfo["product"]["image"]}
                  productId={productInfo["product"]["id"]}
                /> 
              )
          })
        )
      } catch (error) {
        return <h3>Error Getting Product Info</h3>
      }
      
    }
  }

  return (
    <>
      <NavbarTop title="Product Dashboard"/>
      <div 
        className="flex flex-col items-center gap-4 px-32 pt-4"
      >
        {renderProductCards()}
        {/* <ProductCard
          productTitle="Test Product"
          productImg="https://m.media-amazon.com/images/I/71IRptDkCRL._AC_SX679_.jpg"
        /> */}
      </div>
      
      <Footer />
    </>
  );
};
