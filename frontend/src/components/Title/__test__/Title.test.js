import React from 'react'
import Title from '../Title'
import { render, screen } from '@testing-library/react'
import '@testing-library/jest-dom/extend-expect'
import '@testing-library/jest-dom'

test('Title renders with correct text', () => {
  render(<Title title={'Title of this page'}/>)
  expect(screen.getByTestId('Title')).toHaveTextContent('Title of this page')
})

test('Title renders with initial text set to none', () => {
  render(<Title title={''} />)
  expect(screen.getByTestId('Title')).toHaveTextContent('')
})

test('Title rerenders when different props are passed', () => {
  const { rerender } = render(<Title title={'Title of this page'}/>)
  expect(screen.getByTestId('Title')).toHaveTextContent('Title of this page')
  rerender(<Title title={'New title of this page'} />)
  expect(screen.getByTestId('Title')).toHaveTextContent('New title of this page')
})
