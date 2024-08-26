import { REFRESH_TOKEN, USERNAME } from "../constants";
import PersonIcon from "@mui/icons-material/Person";
import LogoutIcon from '@mui/icons-material/Logout';
import AddProductBtn from "./AddProductBtn";
import api from "../api";
import { AxiosError } from "axios";

interface Props {
  title: string;
  urlScraperCallback : (url: string) => void;
}

const NavbarTop = ({ title, urlScraperCallback }: Props) => {

 const logout = async () => {
    console.log("Logging out");
    try {
      await api.post("/api/logout/", {refresh_token: localStorage.getItem(REFRESH_TOKEN)});
      localStorage.clear();
      console.log("Cleared storage!");
      window.location.href = "/login";
    } catch (error : any) {
      console.log(error);
      console.log("ERROR RESPONSE:");
      const errorResponse = error as AxiosError;
      console.log(errorResponse.response);
    }
  }


  return (
    // <nav className="flex bg-gradient-to-r from-slate-700 to-slate-900 text-white h-12 justify-between items-center px-4 sticky top-0 z-50 border-b-2 border-slate-400">
    <nav className="bg-[rgba(19,58,63)] text-white h-14 flex justify-between items-center px-4 sticky top-0 z-50 border-b-4 border-x-0 border-gray-900">  
      <div className="flex gap-8 items-center">
        <span className="text-2xl">{title}</span>
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
