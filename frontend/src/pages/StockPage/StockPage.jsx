// noinspection JSValidateTypes

import { useParams } from 'react-router-dom'
import React, { useEffect, useState } from 'react'
import { Grid } from '@mui/material'
import StockPriceChart from '../../components/StockPriceChart/StockPriceCharts'
import StockPriceDetails from './components/StockPriceDetails'
import StockDetails from './components/StockDetails'
import { FetchFunction } from '../../components/FetchFunction'
import StockTimeButtons from './components/StockTimeButtons'

const { DateTime } = require('luxon')

const StockPage = () => {
  const { stockName } = useParams()
  const [stockInfo, setStockInfo] = useState({})
  const lastUpdatedFmt = DateTime.fromISO(stockInfo.last_updated).toLocaleString(DateTime.DATETIME_SHORT_WITH_SECONDS)
  const listOfPeriods = ['1d', '5d', '7d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']
  const [historicalData, setHistoricalData] = useState([])

  const [selectedPeriod, setPeriod] = useState(listOfPeriods[0])

  useEffect(() => {
    if (stockName !== '') {
      FetchFunction('GET', `/quote/${stockName}`, null)
        .then(res => setStockInfo(res))
        .catch(error => alert(error.msg))
      handleGetHistoricalData(selectedPeriod)
    }
  }, [stockName])

  useEffect(() => {
    handleGetHistoricalData(selectedPeriod)
  }, [selectedPeriod])

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

            <StockPriceDetails
                lastUpdatedFmt={lastUpdatedFmt}
                stockInfo={stockInfo}
            />

            <Grid item>
              <StockTimeButtons
                label={'List of periods'}
                listOfTimes={listOfPeriods}
                setDuration={setPeriod}
              />
            </Grid>

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
