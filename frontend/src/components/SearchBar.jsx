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
  border-radius: 10px;
`

const SearchInput = styled.input`
  background-color: black;
  color: white;
  font-size: 1.3rem;
  padding: 0.5em;
  width: 500px;
  border-radius: 1em 1em 0 0;
`

const SearchIconBox = styled.div`
  display: grid;
  place-items: center;
  height: 30px;
  width: 40px;
  background-color: black;
  position: absolute;
  border-radius: 15px;
  top: 10px;
  right: 10px;
`

// noinspection CssUnknownProperty
const DataResult = styled.div`
  justify-items: center;
  display: grid;
  background-color: black;
  color: white;
  width: 525px;
  overflow-y: auto;
  height: 200px;
  scrollbar-width: none;
  z-index: 2;
  position: absolute;
  right: -262px;
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
            <div style={{position: "relative"}}>
                {searchWord.length !== 0 && (
                    <DataResult>
                        {data.map((value, key)=> {
                            return <p key={key}>{value.value}</p>
                        })}
                    </DataResult>
                )
                }
            </div>
        </SearchDivBox>
    );
};

export default SearchBar;