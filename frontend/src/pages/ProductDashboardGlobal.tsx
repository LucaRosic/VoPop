import { useNavigate } from "react-router-dom";
import { ProductCard } from "../components/ProductCard";
import NavbarTop from "../components/NavbarTop";
import Footer from "../components/Footer";
import { useContext, useEffect, useState } from "react";
import api from "../api";
import ProductCardLoading from "../components/ProductCardLoading";
import ConfirmBox from "../components/ConfirmBox";
import { Context } from "../app-context/Store";

export const ProductDashboardGlobal = () => {
  /*
    Page to render the products the user is currently tracking.
  */
  const navigate = useNavigate();

  const navFunc = (prodId : number) => {
    navigate('/product-info', { state: { prodId: prodId} }); 
  }

  const [loading, setLoading] = useState<boolean>(false);

  // Get products the user is currently tracking
  const getProductInfo = async () => {
    setLoading(true);
    try {
      const res = await api.get("/api/product/home/");
      console.log(res.data); // REMOVE
      console.log(`Type of data: ${typeof res.data}`);
      return res.data // Filled object
    } catch (error) {
      console.log(error);
      return Promise.reject(error); // Empty object
    } finally {
      setLoading(false);
    }
  }

  // const [cardState, setCardState] = useContext(Context);
  // const {cardState, updateCardState} = useContext(Context);
  const {cards, waitingNum, updateCardState} = useContext(Context);
  console.log(`Card state: ${JSON.stringify(cards)}`)
 

  const [productData, setProductData] = useState<any[]>([]);
  // On page load get the list of products user is tracking and update the information
  useEffect(() => { 
    console.log(`Waiting Num: ${waitingNum}`)
    getProductInfo()
      .then((res) => {
        let productDataList:any[] = []; // Change this any to a defined product card object in future
        res.map((productInfo : any) => productDataList.push(productInfo))
        let newCardState = {cards: productDataList}
        updateCardState(newCardState)
        // setProductData(cardState.cards);
      }).catch((error) => {
        console.log(error)
        setProductData([]);
      })
  }, [])

  useEffect(() => {
    console.log("CARD STATE UPDATE DETECTED")
  }, [cards])

  // Function to cut of a string at a specific length (for rendering ... at long strings)
  const stringLimiter = (inString : string, sliceLength : number) => {
    if (inString.length > sliceLength) {
      return `${inString.slice(0,sliceLength)}...` // Slice up the string
    } else {
      return inString; // No need to slice up the string
    }

  }

  // Count number of cards currently loading
  const [waitingCardNumber, setWaitingCardNumber] = useState<number>(0); 
  // Set local storage waiting card number
  useEffect(() => {
    // Add event listener to clear sessionStorage when window refreshed:
    // window.addEventListener('beforeunload', () => {
    //   sessionStorage.clear();
    // })

    // Get waiting card number from previous session
    if (sessionStorage.getItem("WAITING_NUMBER") === null) {
      sessionStorage.setItem("WAITING_NUMBER", JSON.stringify(0))
    } else {
      const waitingNum = Number(sessionStorage.getItem("WAITING_NUMBER"))
      setWaitingCardNumber(waitingNum);
      console.log(`GETTING WAITING NUM: ${waitingNum}`)
    }

  },[])


  // TODO:
  // Redux is the way to go

  const addProductCard = async ( scrapeUrl : string, scrapeSecondaryUrl: string ) => {
   
    // Increment number of waiting cards to be processed
    let waitingNum = Number(sessionStorage.getItem("WAITING_NUMBER"))+1
    sessionStorage.setItem("WAITING_NUMBER", JSON.stringify(waitingNum));
    updateCardState({waitingNum: 69});
    console.log(`JUST SET WAITING NUM TO ${waitingNum}`);
    setWaitingCardNumber(waitingCardNumber + 1);
    // Call the URL scraper API
    try {
      const urlData = {url:[scrapeUrl, scrapeSecondaryUrl]};
      console.log("Sending scraping api");
      console.log(`Scraping: ${scrapeUrl} & ${scrapeSecondaryUrl}`)
      const res = await api.post("/api/product/",urlData);
      console.log(res.data);

      if (res.data[0] !== undefined) {
        let newCards = {cards: [res.data[0], ...cards]};
        updateCardState(newCards);
        // setProductData((productData : any) => [res.data[0], ...productData]);
        console.log("Added product information.");
        console.log(`New product ${JSON.stringify(cards)}`)
      }
    } catch (error) {
      console.log(error);
    } finally {
      // Decrement waitng card number -> the card has been processed
      setWaitingCardNumber(waitingCardNumber => Math.max(waitingCardNumber - 1,0)); // Clamp value to 0
      waitingNum -= 1; // Decrement the count again
      sessionStorage.setItem("WAITING_NUMBER", JSON.stringify(waitingNum))
      console.log("URL request has finished processing!");
      console.log(`User location: ${window.location.pathname}`)
      if (window.location.pathname === "/dashboard") {
        // window.location.reload();
      }
      
      
    }
  }

  const [dialogOpen, setDialogOpen] = useState<boolean>(false);
  const [deleteProdId, setDeleteProdId] = useState<number|null>(null);

  const confirmDeleteCardCallback = async (prodId:number|null) => {
    const oldProductData = productData; // Save old product data
    setProductData(prev => prev.filter(element => element["product"]["id"] !== prodId )); // Optimistic deletion
    setDeleteProdId(null);
    setDialogOpen(false);
    try {
      const res = await api.delete(`/api/product/delete/${prodId}/`);
      console.log(res.data); // REMOVE
      console.log("Success for delete request!");
    } catch (error) {
      setProductData(oldProductData) // Revert changes
      console.log(error)
    }
    
  }

  // Delete card callback function
  const deleteCard = (prodId:number|null) => {
    console.log(`Sending delete request for product id: ${prodId}`);
    setDeleteProdId(prodId);
    setDialogOpen(true);
  }

  // Render the product card based on information given by backend
  const renderProductCards = () => {
    if (loading === true) {
      return <h3>Page Loading...</h3>
    } else {
      console.log(productData);
      console.log(cards)
      console.log(`Type test 2: ${typeof productData}`)
      try{
          return (
            // productData.map((productInfo : any) => {
              cards.map((productInfo:any) => {
              return(
                <ProductCard
                  key={productInfo["product"]["id"]}
                  productId={productInfo["product"]["id"]}
                  productTitle={stringLimiter(productInfo["product"]["name"], 20)}
                  productImg={productInfo["product"]["image"]}
                  productOverview={stringLimiter(productInfo["overview"], 200)}
                  lastUpdated={productInfo["date"]}
                  sentimentScore={productInfo["avg_sentiment"]}
                  positiveCount={productInfo["positive_count"]}
                  negativeCount={productInfo["negative_count"]}
                  deleteCallback={deleteCard}
                  onClick={() => navFunc(productInfo["product"]["id"])}
                /> 
              )
          })
        )
      } catch (error) {
        console.log(error);
        return (
          <>
            <h3>Error Getting Product Info</h3>
            <a href=".">Retry</a>
          </>
          
        )
      }
      
    }
  }

  // Render the loading cards (cards with loading icons)
  const renderLoadingCards = (numCards : number) => {
    if (loading === true) {
      return <h3>Page Loading...</h3>
    }
    else {
      // Function to render numCards loading product cards
      console.log(`Number loading: ${numCards}`)
      return [...Array(numCards).keys()].map((key) => {
        return (<ProductCardLoading key={key} />)
      })
    }
    
  }
  

  return (
    <div className="flex flex-col min-h-[100vh]">
      <NavbarTop urlScraperCallback={addProductCard}/>
      <div className="flex-grow flex flex-col gap-8 bg-[#FBF5F3]">
        <div 
          className="flex-grow flex flex-col items-center gap-4 px-32 pt-4"
        >
          {/* Render loading card components */}
          {renderLoadingCards(waitingCardNumber)}

          {/* Render the product cards */}
          {renderProductCards()}
        </div>
        <ConfirmBox
          open={dialogOpen}
          handleClose={() => setDialogOpen(false)}
          productId={deleteProdId}
          confirmDeleteCallback={confirmDeleteCardCallback}
        />
        <Footer />
      </div>
    </div>
  );
};
