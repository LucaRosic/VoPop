const delay = (delayInms:number) => {
    return new Promise(resolve => setTimeout(resolve, delayInms));
};


const longFunc = async () => {
    await delay(5000);
    console.log("Worker Long Func Finished!");
    localStorage.setItem("TEST", "State 1");
}

onmessage = (message) => {
    if (message.data === "PERSISTENT") {
        longFunc();
    }
    else {
      console.log("ELSE");
    }
   
}