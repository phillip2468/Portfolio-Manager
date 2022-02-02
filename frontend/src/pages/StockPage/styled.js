import styled from 'styled-components'

export const StockPercentageChange = styled.div`
  display: flex;
  align-items: center;
  background-color: ${props => (props.percentageChange > 0 ? 'green' : 'red')};
  border-radius: 5px;
`

export const StockInfoContainer = styled.div`
  display: flex;
  column-gap: 2%;
  align-items: center;
`

export const MiscDetailsStock = styled.div`
    font-size: 0.75em;
`
