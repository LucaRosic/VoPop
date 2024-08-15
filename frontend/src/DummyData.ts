const product1 = {
  id: 0,
  title: "Dummy Product 1",
  img: "/images/phone_charger_test_img.png",
  sentimoji: "😎",
  brief: "Reviewers praised the phone charger for its fast charging speed and durable build, but some complained of overheating issues and lack of included charging cable.",
  lastUpdated: "?/?/?",
};
const product2 = {
  id: 1,
  title: "Dummy Product 2",
  img: "/images/dummy_watch.png",
  sentimoji: "😁",
  brief: "Reviewers praised the watch's sleek design and long battery life, but some complained of poor screen visibility outdoors and unreliable heart rate tracking.",
  lastUpdated: "?/?/?",
};
const product3 = {
  id: 2,
  title: "Dummy Product 3",
  img: "/images/dummy_book.png",
  sentimoji: "😒",
  brief: "Readers praised 1984 as a chillingly prophetic exploration of totalitarianism, but some found the bleak ending and dense prose to be overwhelming.",
  lastUpdated: "?/?/?",
};
const product4 = {
  id: 3,
  title: "Dummy Product 4",
  img: "/images/dummy_keyboard.png",
  sentimoji: "🙂",
  brief: "Reviewers raved about the keyboard's build quality, but some complained of the loud clicky noises.",
  lastUpdated: "?/?/?",
};


const productsList = [product1, product2, product3, product4];

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
