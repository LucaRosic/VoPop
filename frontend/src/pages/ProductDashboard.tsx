import { ProductCard } from "../components/ProductCard";

export const ProductDashboard = () => {
  const product1 = {
    title: "Phone Charger",
    img: "/images/phone_charger_test_img.png",
  };
  const product2 = {
    title: "Fart Test",
    img: "/images/whoopee_cushion_test.png",
  };
  const product3 = { title: "Tooty", img: "/images/whoopee_cushion_test.png" };
  const product4 = {
    title: "Diffy Shock",
    img: "/images/phone_charger_test_img.png",
  };

  const productsList = [product1, product2, product3, product4];

  return (
    <>
      <h1>ProductDashboard</h1>
      <div className="dashboard-container">
        {productsList.map((product) => (
          <ProductCard
            key={product.title}
            productTitle={product.title}
            productImg={product.img}
            onClick={() => console.log(product.title)}
          />
        ))}
      </div>
      <p>
        <a href="/home">Back Home</a>
      </p>
    </>
  );
};
