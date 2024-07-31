import { useNavigate } from "react-router-dom";
import { ProductCard } from "../components/ProductCard";

export const ProductDashboard = () => {
  const product1 = {
    id: 0,
    title: "Phone Charger",
    img: "/images/phone_charger_test_img.png",
  };
  const product2 = {
    id: 1,
    title: "Fart Test",
    img: "/images/whoopee_cushion_test.png",
  };
  const product3 = {
    id: 2,
    title: "Tooty",
    img: "/images/whoopee_cushion_test.png",
  };
  const product4 = {
    id: 3,
    title: "Diffy Shock",
    img: "/images/phone_charger_test_img.png",
  };

  const productsList = [product1, product2, product3, product4];

  const navigate = useNavigate();

  const navFunc = (prodId : number) => {
    navigate('/product-info', { state: { product: productsList[prodId], meaning : 'test' } }); 
  }

  return (
    <>
      <h1>ProductDashboard</h1>
      <div className="dashboard-container">
        {productsList.map((product) => (
          <ProductCard
            key={product.title}
            productTitle={product.title}
            productImg={product.img}
            productId={product.id}
            onClick={() => navFunc(product.id)}
          />
        ))}
      </div>
      <p>
        <a href="/home">Back Home</a>
      </p>
    </>
  );
};
