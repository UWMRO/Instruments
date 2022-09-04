import { useState } from "react";
import { useForm } from "react-hook-form"
import { getTemperature, setTemperature } from "../apiClient";

function GetTemp({temp, setTemp}) {
    const [input, setInput] = useState(temp)
    // const [sent, setSent] = useState(false)
    const {register, handleSubmit, errors} = useForm()

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

    const onSubmit = (data) => {
      console.log(data)
    }

    return (
      <form onSubmit={handleSubmit(onSubmit)}>
        <label>Input Temperature</label>
        <input type='text' {...register('temp', { required: true })}/>
        
        <input type='submit'/>
      </form>
      
            
      
      
    );
  }

  
  export default GetTemp;
  