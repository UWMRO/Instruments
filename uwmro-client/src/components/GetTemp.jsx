import { useState } from "react";
import { getTemperature } from "../apiClient";

function GetTemp() {
    const [variable, setVariable] = useState('initialized');

    async function callGetTemperature() {
        setVariable(await getTemperature())
    }

    return (
      <div className="Temperature">
        <button onClick={callGetTemperature}>Get Temperature</button>
        <div>
        {variable}
        </div>
      </div>
      
    );
  }
  
  export default GetTemp;
  