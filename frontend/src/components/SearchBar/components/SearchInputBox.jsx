import { SearchBox, SearchIconBox, SearchInput } from '../styled'
import SearchIcon from '@material-ui/icons/Search'
import * as PropTypes from 'prop-types'
import React from 'react'

const SearchInputBox = (props) => {
  return <SearchBox>
        <SearchInput
            onBlur={props.onBlur}
            onChange={props.onChange}
            onFocus={props.onFocus}
            placeholder={props.placeholder}
            type={'text'}
            value={props.value}
        />
        <SearchIconBox>
            <SearchIcon/>
        </SearchIconBox>
    </SearchBox>
}

SearchInputBox.propTypes = {
  placeholder: PropTypes.any,
  value: PropTypes.string,
  onChange: PropTypes.func,
  onBlur: PropTypes.func,
  onFocus: PropTypes.func
}

export default SearchInputBox
