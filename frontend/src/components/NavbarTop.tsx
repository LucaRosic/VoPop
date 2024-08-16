import { USERNAME } from "../constants";
import PersonIcon from "@mui/icons-material/Person";
import AddProductBtn from "./AddProductBtn";

interface Props {
  title: string;
}

const NavbarTop = ({ title }: Props) => {
  return (
    // <nav className="flex bg-gradient-to-r from-slate-700 to-slate-900 text-white h-12 justify-between items-center px-4 sticky top-0 z-50 border-b-2 border-slate-400">
    <nav className="bg-[rgba(19,58,63)] text-white h-14 flex justify-between items-center px-4 sticky top-0 z-50 border-b-4 border-x-0 border-gray-900">  
      <div className="flex gap-8 items-center">
        <span className="text-2xl">{title}</span>
        <AddProductBtn />
      </div>

      <div className="flex gap-3 items-center hover:bg-slate-700 px-2 py-1">
        <div>{localStorage.getItem(USERNAME) || "Hugh Mungus"}</div>
        <div className="bg-slate-400 rounded-full p-1">
          <PersonIcon></PersonIcon>
        </div>
      </div>
    </nav>
  );
};

export default NavbarTop;
