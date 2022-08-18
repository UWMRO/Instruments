import { useState, Component } from "react";
import { getTemperature, setTemperature } from "../apiClient";

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

function SetTemp() {
  const [variable, setVariable] = useState('initialized');

  async function callSetTemperature(e) {
    setVariable(await setTemperature(e))
  }

  async function callGetTemperature() {
    setVariable(await getTemperature())
}

  <div className="Temperature">
        <input type='number' value={callGetTemperature} onChange={callSetTemperature}>Set Temperature</input>
        <div>
        {variable}
        </div>
      </div>

}
  
  export default GetTemp;
  