import { useEffect, useState } from "react";
import { Form } from "../components/Form";
import { useNavigate } from "react-router-dom";
import { isLoggedIn } from "../tokenManager";

export const Register = () => {

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
    console.log("Register allowed");
    return (
      <div className="text-center">
        <Form route="/api/user/register/" method="register" />
        <p>Have an Account? <a href="/login">Login</a></p>
      </div>
    );
  }
};
