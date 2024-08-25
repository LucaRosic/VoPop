import { Skeleton } from "@mui/material";

const ProductCardLoading = () => {
  return (
    <div
      className="product-card bg-slate-100 w-[60vw] h-60 px-8 py-4 flex gap-4 border-2 
      border-gray-400 select-none transform hover:scale-[1.02] hover:shadow-[10px_10px_0px_-5px_rgba(35,106,114)] transition-all shadow-[10px_10px_0px_0px_rgba(35,106,114)]"
    >
        <Skeleton variant="rectangular" width={"30%"} height={"100%"} />
        <div className="w-[70%] flex flex-col gap-4">
            <Skeleton variant="rectangular" width={"100%"} height={"40%"} />
            <div className="h-full">
                <Skeleton variant="text" width={"100%"} height={"25%"} animation="wave" />
                <Skeleton variant="text" width={"100%"} height={"25%"} animation="wave" />
                <Skeleton variant="text" width={"100%"} height={"25%"} animation="wave" />
                <Skeleton variant="text" width={"100%"} height={"25%"} animation="wave" />
            </div>
        </div>
        
    </div>
  );
};

export default ProductCardLoading;
