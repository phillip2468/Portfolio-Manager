import React, {useEffect, useState} from 'react';
import styled from "styled-components"
import SearchIcon from "@material-ui/icons/Search";


const OuterContainer = styled.div`
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
  display: grid;
  background-color: black;
  color: white;
  width: 525px;
  overflow-y: auto;
  height: 250px;
  scrollbar-width: none;
  z-index: 2;
  position: absolute;
  right: -262px;
`

const SearchResultsGrid = styled.div`
  display: inline-grid;
  grid-template-columns: 70% 20% 10%;
  grid-template-rows: 100%;
  grid-auto-flow: row;
  justify-items: stretch;
  grid-template-areas: ". . .";
  border: 2px solid #072f34;
  font-family: Arial, Helvetica, sans-serif;;
`


const SearchBar = ({placeholder, data}) => {

    const [typedInput, setTypedInput] = useState("");
    const [filteredData, setFilteredData] = useState([]);
    const [searchable, setSearchable] = useState([])

    useEffect(()=> {
            fetch('/quote/search')
                .then((res) => res.json())
                .then((res) => {
                    setSearchable(Object.values(res))
                })
        }
        , [])


    const handleSearch = (event) => {
        const searchTerm = event.target.value;
        setTypedInput(searchTerm);

        const newFilter = searchable.filter((value) => {
            return value.stock_name.toLowerCase().includes(typedInput.toLowerCase())
        })
        if (typedInput === "") {
            setFilteredData([]);
        } else {
            setFilteredData(newFilter);
        }
    }

    return (
        <OuterContainer>
            <SearchBox>
                <SearchInput
                    type={"text"}
                    placeholder={placeholder}
                    value={typedInput}
                    onChange={handleSearch}
                />
                <SearchIconBox>
                    <SearchIcon/>
                </SearchIconBox>
            </SearchBox>
            <div style={{position: "relative"}}>
                {typedInput.length !== 0 && (
                    <DataResult>
                        {filteredData.map((value, key)=> {
                            return <SearchResultsGrid
                                key={key}>
                                <div style={{display: "flex", flexDirection: "column", paddingLeft: "5%", justifyContent: "center"}}>
                                    <div>{value.stock_name}</div>
                                    <div>{value.symbol}</div>
                                </div>
                                <div style={{display: "flex", alignItems: "center"}}>
                                    ${value.price}
                                </div>
                                <div style={{display: "flex", alignItems: "center"}}>
                                    {value.change.toFixed(2)}
                                </div>
                            </SearchResultsGrid>
                        })}
                    </DataResult>
                )
                }
            </div>
        </OuterContainer>
    );
};

export default SearchBar;