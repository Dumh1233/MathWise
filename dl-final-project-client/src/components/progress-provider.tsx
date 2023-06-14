import React, { useEffect,useState } from "react";

const ProgressProvider = ({ valueStart,valueNow, valueEnd,color, children }:any) => {
    const [thisValueEnd, setThisValueEnd] = useState(valueStart);
    const [thisValueNow, setThisValueNow] = useState(valueStart);
    const [thisColor, setThisColor] = useState(valueStart);
    useEffect(() => {
        setThisValueEnd(valueEnd);
        setThisValueNow(valueNow);
        setThisColor(color);
    }, [valueEnd,valueNow,color]);
  
    return children({valueNow:thisValueNow,valueEnd:thisValueEnd,color:thisColor});
  };
  export default ProgressProvider;