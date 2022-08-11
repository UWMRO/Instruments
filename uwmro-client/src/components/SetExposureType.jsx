function ExposureTypeSelector() {
    return (
      <fieldset> 
          <legend>
              Exposure Type
          </legend>
          <label> Single
              <input type='radio' name='ImageType' onChange={GetExposureTypeClicked} value='Single'/>
          </label>
          <label> Real Time
              <input type='radio' name='ImageType' onChange={GetExposureTypeClicked} value='Real Time'/>
          </label>
          <label> Series
              <input type='radio' name='ImageType' onChange={GetExposureTypeClicked} value='Series'/>
          </label>
          
      </fieldset>
    );
  }
  
  function GetExposureTypeClicked(e) {
      console.log(e.target.value)
  }
  
  export default ExposureTypeSelector;
  