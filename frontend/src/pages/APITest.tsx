import axios from "axios"
import { useState } from "react"
import api from "../api"
import { data } from "../components/BarGraph"

const APITest = () => {

  const [quote, setQuote] = useState<string>("")

  const getQuote = async () => {
    console.log("Hello!")
    try {
      const res = await axios.get('https://type.fit/api/quotes');
      const apiQuote = res.data[0].text;
      console.log(apiQuote);
      setQuote(apiQuote);
    } catch (error) {
      console.log(error);
    }
  }

  const getProduct = async () => {
    console.log("Testing Django");
    try {
      const res = await api.get("/api/user/product/home/");
      console.log(res.data);
    } catch (error) {
      console.log(error);
    }
  }

  const sendUrl = async () => {
    console.log("Sending URL api");
    try {
      const urlData = {url:"google.com"};
      console.log("Sending api:");
      const res = await api.get("/api/product/",urlData);
      console.log("DONE!");
      console.log(res.data);
    } catch (error) {
      console.log(error);
    }
  }

  const clearCache = () => {
    console.log("Cleared the cache!");
    localStorage.clear();
  }

  return (
    <div>
      <button onClick={getQuote}>Get Quote</button>
      <p>{quote}</p>
      <button 
      onClick={getProduct}
      className="bg-gray-600 rounded-lg p-2 text-white"
      >
        /api/user/product/home
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
        onClick={clearCache}
        className="bg-gray-600 rounded-lg p-2 text-white"
      >
        Remove Local Cache
      </button>
    </div>
  )
}

export default APITest