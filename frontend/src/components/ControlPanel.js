function ControlPanel({

    region,
    setRegion,

    mode,
    setMode
}){

    return(

        <div
            style={{
                background:"yellow",
                margin:20,
                padding:20,
                height:250,
                border:"4px solid black"
            }}
        >

            <h2>地點搜尋</h2>

            <select
                value={region}
                onChange={(e)=>
                    setRegion(e.target.value)
                }
            >

                <option>全台</option>

                <option>台北市</option>

                <option>新北市</option>

                <option>桃園市</option>

                <option>台中市</option>

                <option>台南市</option>

                <option>高雄市</option>

            </select>

            <br /><br />

            <button
                onClick={()=>
                    setMode("radar")
                }
            >
                雷達迴波圖
            </button>

            <button
                onClick={()=>
                    setMode("prob")
                }
            >
                降雨機率圖
            </button>

        </div>
    )
}

export default ControlPanel