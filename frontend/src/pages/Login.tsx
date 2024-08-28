import { useNavigate } from "react-router-dom";
import { Form } from "../components/Form"
import { isLoggedIn } from "../tokenManager";
import { useEffect, useState } from "react";
import { ACCESS_TOKEN } from "../constants";


export const Login = () => {

  const [loading, setLoading] = useState<boolean>(false);
  const navigate = useNavigate();


  useEffect(() => {
    setLoading(true); // Set loading to try whilst confirming
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
