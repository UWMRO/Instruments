import { capture } from "../apiClient"

function ExposureControls({ exposureType, imageType, filterType, temp }) {

    function eventChange(e) {
        console.log(e.target.value)
    }

    function ExposureTimeChanged(e) {
        const val = parseFloat(e.target.value)
        if (isNaN(val)){
            console.log('Not A Number')
        } else {console.log(val)}
    }

    // should call startAcquisition
    async function getExposure() {
        const img = await capture()
        console.log(img)
    }

    // to-do for get-exposure:
    // 1.) check each prop for errors
    // 2.) using each prop, take the image with parameters
    // 3.) 

    return (
      <fieldset className='exposure-controls'> 
          <legend>
              Exposure Controls
          </legend>
          <label> Save Name 
              <input type='text' name='Save Name' onChange={eventChange}/>
          </label>
          <label> Exposure Time
              <input type='text' name='Exposure Time' onChange={ExposureTimeChanged}/>
          </label>
          {exposureType === 'Series'
            && <label> Number of Exposures
                <input type='text' name='Number of Exposures' onChange={ExposureTimeChanged}/>
               </label>
          }
          <button onClick={getExposure}>Get Exposure</button>

      </fieldset>
    );


  }
  
  
  
  
  export default ExposureControls;