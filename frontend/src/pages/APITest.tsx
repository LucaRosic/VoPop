import axios from "axios"
import { useState } from "react"

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
  return (
    <div>
      <button onClick={getQuote}>Get Quote</button>
      <p>{quote}</p>
    </div>
  )
}

export default APITest