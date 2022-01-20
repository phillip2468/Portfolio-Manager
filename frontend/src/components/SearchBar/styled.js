import styled from "styled-components";

export const OuterContainer = styled.div`
  display: flex;
  justify-content: center;
  flex-direction: column;
  align-items: center;
  position: relative;
`


export const SearchBox = styled.div`
  display: flex;
  position: relative;
  justify-content: center;
  border-radius: 10px;
`

export const SearchInput = styled.input`
  background-color: black;
  color: white;
  font-size: 1.3rem;
  padding: 0.5em;
  width: 500px;
  &:focus {
    border-radius: 1em 1em 0 0;
  }
  border-radius: 1em 1em 1em 1em;
`

export const SearchIconBox = styled.div`
  display: grid;
  place-items: center;
  height: 30px;
  width: 40px;
  background-color: black;
  position: absolute;
  border-radius: 15px;
  top: 8px;
  right: 10px;
`

// noinspection CssUnknownProperty
export const DataResult = styled.div`
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
  cursor: pointer;
`

export const SearchResultsGrid = styled.div`
  display: inline-grid;
  grid-template-columns: 70% 15% 10%;
  grid-template-rows: 100%;
  grid-auto-flow: row;
  justify-items: stretch;
  grid-template-areas: ". . .";
  border: 2px solid #072f34;
  font-family: Arial, Helvetica, sans-serif;
  padding-left: 5%;
`

export const TriangleSymbol = styled.div`
  display: inline-block;
  border-right: 2px solid transparent;
  align-self: center;
`

export const StocksNameTicker = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: center;
`

export const StocksPrice = styled.div`
  display: flex;
  align-items: center;
`

export const StocksPercentage = styled.div`
  display: flex;
  align-items: center;
  background-color: ${props => (props.percentageChange > 0 ? "green" : "red")};
  border-radius: 5px;
  margin-top: 40%;
  margin-bottom: 40%;
`