import { getTemperature, setTemperature } from "../apiClient";

function GetTemp({temp, setTemp}) {
    

    async function callGetTemperature() {
      setTemp(await getTemperature())
    }

    async function callSetTemperature(e) {
      e.preventDefault()
      setTemp(await setTemperature(e))
    }

    return (
      <form onSubmit={callSetTemperature}>Temperature
        <input onChange={(e) => callSetTemperature(e.target.value)} value={temp} />
        <button type='submit'>Click To Submit</button>
        <div>
          {temp}
        </div>
        <button onClick={callGetTemperature}>Get Temperature</button>
      </form>
      
            
      
      
    );
  }

  
  export default GetTemp;
  