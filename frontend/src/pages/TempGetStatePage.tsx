import { useLocation } from "react-router-dom"

export const TempGetStatePage = () => {

  const {state} = useLocation();
  if (state === null) {
    return (<h2>No give state.</h2>)
  }
  const {meaning} = state;
  
  return (
    <>
      <h1>Temp Get State</h1>
      <h2>Meaning: {meaning}</h2>
    </>
  )
}
