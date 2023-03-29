import { capture } from "../apiClient"
import { useForm } from "react-hook-form"
import {useEffect, useState} from "react"



function ExposureControls({ exposureType, imageType, filterType }) {

    const [playing, setPlaying] = useState(false)
    const [audio] = useState(new Audio(process.env.PUBLIC_URL + '/tadaa-47995.mp3'))

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
        // if exposure time is less than 0, set it to 0
        data.exp_time = Math.max(0, data.exp_time)
        // make sure exposure number is at least 1 exposure
        data.exp_num = Math.max(1, data.exp_num)

        data.exp_type = exposureType
        // if exposure time is 0, use bias type
        data.img_type = data.exp_time == 0 ? "Bias" : imageType

        data.fil_type = filterType

        const message = await capture(data)

        console.log(message)
        // need to create url for file
        window.JS9.Load(message.url)

        // Play sounds after exposure completes.
        console.log('here')
        setPlaying(true)

    }

    useEffect(() => {
        playing ? audio.play() : audio.pause();
      },
      [playing, audio]
    );

    useEffect(() => {
      audio.addEventListener('ended', () => setPlaying(false));
      return () => {
        audio.removeEventListener('ended', () => setPlaying(false));
      };
    }, [audio]);

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
                <input type='number' {...register('exp_time', { required: true })}/>
                </label>
            }
            {exposureType === 'Series'
            && <label> Number of Exposures
                <input type='number' {...register('exp_num', { required: false })}/>
                </label>
            }
            <button type='submit'>Get Exposure</button>

        </form>
    );


  }

  export default ExposureControls;
