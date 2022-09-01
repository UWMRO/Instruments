import { useState } from "react";
import { getTemperature, setTemperature } from "../apiClient";

function GetTemp({temp, setTemp}) {
    const [input, setInput] = useState(temp)
    // const [sent, setSent] = useState(false)

    async function callGetTemperature() {
      setTemp(await getTemperature())
    }

    async function callSetTemperature(value) {
      value.preventDefault()
      setTemp(await setTemperature(value))
    }

    async function sendInputTemp() {
      console.log(typeof input)
      const val = parseFloat(input)
        if (isNaN(val)){
            console.log('Not A Number')
        } else {
          setTemp(callSetTemperature(input))
          //setSent(false)
          console.log('temperature set!')
        }
      
    }

    return (
      <div>Temperature
        
        
        <input type='text' onChange={(e)=>setInput(e.target.value)}/>
        {input}
        <button onClick={sendInputTemp}>Click To Submit</button>
        


        <button onClick={callGetTemperature}>Get Temperature</button>
        {temp}
      </div>
      
            
      
      
    );
  }

  
  export default GetTemp;
  