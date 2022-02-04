import { Grid, Typography } from '@mui/material'
import DataTable from 'react-data-table-component'
import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { FetchFunction } from '../components/FetchFunction'

const PortfolioPage = () => {
  const navigate = useNavigate()

  const [popularStocks, setPopularStocks] = useState([])

  const [listOfPortfolios, setListOfPortfolios] = useState([])

  const getListOfPortfolios = () => {
    FetchFunction('GET', '')
  }

  useEffect(() => {
    fetch('/actively-traded')
      .then((res) => res.json())
      .then((res) => {
        setPopularStocks(res)
      })
  }, [])

  const columns = [
    {
      name: 'symbol',
      selector: row => row.symbol,
      width: '100px'
    },
    {
      name: 'Name',
      selector: row => row.stock_name,
      compact: true,
      width: '250px'
    },
    {
      name: 'price',
      selector: row => row.market_current_price,
      compact: true,
      width: '100px'
    },
    {
      name: 'change %',
      selector: row => row.market_change_percentage,
      compact: true,
      width: '100px',
      format: row => (row.market_change_percentage * 100).toFixed(2)
    }
  ]

  return (
    <>
      <Grid item>
        <Typography align={'center'} variant={'h5'}>
          Portfolio page
        </Typography>
      </Grid>

      <Grid item>
        <DataTable
          columns={columns}
          data={popularStocks}
          dense={true}
          highlightOnHover={true}
          onRowClicked={(row) => navigate(`/${row.symbol}`)}
          pointerOnHover={true}
          striped={true}
          theme={'dark'}
          title={'Popular stocks today'}
        />
      </Grid>
    </>
  )
}

export default PortfolioPage
