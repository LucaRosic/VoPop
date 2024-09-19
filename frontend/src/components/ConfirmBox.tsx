import { Dialog, DialogContent } from "@mui/material"
interface Props {
  open: boolean,
  handleClose: () => void,
  productId: number|null,
  confirmDeleteCallback: (arge0:number|null) => void,
}
const ConfirmBox = ({open, handleClose, productId, confirmDeleteCallback} : Props) => {
  return (
    <Dialog
      fullWidth
      open={open}
      onClose={handleClose}
      maxWidth="xs"
      scroll="body"
    >
      <DialogContent>
        <div className="flex flex-col items-center gap-3">
          <div className="font-bold">
            Are you sure you want to remove?
          </div>
          <div className="flex gap-4">
            <button className="bg-red-600 text-white p-2" onClick={() => confirmDeleteCallback(productId)}> Remove</button>
            <button className="bg-blue-600 text-white p-2" onClick={handleClose}> Cancel</button>
          </div>
        </div>
         
      </DialogContent>
    
    </Dialog>
  )
}
export default ConfirmBox