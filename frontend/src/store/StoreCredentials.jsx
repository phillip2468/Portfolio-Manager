import {createContext, useEffect, useState} from "react";
import {FetchFunction} from "../components/FetchFunction";
import {useNavigate} from "react-router-dom";

// https://www.youtube.com/watch?v=xjMP0hspNLE

export const ClientContext = createContext(null);

export const ClientWrapper = ({children}) => {
    const navigate = useNavigate();
    const [loading, setLoading] = useState(true)

    const [token, setToken] = useState(()=> localStorage.getItem('token') ? localStorage.getItem('token') : null);
    const [refreshToken, setRefreshToken] = useState(()=> localStorage.getItem('refreshToken') ? localStorage.getItem('refreshToken') : null)

    const replaceRefreshToken = () => {
        console.log(refreshToken)
        if (token) {
            FetchFunction('GET', '/auth/refresh', refreshToken, null)
                .then(response => {
                    localStorage.setItem('token', response['access_token'])
                    contextData.setToken(localStorage.getItem('token'))
                })
                .catch(error => {
                    if (error !== "EarlyRefreshError") {
                        logoutUser()
                    }
                })
        }
        if (loading) {
            setLoading(false)
        }
    }

    const loginUser = (email, password) => {
        const body = {
            email: email,
            password: password,
        }
        FetchFunction('POST', 'auth/login', null, body)
            .then(response => {
                localStorage.setItem('token', response['access_token'])
                localStorage.setItem('refreshToken', response['refresh_token'])
                contextData.setToken(localStorage.getItem('token'))
                contextData.setRefreshToken(response['refresh_token'])
                navigate('/')
            })
            .catch(e => {
                console.log(e)
                alert(e)
            })
    }

    const logoutUser = () => {
        localStorage.removeItem('token')
        localStorage.removeItem('refreshToken')
        contextData.setToken(null)
        contextData.setRefreshToken(null)
        navigate('/login')
    }

    let contextData = {
        token, setToken, replaceRefreshToken, loginUser, logoutUser, refreshToken, setRefreshToken
    }

    useEffect( () => {

        if (loading) {
            replaceRefreshToken();
        }
        // eslint-disable-next-line
        let interval = setInterval(()=> {
            if (contextData.token) {
                replaceRefreshToken();
            }
        }, 1000 * 60 * 2)
        return () => clearInterval(interval)
        // eslint-disable-next-line
    }, [contextData.token, loading])
    
    return (
        <ClientContext.Provider value={contextData}>
            {children}
        </ClientContext.Provider>
    )
}