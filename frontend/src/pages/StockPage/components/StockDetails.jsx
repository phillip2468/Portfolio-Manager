import {Grid} from "@mui/material";
import * as PropTypes from "prop-types";
import React from "react";

const StockDetails = (props) => {
    return <Grid item>
        <div>
            {props.stockInfo.symbol}
        </div>
        <div style={{fontSize: "2em"}}>
            {props.stockInfo !== [] && props.stockInfo.stock_name}
        </div>
    </Grid>;
}

StockDetails.propTypes = {
    stockInfo: PropTypes.any,
};

export default StockDetails;