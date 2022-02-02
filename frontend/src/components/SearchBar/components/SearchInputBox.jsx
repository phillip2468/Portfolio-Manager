import { SearchBox, SearchIconBox, SearchInput } from '../styled'
import SearchIcon from '@material-ui/icons/Search'
import * as PropTypes from 'prop-types'
import React from 'react'

const SearchInputBox = (props) => {
  return <SearchBox>
        <SearchInput
            type={'text'}
            placeholder={props.placeholder}
            value={props.value}
            onChange={props.onChange}
            onBlur={props.onBlur}
            onFocus={props.onFocus}
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
