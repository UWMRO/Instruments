import './App.css';
import { useState } from "react";
import ImageTypeSelector from './components/ImageTypeSelector';
import GetTemp from './components/TempControls';
import ExposureTypeSelector from './components/SetExposureType';
import FilterTypeSelector from './components/FilterControls';
import ExposureControls from './components/ExposureControls';

function App() {
  const [exposureType, setExposureType] = useState('Single')

  return (
    <div className='App'> Manastash Ridge Observatory Controls
    <form>
      <ImageTypeSelector/>
      <ExposureTypeSelector exposureType={exposureType} setExposureType={setExposureType}/>
      <FilterTypeSelector/>
      <ExposureControls exposureType={exposureType}/>
      <GetTemp/>
    </form>
    </div>
  );
}

export default App;
