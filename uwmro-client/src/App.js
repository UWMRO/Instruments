import './App.css';
import { useState } from "react";
import ImageTypeSelector from './components/ImageTypeSelector';
import GetTemp from './components/TempControls';
import ExposureTypeSelector from './components/SetExposureType';
import FilterTypeSelector from './components/FilterControls';
import ExposureControls from './components/ExposureControls';
import logo from './aueg_logo.png'

function App() {
  const [exposureType, setExposureType] = useState('Single')
  const [imageType, setImageType] = useState('Bias')
  const [filterType, setFilterType] = useState('Ha')
  const [temp, setTemp] = useState('-999')

  return (
    <div className='App'> Manastash Ridge Observatory Controls
    <img src={logo} className='Logo' alt='Logo'/>
    <form>
      <ImageTypeSelector imageType={imageType} setImageType={setImageType}/>
      <ExposureTypeSelector exposureType={exposureType} setExposureType={setExposureType}/>
      <FilterTypeSelector filterType={filterType} setFilterType={setFilterType}/>
      <ExposureControls exposureType={exposureType}/>
      <GetTemp/>
    </form>
    </div>
  );
}

export default App;
