import { useParams } from "react-router-dom"

export const TempStatePage = () => {
  const { id } = useParams()
  const thereIsId = (id !== undefined)
  const DisplayState = (id : string | undefined) => {
    return (
      <h2>State {id}</h2>
    )
  }
  // If you do /state nothing shows up
  // If you do /state/<id> something shows up!
  // /state/1 -> State 1 displayed :D

  return (
    <>
      <h1>Product State Page :D</h1>
      {thereIsId && DisplayState(id)}
    </>
  )
}
