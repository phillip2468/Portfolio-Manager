// noinspection JSValidateTypes

import { useParams } from 'react-router-dom'
import React, { useEffect, useState } from 'react'
import { Divider } from '@mui/material'
import Button from '@mui/material/Button'
import StockPriceChart from '../../components/StockPriceChart/StockPriceCharts'
import StockIntervals from './components/StockIntervals'
import StockPriceDetails from './components/StockPriceDetails'
import StockDetails from './components/StockDetails'
import { FetchFunction } from '../../components/FetchFunction'

const { DateTime } = require('luxon')

const StockPage = () => {
  const { stockName } = useParams()
  const [stockInfo, setStockInfo] = useState({})
  const lastUpdatedFmt = DateTime.fromISO(stockInfo.last_updated).toLocaleString(DateTime.DATETIME_SHORT_WITH_SECONDS)
  const listOfPeriods = ['1d', '5d', '7d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']
  const [historicalData, setHistoricalData] = useState([])

  useEffect(() => {
    if (stockName !== '') {
      FetchFunction('GET', `/quote/${stockName}`, null)
        .then(res => setStockInfo(res))
        .catch(error => alert(error.msg))
      handleGetHistoricalData('1d')
    }
  }, [stockName])

  const handleGetHistoricalData = (period) => {
    FetchFunction('GET', `/quote/${stockName}&period=${period}&interval=30m`, null)
      .then(res => setHistoricalData(res))
      .catch(error => alert(error.msg))
  }

  const dateFormatter = date => {
    return DateTime.fromHTTP(date).toLocaleString(DateTime.DATETIME_SHORT)
  }

  return (
        <>
            <StockDetails
                stockInfo={stockInfo}
            />

            <Divider light={true}/>

            <StockPriceDetails
                lastUpdatedFmt={lastUpdatedFmt}
                stockInfo={stockInfo}
            />

            <StockIntervals callbackfn={(element, index) => {
              return (
                    <Button key={index} onClick={() => handleGetHistoricalData(element)} size={'small'}>
                        {element}
                    </Button>
              )
            }} listOfIntervals={listOfPeriods}/>

            <StockPriceChart
                formatTime={dateFormatter}
                heightOfChart={500}
                historicalData={historicalData.priceList}
                widthOfChart={1000}
            />
        </>
  )
}

export default StockPage
