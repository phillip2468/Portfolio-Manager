import DataTable from 'react-data-table-component'
import * as PropTypes from 'prop-types'

const TableOfStocks = (props) => {
  return <DataTable
    actions={props.actions}
    clearSelectedRows={props.clearSelectedRows}
    columns={props.columns}
    contextActions={props.contextActions}
    data={props.data}
    defaultSortFieldId={'symbol'}
    highlightOnHover={true}
    keyField={'portfolio_id'}
    onSelectedRowsChange={props.onSelectedRowsChange}
    pagination={true}
    pointerOnHover={true}
    selectableRows={true}
    theme={'dark'}
    title={`${props.selectedPortfolio} portfolio's`}
  />
}

TableOfStocks.propTypes = {
  actions: PropTypes.any,
  clearSelectedRows: PropTypes.bool,
  columns: PropTypes.any,
  contextActions: PropTypes.any,
  data: PropTypes.arrayOf(PropTypes.any),
  onSelectedRowsChange: PropTypes.func,
  selectedPortfolio: PropTypes.string
}

export default TableOfStocks
