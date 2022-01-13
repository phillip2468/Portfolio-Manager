import React, {useState} from 'react';
import styled from "styled-components"
import SearchIcon from "@material-ui/icons/Search";


const SearchDivBox = styled.div`
  display: flex;
  justify-content: center;
  flex-direction: column;
  align-items: center;
  position: relative;
`

const SearchBox = styled.div`
  display: flex;
  position: relative;
  justify-content: center;
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
  border-radius: 15px;
  top: 7px;
  right: 10px;
`

// noinspection CssUnknownProperty
const DataResult = styled.div`
  justify-items: center;
  display: grid;
  background-color: black;
  color: white;
  width: 500px;
  overflow-y: auto;
  height: 100px;
  scrollbar-width: none;
  position: absolute;
  border-top: 100px;
`

const SearchBar = ({placeholder, data}) => {

    const [searchWord, setSearchWord] = useState("");

    const handleSearch = (event) => {
        const searchTerm = event.target.value;
        setSearchWord(searchTerm);
    }

    return (
        <SearchDivBox>
            <SearchBox>
                <SearchInput
                    type={"text"}
                    placeholder={placeholder}
                    value={searchWord}
                    onChange={handleSearch}
                />
                <SearchIconBox>
                    <SearchIcon/>
                </SearchIconBox>
            </SearchBox>
            {searchWord.length === 0 && (
                    <DataResult>
                        {data.map((value, key)=> {
                            return <p>{value.value}</p>
                        })}
                    </DataResult>
                )
            }
        </SearchDivBox>
    );
};

export default SearchBar;