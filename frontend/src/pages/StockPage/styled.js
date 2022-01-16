import styled from "styled-components";

export const StockPercentageChange = styled.div`
  display: flex;
  align-items: center;
  background-color: ${props => (props.percentageChange > 0 ? "green" : "red")};
  border-radius: 5px;
`