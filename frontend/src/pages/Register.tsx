import { useEffect, useState } from "react";
import { Form } from "../components/Form";
import { useNavigate } from "react-router-dom";
import { isLoggedIn } from "../tokenManager";

export const Register = () => {
  /*
    Component for register form. This is to allow users to register an account.
  */

  const [loading, setLoading] = useState<boolean>(false);
  const navigate = useNavigate();

  // On page load check if user is already logged in
  useEffect(() => {
    setLoading(true); // Set loading to try whilst confirming
    // Check if user is already logged in -> if so, then don't allow them on this page.
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
