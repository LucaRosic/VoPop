import { useNavigate } from "react-router-dom";
import NavbarTop from "../../components/NavbarTop";
import Footer from "../../components/Footer";
import { ProductCard_dummy } from "../../components/dummy/ProductCard_dummy";
import { useState } from "react";
import ConfirmBox from "../../components/ConfirmBox";

export const ProductDashboard_dummy = () => {
  /*
    Create a dummy product dashboard page using dummy data. This page is to work
    without needing any connection established with backend server
  */

  const navigate = useNavigate();

  const navFunc = (prodId : number) => {
    navigate('/product-info-dummy', { state: { prodId: prodId, meaning : 'test' } }); 
  }

  const [productsList, setProductsList] = useState<number[]>([0,1,2,3]);
  const [dialogOpen, setDialogOpen] = useState<boolean>(false);
  const [deleteProdId, setDeleteProdId] = useState<number|null>(null);


  const confirmDeleteCardCallback = (prodId:number|null)  => {
    setProductsList(prev => prev.filter(element => element !== prodId ))

    setDialogOpen(false);
    setDeleteProdId(null);
  }

  const deleteCard = (prodId:number|null) => {
    console.log(`Delete product: ${prodId}`);
    setDeleteProdId(prodId);
    setDialogOpen(true);
  }

  return (
    <>
      <NavbarTop urlScraperCallback={(arg:string) => (console.log(arg))}/>
      <div className="flex flex-col gap-8 bg-[#FBF5F3]">
        <div  
          className="flex flex-col items-center gap-4 px-32 pt-4"
        >
          {productsList.map((product) => (
            <ProductCard_dummy
              key={product}
              productId={product}
              deleteCallback={deleteCard}
              onClick={() => navFunc(product)}
            />
          ))}
        </div>
        <ConfirmBox 
          open={dialogOpen}
          handleClose={() => setDialogOpen(false)}
          productId={deleteProdId}
          confirmDeleteCallback={confirmDeleteCardCallback}
        />
        <Footer />
      </div>
    </>
  );
};
