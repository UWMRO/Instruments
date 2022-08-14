import './App.css';
import ImageTypeSelector from './components/ImageTypeSelector';
import GetTemp from './components/GetTemp';
import ExposureTypeSelector from './components/SetExposureType';

function App() {
  return (
    <div className='App'> Manastash Ridge Observatory Controls
      <ImageTypeSelector/>
      <ExposureTypeSelector/>
      <GetTemp/>
    </div>
  );
}

export default App;
