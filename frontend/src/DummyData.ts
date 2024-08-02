const product1 = {
  id: 0,
  title: "Dummy Product 1",
  img: "/images/phone_charger_test_img.png",
  sentimoji: "😎",
  brief: "The Dummy Charger delivers lightning-fast charging speeds without overheating for a stress-free battery boost.",
};
const product2 = {
  id: 1,
  title: "Dummy Product 2",
  img: "/images/dummy_watch.png",
  sentimoji: "😁",
  brief: "The Dummy Watch boasts a sleek design, advanced features, and unparalleled comfort for the modern, on-the-go lifestyle.",
};
const product3 = {
  id: 2,
  title: "Dummy Product 3",
  img: "/images/dummy_book.png",
  sentimoji: "😒",
  brief: "Immerse yourself in the captivating world of '1984,' a thrilling sci-fi adventure that will leave you breathless.",
};


const productsList = [product1, product2, product3];

const DummyData = (productId: number) => {
  // This function is to take in a product id and return JSON object for dummy info
  /*
    Information required:
        - Product title
        - Product image
        - Simple sentiment information (emoji)
        - Brief overview
        - Last updated date (for now just keep it ?/?/?)
  */
  return productsList[productId];
};

export default DummyData;
