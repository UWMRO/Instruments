import { useState } from "react";
import { useForm } from "react-hook-form"
import { getTemperature, setTemperature } from "../apiClient";

function GetTemp({temp, setTemp}) {
    // const [input, setInput] = useState(temp)
    // const [sent, setSent] = useState(false)
    const {register, handleSubmit, errors} = useForm()

    async function callGetTemperature() {
      setTemp(await getTemperature())
    }

    async function callSetTemperature(value) {
      setTemp(await setTemperature(value))
    }

    
      
    

    const onSubmit = (data) => {
      const val = parseInt(data.temp)
        if (isNaN(val)){
            console.log('Not A Number')
        } else {
          
          callSetTemperature(data)
          //setSent(false)
          console.log('temperature set!')
        }
    }

    return (
      <form onSubmit={handleSubmit(onSubmit)}>
        <label>Input Temperature (Celsius)
        <input type='text' {...register('temp', { required: true })} placeholder='temperature (celsius)'/>
        </label>
        <input type='submit'/>
        
        <button onClick={callGetTemperature} name='get temp'>Get Temp</button>
        
        {temp}
      </form>
      
            
      
      
    );
  }

  
  export default GetTemp;
  