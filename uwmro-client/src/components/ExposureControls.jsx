import { capture } from "../apiClient"
import { useForm } from "react-hook-form"

function ExposureControls({ exposureType, imageType, filterType }) {

    const {register, handleSubmit, errors} = useForm()

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

    const onSubmit = (data) => {
        data.exp_type = exposureType
        data.img_type = imageType
        data.fil_type = filterType

        const message = capture(data)
        console.log(message)
    }

    return (
        <form onSubmit={handleSubmit(onSubmit)} className='exposure-controls'>
            
            <legend>
                Exposure Controls
            </legend>
            <label> File Name 
                <input type='text' {...register('file_name', { required: true })}/>
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