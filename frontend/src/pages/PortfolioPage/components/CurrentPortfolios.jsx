import { Grid, MenuItem, Select } from '@mui/material'
import * as PropTypes from 'prop-types'

function CurrentPortfolios (props) {
  return <Grid container direction={'row'} justifyContent={'center'} spacing={2}>
    <Select
      displayEmpty
      onChange={props.onChange}
      renderValue={props.renderValue}
      sx={{ width: '210px' }}
      value={props.value}
      variant={'standard'}
    >
      <MenuItem disabled value="">
        <em>Select...</em>
      </MenuItem>
      {
        props.listOfPortfolios.map(props.callbackfn
        )}
    </Select>
  </Grid>
}

CurrentPortfolios.propTypes = {
  onChange: PropTypes.func,
  renderValue: PropTypes.func,
  value: PropTypes.string,
  listOfPortfolios: PropTypes.arrayOf(PropTypes.any),
  callbackfn: PropTypes.func
}
export default CurrentPortfolios
