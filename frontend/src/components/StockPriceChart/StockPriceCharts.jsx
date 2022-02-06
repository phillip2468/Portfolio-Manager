import { Grid } from '@mui/material'
import { CartesianGrid, Line, LineChart, Tooltip, XAxis, YAxis } from 'recharts'
import * as PropTypes from 'prop-types'
import React from 'react'

const StockPriceChart = (props) => {
  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
                <div className="custom-tooltip" style={{ background: 'white', color: 'black' }}>
                    <p className="label">{`${props.formatTime(label)}`}</p>
                    <p>${parseFloat(payload[0].value).toFixed(2)}</p>
                </div>
      )
    }

    CustomTooltip.propTypes = {
      active: PropTypes.bool,
      payload: PropTypes.any,
      label: PropTypes.string
    }

    return null
  }

  return (
        <Grid item>
            <LineChart data={props.historicalData} height={props.heightOfChart} width={props.widthOfChart}>
              <XAxis dataKey={'time'} domain={['dataMin', 'dataMax']} interval={'preserveStartEnd'}
                     tickFormatter={props.formatTime}/>
              <YAxis domain={['auto', 'auto']}/>
              <CartesianGrid strokeDasharray="2 2"/>
              <Tooltip content={<CustomTooltip/>}/>
              <Line activeDot={{ r: 3 }} dataKey={'open'} stroke="#8884d8" type="monotone"/>
            </LineChart>
        </Grid>
  )
}

StockPriceChart.propTypes = {
  historicalData: PropTypes.arrayOf(PropTypes.any),
  formatTime: PropTypes.func,
  heightOfChart: PropTypes.any,
  widthOfChart: PropTypes.number,
  priceList: PropTypes.objectOf(PropTypes.shape({
    open: PropTypes.string,
    time: PropTypes.string
  }))
}

export default StockPriceChart
