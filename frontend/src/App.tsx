import { Routes, Route } from "react-router-dom";
import { Link } from "react-router-dom";
// Pages --------------------
import { Home } from "./pages/Home";
import { ProductDashboard } from "./pages/ProductDashboard";
import { TempStatePage } from "./pages/TempStatePage";
import { TempStatePage2 } from "./pages/TempStatePage2";
import { TempGetStatePage } from "./pages/TempGetStatePage";
// --------------------------

const App = () => {
  return (
    <>
      {/* Create navbar here */}
      <nav>
        <ul>
          <li>
            <Link to="/home">Home</Link>
          </li>
          <li>
            <Link to="/dashboard">Dashboard</Link>
          </li>
          <li>
            <Link to="/state">State</Link>
          </li>
        </ul>
      </nav>
      {/* Only things inside routes component changes ^ Nav bar above is bing chilling */}
      <Routes>
        <Route index element={<Home />} />
        <Route path="/home" element={<Home />} />
        <Route path="/dashboard" element={<ProductDashboard />} />
        <Route path="/state">
          <Route index element={<TempStatePage />}/>
          <Route path=":id" element={<TempStatePage />}/>
          {/* This is another way to share state -> useNavigate and useLocation */}
          <Route path="X" element={<TempStatePage2 />}/>
          <Route path="get-state" element={<TempGetStatePage />}/>
          {/* ------------------------ */}
        </Route>
        <Route path="*" element={<p>OH NOES THIS NOT EXIST DUMBASS</p>} />
      </Routes>
    </>
  );
};

export default App;
