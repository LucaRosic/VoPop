import { useEffect, useState } from "react";
import { Form } from "../components/Form";
import { useNavigate } from "react-router-dom";
import { isLoggedIn } from "../tokenManager";


export const Login = () => {
  /*
    Component for login form. This is to allow users to log in and get authorized.
  */

  const [loading, setLoading] = useState<boolean>(false);
  const navigate = useNavigate();

  // On page load check if the user is already logged in
  useEffect(() => {
    setLoading(true); // Set loading to try whilst confirming
    // If user is already logged in, do not allow them to this page.
    isLoggedIn().then((res) => {
      if (res) {
        navigate("/dashboard");
      }
    }).finally(() => setLoading(false));
    
  }, []);

  if (loading) {
    return (
      <div className="h-full flex items-center">
        <h1>Loading...</h1>
      </div>
    )
  } else {
    return (
      <div className="text-center">
        <Form
          route="/api/token/"
          method="login" 
        />
        <p>No Account? <a href="/register">Register</a></p>
      </div>
      
    )
  }

  
}
