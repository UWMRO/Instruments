import { capture } from "../apiClient"
import { useForm } from "react-hook-form"


function ExposureControls({ exposureType, imageType, filterType, setDownloadPath }) {

    const {register, handleSubmit, errors} = useForm()
    // const [state, setState] = 

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


    const onSubmit = async data => {
        data.exp_type = exposureType
        data.img_type = imageType
        data.fil_type = filterType

        const message = await capture(data)
        console.log(message.message)
    }

    return (
        <form onSubmit={handleSubmit(onSubmit)} className='exposure-controls'>
            
            <legend>
                Exposure Controls
            </legend>
            <label> File Name 
                <input type='text' {...register('file_name', { required: false })} placeholder="image.fits"/>
            </label>
            {exposureType !== 'Real Time'
            && <label> Exposure Time
                <input type='text' {...register('exp_time', { required: true })}/>
                </label>
            }
            {exposureType === 'Series'
            && <label> Number of Exposures
                <input type='text' {...register('exp_num', { required: false })}/>
                </label>
            }
            <button type='submit'>Get Exposure</button>

            
        </form>
    );


  }
  
  
  
  
  export default ExposureControls;