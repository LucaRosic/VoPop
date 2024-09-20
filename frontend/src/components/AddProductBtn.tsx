import { useEffect, useRef, useState } from "react";
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
    setShowForm(false); // Close the form box
  }


  const popupBoxRef = useRef<HTMLDivElement>(null);

  const urlForm = () => {
    return (
      <div className="border-2 border-gray-700 border-solid absolute top-[3.2rem] w-[400px] 
        py-4 p-2 bg-gray-900 text-white shadow-[10px_10px_0px_0px_rgba(35,106,114,90%)]
        hover:scale-[1.02] hover:shadow-[10px_10px_0px_-5px_rgba(35,106,114,90%)] transition-all">
        <form onSubmit={handleSubmit} className="flex flex-col gap-3 items-center justify-around">
          {/* Primary url */}
          <input 
          className="bg-slate-100 w-[350px] h-[40px] px-2 border-2 border-slate-100 border-solid text-black placeholder-gray-900 placeholder:italic"
          type="text"
          value={url}
          onChange={(e) => {setUrl(e.target.value)}}
          placeholder="Enter URL of Product:"
        />
          {/* Secondary url */}
           <input 
          className="bg-slate-100 w-[350px] h-[40px] px-2 border-2 border-slate-200 border-solid text-black placeholder-gray-900 placeholder:italic"
          type="text"
          value={secondaryUrl}
          onChange={(e) => {setSecondaryUrl(e.target.value)}}
          placeholder="Add Additional URL:"
          />
        <button className="w-[200px] h-[40px] bg-[rgba(35,106,114)] font-bold text-lg" type="submit">ADD</button>
        </form>
      </div>
    )
  }

  const [showForm, setShowForm] = useState<boolean>(false);
  const toggleState = () => {setShowForm(!showForm)};

  
  

  // Handle clicking outside of popupbox
  const handleClick = (event: MouseEvent) => {
    if (popupBoxRef.current && !popupBoxRef.current.contains(event.target as HTMLElement)) {
      setShowForm(false); // Close the popupbox
    }
  }

  useEffect(() => {
    window.addEventListener('click', handleClick);

    return () => {
      window.removeEventListener('click', handleClick);
    }
  }, [])

  return(
    <div ref={popupBoxRef} className="flex flex-col">
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
