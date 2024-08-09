import { Form } from "../components/Form"


export const Login = () => {
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
