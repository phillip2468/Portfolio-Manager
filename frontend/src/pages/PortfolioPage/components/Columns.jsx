import { useMemo } from 'react'
import { FetchFunction } from '../../../components/FetchFunction'
import { Link } from 'react-router-dom'
import { TextField } from '@mui/material'

function findById (array, id) {
  return array.findIndex((d) => d.portfolio_id === id)
}

function Columns (listOfStocks, setListOfStocks, userId) {
  return useMemo(() => {
    const handleCellEditable = (field) => (row) => (e) => {
      if (e.target.value >= 0) {
        const newRow = { ...row }
        newRow[field] = e.target.value

        const newData = listOfStocks.slice(0)
        newData[findById(listOfStocks, row.portfolio_id)] = newRow
        setListOfStocks(newData)

        const body = {
          units_price: newRow.units_price,
          units_purchased: newRow.units_purchased
        }
        FetchFunction('PATCH', `portfolio/${userId}/${newRow.portfolio_name}/${newRow.stock_details.stock_id}`, body)
          .then(res => console.log(res))
          .catch(error => alert(error))
      }
    }

    return [
      {
        name: 'symbol',
        selector: row => row.stock_details.symbol,
        sortable: true,
        cell: row => <Link target="_blank" to={`/${row.stock_details.symbol}`}>{row.stock_details.symbol}</Link>
      },
      {
        name: 'exchange',
        selector: row => row.stock_details.exchange,
        sortable: true
      },
      {
        name: 'Name',
        selector: row => row.stock_details.stock_name,
        wrap: true,
        sortable: true
      },
      {
        name: 'Last',
        selector: row => row.stock_details.market_current_price,
        sortable: true
      },
      {
        name: 'Currency',
        selector: row => row.stock_details.currency,
        sortable: true
      },
      {
        name: 'Todays change %',
        selector: row => row.stock_details.market_change_percentage,
        sortable: true,
        format: row => (row.stock_details.market_change_percentage * 100).toFixed(2)
      },
      {
        name: 'Unit price',
        selector: row => row.units_price,
        sortable: true,
        cell: (row) => (
          <TextField
            onChange={handleCellEditable('units_price')(row)}
            value={row.units_price}
          />
        )
      },
      {
        name: 'Units',
        selector: row => row.units_purchased,
        sortable: true,
        cell: (row) => (
          <TextField
            onChange={handleCellEditable('units_purchased')(row)}
            style={{ fontSize: '5px' }}
            value={row.units_purchased}
          />
        )
      },
      {
        name: 'Value',
        selector: row => (row.units_purchased * row.units_price),
        sortable: true,
        format: row => ((parseFloat(row.units_purchased) * row.units_price).toFixed(2))
      },
      {
        name: 'Loss/Gain %',
        selector: row => (100 - ((row.units_price / row.stock_details.market_current_price) * 100)),
        sortable: true,
        format: row => (100 - ((row.units_price / row.stock_details.market_current_price) * 100)).toFixed(2)
      }
    ]
  }, [listOfStocks])
}

export default Columns
