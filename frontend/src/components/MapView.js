import { useEffect, useRef } from "react";

import { renderRadar } from "../renderRadar";

import { renderProbability } from "../renderProbability";

function MapView({

    mode,

    current
}){

    const canvasRef = useRef();

    useEffect(()=>{

        const canvas = canvasRef.current;

        if(mode === "radar"){

            renderRadar(
                canvas,
                current.dbz
            )

        }else{

            renderProbability(
                canvas,
                current.probability
            )
        }

    }, [current, mode])

    return(

        <div
            style={{
                background:"#EEE",
                flex:1,
                margin:20,
                border:"4px solid black",

                display:"flex",

                justifyContent:"center",

                alignItems:"center"
            }}
        >

            <canvas
                ref={canvasRef}
                style={{
                    width:"100%",
                    height:"100%",
                    objectFit:"contain"
                }}
            />

        </div>
    )
}

export default MapView