import { Routes, Route, Navigate } from "react-router-dom";
// import { Link } from "react-router-dom";
// Pages --------------------
import { Home } from "./pages/Home";
import { ProductDashboard } from "./pages/ProductDashboard";
import { TempStatePage } from "./pages/TempStatePage";
import { TempStatePage2 } from "./pages/TempStatePage2";
import { TempGetStatePage } from "./pages/TempGetStatePage";
import { Login } from "./pages/Login";
import { Register } from "./pages/Register";
import { NotFound } from "./pages/NotFound";
// --------------------------
import ProtectedRoute from "./components/ProtectedRoute";
import { TempProtectedPage } from "./pages/TempProtectedPage";
import APITest from "./pages/APITest";

import "./index.css"
import { ProductDashboard_dummy } from "./pages/ProductDashboard_dummy";
import { ProductInfoPage_dummy } from "./pages/ProductInfoPage_dummy";
import { ProductInfoPage } from "./pages/ProductInfoPage";
// TODO:
// When refactoring rename function to have function clause



// Wrap anything that should not be accessible without authentication
// with a <ProtectedRoute> tag

// Things that need to become protected:
/*
  - /dashboard (dashboard page)
  - /product-info (product information page)
*/

const App = () => {
  return (
    <>
      {/* Create navbar here */}
      
      {/* <nav>
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
      </nav> */}

      {/* Only things inside routes component changes ^ Nav bar above is bing chilling */}
      <Routes>
        <Route index element={<Navigate to="/dashboard" />} />
        <Route path="/home" element={<Home />} />
        <Route path="/dashboard" element={
          <ProtectedRoute>
            <ProductDashboard />
          </ProtectedRoute>
          } /> 
        <Route path="/state">
          <Route index element={<TempStatePage />}/>
          <Route path=":id" element={<TempStatePage />}/>
          {/* This is another way to share state -> useNavigate and useLocation */}
          <Route path="X" element={<TempStatePage2 />}/>
          <Route path="get-state" element={<TempGetStatePage />}/>
          {/* ------------------------ */}
        </Route>
        <Route path="/product-info-dummy" element={<ProductInfoPage_dummy/>} />
        <Route path="/product-info" element={<ProductInfoPage />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/not-found" element={<NotFound />} />
        <Route path="/test-protected" element={
          <ProtectedRoute>
            <TempProtectedPage />
          </ProtectedRoute>
        } />
        <Route path="/api" element={
            <APITest />
        } />
        <Route path="/dummy" element={<ProductDashboard_dummy />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </>
  );
};

export default App;
