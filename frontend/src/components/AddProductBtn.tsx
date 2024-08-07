import { useState } from "react";

const AddProductBtn = () => {
  const [url, setUrl] = useState<string>("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault(); // Prevent page from reloading
    console.log(`URL Sent: ${url}`);
  }

  const urlForm = () => {
    return (
      <div className="bg-slate-300 rounded-lg absolute max-h-[40vh] top-[3.2rem] w-[400px] p-2 text-black">
        Dropdown Box
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
        className="bg-green-800 p-2 rounded-sm cursor-pointer absolute top-1 w-28"
        onClick={toggleState}
      >
      Add Product
      </div>
      {showForm && urlForm()}
    </div>
    
  ) 
};

export default AddProductBtn;
