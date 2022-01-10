import {useEffect, useState} from "react";
import {XAxis, YAxis, LineChart, Line, CartesianGrid, Tooltip, Legend, ResponsiveContainer} from "recharts";

const _ = require('lodash');

const PredictorPage = () => {


    const [data, setData] = useState([])
    const [actualPrices, setActualPrices] = useState([])
    const [predictedPrices, setPredictedPrices] = useState([])

    useEffect( ()=> {
        fetch("/ai-data")
            .then(res => res.json())
            .then(res => {
                setActualPrices(res["actual"])
                setPredictedPrices(res["predicted"])
                setData(res["next_day"])
            })
            .catch((error) => console.log(error))
        }
    , [])

    return (
        <>
            {"This stupid thing thinks that the price for this stock next day will be " + data}
            <ResponsiveContainer height={500}>
                <LineChart height={300} >
                    <XAxis type="number" dataKey={"day"} domain={['auto', 'auto']}/>
                    <YAxis domain={[50, 'auto']}/>
                    <CartesianGrid strokeDasharray="3 3"/>
                    <Tooltip/>
                    <Legend />
                    <Line type="monotone" data={actualPrices} dataKey="price" stroke="darkgreen" activeDot={{r: 8}} name={"Actual"}/>
                    <Line type="monotone" data={predictedPrices} dataKey="price" stroke="#8884d8" name={"Predicted"}/>
                </LineChart>
            </ResponsiveContainer>

        </>
    )
}

export default PredictorPage;