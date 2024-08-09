import { Form } from "../components/Form";

export const Register = () => {
  return (
    <div className="text-center">
      <Form route="/api/user/register/" method="register" />
      <p>Have an Account? <a href="/login">Login</a></p>
    </div>
  );
};
