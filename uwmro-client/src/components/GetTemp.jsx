import { getTemperature } from "../apiClient";

function GetTemp({currTemp, setCurrTemp}) {

    async function callGetTemperature() {
      setCurrTemp(await getTemperature())
    }


    return (
      <fieldset className="Temperature">
        <label> Current Temperature
          <button onClick={callGetTemperature}>Get Temperature</button>
          {currTemp}
        </label>
      
      
            
      
      </fieldset>
    );
  }

  
  export default GetTemp;
  