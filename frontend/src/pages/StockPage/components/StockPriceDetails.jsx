import { Grid } from '@mui/material'
import { MiscDetailsStock, StockInfoContainer, StockPercentageChange } from '../styled'
import { TriangleSymbol } from '../../../components/SearchBar/styled'
import * as PropTypes from 'prop-types'
import React from 'react'

const StockPriceDetails = (props) => {
  return <Grid item>
        <StockInfoContainer>
            <div style={{ fontSize: '2em' }}>
                ${parseFloat(props.stockInfo.market_current_price).toFixed(2)}
            </div>
            <div style={{ fontSize: '1.2em' }}>
                <StockPercentageChange percentageChange={props.stockInfo.market_change_percentage}>
                    {props.stockInfo.market_change_percentage > 0
                      ? <TriangleSymbol>&#x25B2;</TriangleSymbol>
                      : <TriangleSymbol>&#x25BC;</TriangleSymbol>}
                    {(props.stockInfo.market_change_percentage * 100).toFixed(2)}%
                </StockPercentageChange>
            </div>
            <div>
                {props.stockInfo.market_change > 0 ? ('+') : ('-')}
                {(props.stockInfo.market_change)}
            </div>
        </StockInfoContainer>
        <MiscDetailsStock>
            {props.lastUpdatedFmt} {props.stockInfo.currency} {props.stockInfo.exchange}
        </MiscDetailsStock>
    </Grid>
}

StockPriceDetails.propTypes = {
  stockInfo: PropTypes.shape({
    currency: PropTypes.string,
    exchange: PropTypes.string,
    market_change: PropTypes.number,
    market_change_percentage: PropTypes.number,
    market_current_price: PropTypes.string
  }),
  lastUpdatedFmt: PropTypes.string
}

export default StockPriceDetails
