import {useEffect, useState} from "react";

const PredictorPage = () => {

    const [data, setData] = useState([])

    useEffect( ()=> {
        fetch("/past-data")
            .then(res => res.json())
            .then(res => setData(res))
            .catch(() => console.log("ERROR"))
        }
    , [])

    return (
        <>
            {"This stupid thing thinks that the price for this stock next day will be" + data["next_day"]}
            Hi there
        </>
    )
}

export default PredictorPage;