import api from "../api"
import { REFRESH_TOKEN } from "../constants";

/*

  File to test specific api calls with buttons.

*/

const APITest = () => {

  // Logout API call function
  const sendLogout = async () => {
    console.log("Logging out");

    try {
      const res = await api.post("/api/logout/", {refresh_token: localStorage.getItem(REFRESH_TOKEN)});
      localStorage.clear();
      console.log("Cleared storage!");
      console.log(res.status);
    } catch (error) {
      console.log(error);
    }
  }

  // Sentiment data API call function
  const getData = async () => {
    console.log("retrieving data")
    try {
      const res = await api.get('/api/product/dashboard/sentiment/50/');
      const apiData = res.data;
      console.log(apiData);
    } catch (error) {
      console.log(error);
    }
  }

  // Product dashboard API call function
  const getProduct = async () => {
    console.log("Testing Django");
    try {
      const res = await api.get("/api/product/home/");
      console.log(res.data);
    } catch (error) {
      console.log(error);
      console.log("Redirecting to login page");
      window.location.href = "/login"; // Back to login page on failure
    }
  }

  // Web scrape API call function
  const sendUrl = async () => {
    console.log("Sending URL api");
    try {
      const urlData = {url:"https://www.amazon.com.au/Chotto-Motto-Crispy-Chilli-Oil/dp/B0BTM969DV/ref=sr_1_5?sr=8-5"};
      console.log(`Sending url: ${urlData}`);
      const res = await api.post("/api/product/",urlData);
      console.log("DONE!");
      console.log(res.data);
    } catch (error) {
      console.log(error);
    }
  }

  // Clear local storage cache of application
  const clearCache = () => {
    console.log("Cleared the cache!");
    localStorage.clear();
  }

  const delay = (delayInms : number) => {
    return new Promise(resolve => setTimeout(resolve, delayInms));
  };

  
  const worker = new Worker("workerScriptTest.ts");

  const persistantFunction = async () => {
    console.log("Sending persistant request...");
    worker.postMessage("PERSISTENT");
    
  }

  const ping = () => {
    console.log(`Bing Bong Ping Pong! ${localStorage.getItem("TEST")}`);
    worker.postMessage("Poking the worker!");
    localStorage.setItem("TEST", "State 0");
  }

  // Return buttons that call above functions
  return (
    <div className="flex flex-col justify-center items-center p-16">
      <h1 className="mb-20">API Test</h1>
      <button  
      onClick={getProduct}
      className="bg-gray-600 rounded-lg p-2 text-white"
      >
        Send Request for Products
      </button>
      <br></br>

      <br></br>
      <button 
      onClick={sendUrl}
      className="bg-gray-600 rounded-lg p-2 text-white"
      >
        Send URL Test
      </button>
      <br></br>

      <br></br>
      <button 
      onClick={sendLogout}
      className="bg-gray-600 rounded-lg p-2 text-white"
      >
        Logout
      </button>
      <br></br>

      <br></br>
      <button
        onClick={clearCache}
        className="bg-gray-600 rounded-lg p-2 text-white"
      >
        Remove Local Cache
      </button>
      <br></br>
      <button 
      onClick={getData}
      className="bg-gray-600 rounded-lg p-2 text-white"
      >
        Get chart data test
      </button>

      <br></br>
      <button 
      onClick={ping}
      className="bg-gray-600 rounded-lg p-2 text-white"
      >
        Ping
      </button>
      <br></br>

      <br></br>
      <button 
      onClick={persistantFunction}
      className="bg-gray-600 rounded-lg p-2 text-white"
      >
        Persistent
      </button>
      <br></br>

    </div>

  )
}

export default APITest