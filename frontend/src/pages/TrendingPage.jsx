import React from 'react'
import TrendingTable from '../components/TrendingTable'
import { Grid } from '@mui/material'
import Title from '../components/Title/Title'

const TrendingPage = () => {
  return (
    <>
      <Grid item>
        <Title title={'Trending stocks from yahoo finance'}/>
      </Grid>

      <Grid item>
        <TrendingTable/>
      </Grid>
    </>

  )
}

export default TrendingPage
