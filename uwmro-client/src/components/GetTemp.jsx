import { useForm } from "react-hook-form"
import { getTemperature } from "../apiClient";

function GetTemp({currTemp, setCurrTemp}) {

    const {register, handleSubmit, errors} = useForm()

    async function callGetTemperature() {
      setCurrTemp(await getTemperature())
    }


    return (
      <fieldset class="Temperature">
        <label> Current Temperature
          <button onClick={callGetTemperature}>Get Temperature</button>
          {currTemp}
        </label>
      
      
            
      
      </fieldset>
    );
  }

  
  export default GetTemp;
  