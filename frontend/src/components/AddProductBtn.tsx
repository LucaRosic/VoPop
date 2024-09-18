import { useState } from "react";
import AddIcon from '@mui/icons-material/Add';

interface Props {
  urlScraperCallback : (url: string, secondaryUrl: string) => void;
}

const AddProductBtn = ( {urlScraperCallback} : Props ) => {
  /*
    React Component for the add product button. When button pressed, a box is 
    opened allowing user to enter in a url
  */
  const [url, setUrl] = useState<string>("");
  const [secondaryUrl, setSecondaryUrl] = useState<string>("")

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault(); // Prevent page from reloading
    console.log(`Secondary URL Sent: ${secondaryUrl}`)
    urlScraperCallback(url, secondaryUrl); // Send the url
    setUrl(""); // Clear url field
    setSecondaryUrl(""); // Clear secondary field 
  }

  const urlForm = () => {
    return (
      <div className="bg-slate-300 rounded-lg absolute max-h-[40vh] top-[3.2rem] w-[400px] p-2 text-black">
        <form onSubmit={handleSubmit} className="text-center">
          {/* Primary url */}
          <input 
          className="form-input w-[350px]"
          type="text"
          value={url}
          onChange={(e) => {setUrl(e.target.value)}}
          placeholder="Enter URL of Product:"
        />
          {/* Secondary url */}
           <input 
          className="form-input w-[350px]"
          type="text"
          value={secondaryUrl}
          onChange={(e) => {setSecondaryUrl(e.target.value)}}
          placeholder="Add Additional URL:"
          />
        <button className="form-button w-[350px]" type="submit">Add</button>
        </form>
      </div>
    )
  }

  const [showForm, setShowForm] = useState<boolean>(false);
  const toggleState = () => {setShowForm(!showForm)};

  return(
    <div className="flex flex-col">
      <div 
        className="bg-green-700 hover:bg-green-800 p-1 cursor-pointer w-36 text-center select-none"
        onClick={toggleState}
      >
      <span><AddIcon /></span>  Add Product
      </div>
      {showForm && urlForm()}
    </div>
    
  ) 
};

export default AddProductBtn;
