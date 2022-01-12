import React from 'react';
import styled from "styled-components"
import SearchIcon from "@material-ui/icons/Search";


const SearchDivBox = styled.div`
  display: flex;
  justify-content: center;
`

const SearchBox = styled.div`
  display: flex;
  position: relative;
`

const SearchInput = styled.input`
  background-color: black;
  color: white;
  font-size: 1.3rem;
  padding: 0.5em;
  border-radius: 1em;
  width: 500px;
`

const SearchIconBox = styled.div`
  display: grid;
  place-items: center;
  height: 30px;
  width: 40px;
  background-color: black;
  position: absolute;
  right: 10px;
  top: 8px;
  border-radius: 15px;
`

const SearchBar = ({placeholder, data}) => {
    return (
        <SearchDivBox>
            <SearchBox>
                <SearchInput
                    type={"text"}
                    placeholder={placeholder}
                />
                <SearchIconBox>
                    <SearchIcon/>
                </SearchIconBox>
            </SearchBox>
            <div className={"DropDownMenu"}>
            </div>
        </SearchDivBox>
    );
};

export default SearchBar;