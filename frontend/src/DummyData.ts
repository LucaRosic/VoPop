/*

  File to simulate dummy data (this is when testing frontend application independent
  of the backend server running)

*/

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

const reviewMarkdown = `
## CyberPowerPC Gamer Xtreme VR Review Summary:
**Likes:**
* **Performance:** Customers consistently praise the performance of the PC, especially for its ability to handle modern games on high settings. 
* **Value:** Many reviewers highlight the competitive price point, particularly when purchased on sale.
* **Ease of Setup:** The PC is widely recognized for its straightforward setup process, even for those new to PC building.
* **Quality Components:** Users appreciate the quality of the included parts, often mentioning specific brands like Asus and MSI.
* **Included Peripherals:** The bundled keyboard and mouse are generally well-received.
* **Quiet Operation:** Many users find the PC to be surprisingly quiet, even under load.
* **RGB Lighting:** The customizable RGB lighting is a popular feature.
* **Fast Shipping:** Several reviewers mention quick shipping times.

**Dislikes:**
* **CPU Cooling:** A common complaint is the inadequacy of the stock CPU cooler, leading to high temperatures and fan noise. Many recommend upgrading to a more robust cooler, like the Peerless Assassin.
* **RAM:** Some users find 16GB of RAM insufficient for their needs and suggest upgrading to 32GB.
* **RGB Control:** Difficulty controlling the RGB lighting is mentioned by a few reviewers.
* **Damaged Packaging:** A couple of customers received PCs with damaged packaging, raising concerns about handling during shipping.
* **Fan Noise:** While many find the PC to be quiet, some experience noticeable fan noise, especially during demanding tasks. 
* **Warning Sticker:** Several users struggle to remove the warning sticker from the tempered glass side panel.

**Overall:**
The CyberPowerPC Gamer Xtreme VR is generally well-received, praised for its performance, ease of setup, and value for money. However, the stock CPU cooler is often criticized, requiring an upgrade for optimal thermal performance and quieter operation.
`

export const GetMarkdownReview = () => {return reviewMarkdown}


export default DummyData;
