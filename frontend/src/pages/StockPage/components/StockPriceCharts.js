import {Grid} from "@mui/material";
import {CartesianGrid, Legend, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis} from "recharts";
import * as PropTypes from "prop-types";
import React from "react";
import {DateTime} from "luxon";

const StockPriceChart = (props) => {

    const dateFormatter = date => {
        return DateTime.fromHTTP(date).toLocaleString(DateTime.DATETIME_SHORT);
    };


    const CustomTooltip = ({active, payload, label}) => {
        if (active && payload && payload.length) {
            return (
                <div className="custom-tooltip" style={{background: "white", color: "black"}}>
                    <p className="label">{`${dateFormatter(label)}`}</p>
                    <p>${parseFloat(payload[0].value).toFixed(2)}</p>
                </div>
            );
        }

        return null;
    };

    return (
        <Grid item>
            <ResponsiveContainer>
                <LineChart data={props.historicalData}>
                    <XAxis dataKey={"time"} domain={["dataMin", "dataMax"]} interval={"preserveStartEnd"}
                           tickFormatter={props.tickFormatter}/>
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
    tickFormatter: PropTypes.func
};

export default StockPriceChart;