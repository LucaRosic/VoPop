import { REFRESH_TOKEN, USERNAME } from "../constants";
import PersonIcon from "@mui/icons-material/Person";
import LogoutIcon from '@mui/icons-material/Logout';
import AddProductBtn from "./AddProductBtn";
import api from "../api";
import { AxiosError } from "axios";

interface Props {
  urlScraperCallback : (url: string, secondaryUrl: string) => void;
}

const NavbarTop = ({ urlScraperCallback }: Props) => {
  /*
    Navbar top component. This is to have the vopop logo, add product button, user logged in information,
    and lastly the logout option.
  */

  // Logout function -> Send logout request to the API endpoint and remove local storage
  // TODO: put this functionality in a generic function?
  const logout = async () => {
    console.log("Logging out");
    try {
      await api.post("/api/logout/", {refresh_token: localStorage.getItem(REFRESH_TOKEN)});
      localStorage.clear();
      console.log("Cleared storage!");
      window.location.href = "/login";
    } catch (error) {
      console.log(error);
      const errorResponse = error as AxiosError;
      console.log("LOGOUT ERROR RESPONSE:");
      console.log(errorResponse.response); 
      if (errorResponse.response) {
        localStorage.clear()
        window.location.href = "/login";
      } 
    }
  }


  return (
    <nav className="bg-[rgba(19,58,63)] text-white h-14 flex justify-between items-center px-4 sticky top-0 z-50 border-b-4 border-x-0 border-gray-900">  
      <div className="flex gap-4 items-center">
        {/* <span className="text-2xl">{title}</span> */}
        <img src="/images/vopop_logo.png" className="h-8 pb-1" />
        <AddProductBtn urlScraperCallback={urlScraperCallback}/>
      </div>

      <div className="flex gap-3 items-center px-2 py-1">
        <div>{localStorage.getItem(USERNAME)?.toUpperCase() || "Hugh Mungus"}</div>
        <div className="bg-slate-400 rounded-full p-1">
          <PersonIcon></PersonIcon>
        </div>
        <div className="hover:bg-green-800 p-1 px-2" onClick={logout}><LogoutIcon /></div>
      </div>
    </nav>
  );
};

export default NavbarTop;
