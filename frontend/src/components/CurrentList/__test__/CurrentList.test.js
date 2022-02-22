import React from 'react'
import CurrentList from '../CurrentList'
import { render, screen } from '@testing-library/react'
import '@testing-library/jest-dom/extend-expect'
import '@testing-library/jest-dom'

test('Select component shows the correct text when first created', () => {
  render(<CurrentList currentValue={''} iterateValue={'pf'} listOfValues={[
    {
      pf: 'test1'
    },
    {
      pf: 'test2'
    },
    {
      pf: 'test3'
    }
  ]} />)
  expect(screen.getByTestId('selectCurrentList')).toHaveTextContent('Select a portfolio')
})

test('Select component shows the correct text when an element is selected', () => {
  render(<CurrentList currentValue={'test1'} iterateValue={'pf'} listOfValues={[
    {
      pf: 'test1'
    },
    {
      pf: 'test2'
    },
    {
      pf: 'test3'
    }
  ]} />)
  expect(screen.getByTestId('selectCurrentList')).toHaveTextContent('test1')
})
