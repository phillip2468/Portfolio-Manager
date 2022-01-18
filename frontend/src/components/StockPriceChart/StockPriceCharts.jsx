import {Grid} from "@mui/material";
import {CartesianGrid, Legend, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis} from "recharts";
import * as PropTypes from "prop-types";
import React from "react";

const StockPriceChart = (props) => {


    const CustomTooltip = ({active, payload, label}) => {
        if (active && payload && payload.length) {
            return (
                <div className="custom-tooltip" style={{background: "white", color: "black"}}>
                    <p className="label">{`${props.formatTime(label)}`}</p>
                    <p>${parseFloat(payload[0].value).toFixed(2)}</p>
                </div>
            );
        }

        return null;
    };

    return (
        <Grid item>
            <ResponsiveContainer height={props.heightOfChart}>
                <LineChart data={props.historicalData}>
                    <XAxis dataKey={"time"} domain={["dataMin", "dataMax"]} interval={"preserveStartEnd"}
                           tickFormatter={props.formatTime}/>
                    <YAxis domain={["auto", "auto"]}/>
                    <CartesianGrid strokeDasharray="2 2"/>
                    <Tooltip content={<CustomTooltip/>}/>
                    <Legend/>
                    <Line type="monotone" dataKey={"open"} activeDot={{r: 3}} stroke="#8884d8"/>
                </LineChart>
            </ResponsiveContainer>
        </Grid>
    );
}

StockPriceChart.propTypes = {
    historicalData: PropTypes.arrayOf(PropTypes.any),
    formatTime: PropTypes.func,
    heightOfChart: PropTypes.number
};

export default StockPriceChart;