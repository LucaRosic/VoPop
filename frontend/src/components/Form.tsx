import { useState } from "react"
import api from "../api"
import { useNavigate } from "react-router-dom"
import { ACCESS_TOKEN, REFRESH_TOKEN, USERNAME } from "../constants"
import "../styles/Form.css" // Import the Form.css stylesheet

interface Props {
    route: string; // String for api route
    method: string; // String for type of form method required
}


export const Form = ({route, method} : Props) => {
  /*
    Generic form to be used by either the login or register page.

    Form details filled in by user and is sent to the necessary API endpoint.
  */

  const [username, setUsername] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);
  const navigate = useNavigate();

  const handleSubmit = async (e : React.FormEvent) => {
    setLoading(true);
    e.preventDefault();

    try {
      const res = await api.post(route, {username, password}); // Send username and password to the api endpoint
      if (method === "login") { // For login method
        console.log(`REFRESH SET TO: ${res.data.refresh}`);
        localStorage.setItem(ACCESS_TOKEN, res.data.access);
        localStorage.setItem(REFRESH_TOKEN, res.data.refresh);
        localStorage.setItem(USERNAME, username);
        console.log("Set the Tokens!")
        navigate("/dashboard"); // Navigate back to home
      } else { // For register method
        // Register method should redirect to login page
        navigate("/login");
      }

    } catch (error) {
      alert(error);
    } finally {
      setLoading(false); // No matter what happens, loading has stopped
    }
  }

  const formName = method === "login" ? "Login" : "Register";

  return (
    <form onSubmit={handleSubmit} className="form-container">
      <h1>{formName}</h1>
      <input 
        className="form-input"
        type="text"
        value={username}
        onChange={(e) => {setUsername(e.target.value)}}
        placeholder="Username"
      />
      <input 
        className="form-input"
        type="password"
        value={password}
        onChange={(e) => {setPassword(e.target.value)}}
        placeholder="Password"
      />
      <button className="form-button" type="submit">
        {formName}
      </button>
    </form>
  )
}
