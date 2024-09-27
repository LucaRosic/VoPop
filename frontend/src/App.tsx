import { Routes, Route, Navigate } from "react-router-dom";
import ProtectedRoute from "./components/ProtectedRoute";
import "./index.css"

// Pages --------------------
import { Home } from "./pages/Home";
import { ProductDashboard } from "./pages/ProductDashboard";
import { Login } from "./pages/Login";
import { Register } from "./pages/Register";
import { NotFound } from "./pages/NotFound";
import { ProductInfoPage } from "./pages/ProductInfoPage";
import APITest from "./pages/APITest";
// --------------------------

// Dummy pages --------------
import { ProductDashboard_dummy } from "./pages/dummy/ProductDashboard_dummy";
import { ProductInfoPage_dummy } from "./pages/dummy/ProductInfoPage_dummy";
import { ProductDashboardGlobal } from "./pages/ProductDashboardGlobal";
import { UserContextProvider } from "./app-context/Store";
// --------------------------

/*
  Pages to still create:
  - Homepage
*/

const App = () => {
  /*
    Defines the routes for the web application.
  */
  
  return (
    <>

      <Routes>
        <Route index element={<Navigate to="/dashboard" />} />
        <Route path="/home" element={<Home />} />
        <Route path="/dashboard" element={
          <ProtectedRoute>
            <ProductDashboard />
          </ProtectedRoute>
        } />  

        {/* <Route path="/dashboard" element={
          <ProtectedRoute>
            <UserContextProvider>
              <ProductDashboardGlobal />
            </UserContextProvider>
          </ProtectedRoute>
        } /> */}
        <Route path="/product-info" element={
          <ProtectedRoute>
            <ProductInfoPage />
          </ProtectedRoute>
          } />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/not-found" element={<NotFound />} />
        <Route path="/api" element={
            <APITest />
        } />

        {/* Dummy pages (for testing without connection to backend server) */}
        <Route path="/dummy" element={<ProductDashboard_dummy />} />
        <Route path="/product-info-dummy" element={<ProductInfoPage_dummy/>} />

        {/* Route for undefined routes */}
        <Route path="*" element={<NotFound />} />
      </Routes>
    </>
  );
};

export default App;
