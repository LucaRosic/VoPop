import axios from "axios"
import { useState } from "react"
import api from "../api"
import ProtectedRoute from "../components/ProtectedRoute"

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
    console.log("Testing Django")
    try {
      const res = await api.get("/api/user/product/home/");
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
      <ProtectedRoute>
        <button 
        onClick={getProduct}
        className="bg-gray-600 rounded-lg p-2 text-white"
      >/api/user/product/home</button>
      </ProtectedRoute>
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