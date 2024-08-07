import { useState } from "react";
import AddIcon from '@mui/icons-material/Add';

const AddProductBtn = () => {
  const [url, setUrl] = useState<string>("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault(); // Prevent page from reloading
    console.log(`URL Sent: ${url}`);
  }

  const urlForm = () => {
    return (
      <div className="bg-slate-300 rounded-lg absolute max-h-[40vh] top-[3.2rem] w-[400px] p-2 text-black">
        Enter URL of Product:
        <form onSubmit={handleSubmit}>
          <input 
          className="form-input"
          type="text"
          value={url}
          onChange={(e) => {setUrl(e.target.value)}}
          placeholder="URL"
        />
        <button className="form-button" type="submit">Send</button>
        </form>
      </div>
    )
  }

  const [showForm, setShowForm] = useState<boolean>(false);
  const toggleState = () => {setShowForm(!showForm)};

  return(
    <div className="flex flex-col">
      <div 
        className="bg-green-700 hover:bg-green-800 p-1 rounded-sm cursor-pointer absolute top-[0.4rem] w-40 text-center select-none"
        onClick={toggleState}
      >
      <span><AddIcon /></span>  Add Product
      </div>
      {showForm && urlForm()}
    </div>
    
  ) 
};

export default AddProductBtn;
