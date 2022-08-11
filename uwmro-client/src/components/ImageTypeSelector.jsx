function ExposureTypeSelector() {
  return (
    <fieldset> 
        <legend>
            Image Type
        </legend>
        <label> Bias
            <input type='radio' name='ImageType' onChange={GetImageTypeClicked} value='Bias'/>
        </label>
        <label> Flat
            <input type='radio' name='ImageType' onChange={GetImageTypeClicked} value='Flat'/>
        </label>
        <label> Dark
            <input type='radio' name='ImageType' onChange={GetImageTypeClicked} value='Dark'/>
        </label>
        <label> Object
            <input type='radio' name='ImageType' onChange={GetImageTypeClicked} value='Object'/>
        </label>
    </fieldset>
  );
}

function GetImageTypeClicked(e) {
    console.log(e.target.value)
}

export default ExposureTypeSelector;
