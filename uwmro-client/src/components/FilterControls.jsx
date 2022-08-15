function FilterTypeSelector() {
    return (
      <fieldset> 
          <legend>
              Filters
          </legend>
          <label> Ha
              <input type='radio' name='ImageType' onChange={GetFilterTypeClicked} value='Ha'/>
          </label>
          <label> B
              <input type='radio' name='ImageType' onChange={GetFilterTypeClicked} value='B'/>
          </label>
          <label> V
              <input type='radio' name='ImageType' onChange={GetFilterTypeClicked} value='V'/>
          </label>
          <label> g
              <input type='radio' name='ImageType' onChange={GetFilterTypeClicked} value='g'/>
          </label>
          <label> r
              <input type='radio' name='ImageType' onChange={GetFilterTypeClicked} value='r'/>
          </label>
      </fieldset>
    );
  }
  
  function GetFilterTypeClicked(e) {
      console.log(e.target.value)
  }
  
  export default FilterTypeSelector;