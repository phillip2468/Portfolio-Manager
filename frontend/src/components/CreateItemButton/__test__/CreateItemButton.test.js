import React from 'react'
import CreateItemButton from '../CreateItemButton'
import { render, screen } from '@testing-library/react'
import '@testing-library/jest-dom/extend-expect'
import '@testing-library/jest-dom'

test('Title renders with correct text', () => {
  render(<CreateItemButton text={'Create new portfolio'}/>)
  expect(screen.getByTestId('CreateItemButton')).toHaveTextContent('Create new portfolio')
})
