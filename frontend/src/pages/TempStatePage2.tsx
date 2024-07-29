import { useNavigate } from "react-router-dom"

export const TempStatePage2 = () => {

  const navigate = useNavigate();

  const navFunc = (meaning : string) => {
    navigate('/state/get-state', { state: { meaning: meaning } }); 
  }

  return (
    <>
      <h1>Navigate Page</h1>
      <button onClick={() => navFunc('42')}>Navigate With State</button>
    </>
  )
}
