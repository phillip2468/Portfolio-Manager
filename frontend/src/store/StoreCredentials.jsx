import { createContext, useEffect, useState } from 'react'
import { FetchFunction } from '../components/FetchFunction'
import { useNavigate } from 'react-router-dom'
import * as PropTypes from 'prop-types'

// https://www.youtube.com/watch?v=xjMP0hspNLE

export const ClientContext = createContext(null)

export const ClientWrapper = ({ children }) => {
  const navigate = useNavigate()
  const [loggedIn, setLoggedIn] = useState(false)
  const [userId, setUserId] = useState(null)

  const loginUser = (email, password) => {
    const body = {
      email: email,
      password: password
    }
    FetchFunction('POST', 'auth/login', body)
      .then(() => {
        setLoggedIn(true)
        navigate('/')
      })
      .catch(e => {
        alert(e.msg)
      })
  }

  const logoutUser = () => {
    FetchFunction('POST', 'auth/logout', null)
      .then(res => {
        console.log(res)
        setLoggedIn(false)
        navigate('/login')
      })
      .catch(res => alert(e.msg))
  }

  const findUser = () => {
    FetchFunction('GET', 'auth/which_user', null)
      .then((res) => {
        setLoggedIn(true)
        setUserId(res.user_id)
      })
      .catch(() => {
        setLoggedIn(false)
      })
  }

  const contextData = {
    loginUser, logoutUser, findUser, loggedIn, setLoggedIn, userId
  }

  useEffect(() => {
    // eslint-disable-next-line
        findUser()
  }, [loggedIn])

  return (
        <ClientContext.Provider value={contextData}>
            {children}
        </ClientContext.Provider>
  )
}

ClientWrapper.propTypes = {
  children: PropTypes.any
}
