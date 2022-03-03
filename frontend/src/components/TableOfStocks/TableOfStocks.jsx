import DataTable from 'react-data-table-component'
import * as PropTypes from 'prop-types'
import ListOfTitle from '../TableOfStocksTitle/ListOfTitle'

const titleComponent = (props) => {
  if (props.selectedItem) {
    return <ListOfTitle
      changedValue={props.changedTitle}
      currentValue={`${props.selectedItem}`}
      route={props.route}
      routeBody={props.routeBody}
      setChangedValue={props.setChangedTitle}
    />
  }
}

const TableOfStocks = (props) => {
  return <DataTable
    actions={props.actions}
    clearSelectedRows={props.clearSelectedRows}
    columns={props.columns}
    contextActions={props.contextActions}
    data={props.data}
    data-testid={'TableOfStocks'}
    defaultSortFieldId={'symbol'}
    highlightOnHover={true}
    onSelectedRowsChange={props.onSelectedRowsChange}
    pagination={true}
    pointerOnHover={true}
    selectableRows={true}
    theme={'dark'}
    title={titleComponent(props)}
  />
}

TableOfStocks.propTypes = {
  actions: PropTypes.any,
  clearSelectedRows: PropTypes.bool,
  columns: PropTypes.any,
  contextActions: PropTypes.any,
  data: PropTypes.arrayOf(PropTypes.any),
  onSelectedRowsChange: PropTypes.func,
  selectedItem: PropTypes.string,
  setChangedTitle: PropTypes.func,
  changedTitle: PropTypes.bool,
  route: PropTypes.string,
  routeBody: PropTypes.string
}

export default TableOfStocks
