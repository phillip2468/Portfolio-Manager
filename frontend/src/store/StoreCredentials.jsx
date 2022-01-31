import {createContext, useEffect, useState} from "react";
import {FetchFunction} from "../components/FetchFunction";
import {useNavigate} from "react-router-dom";

// https://www.youtube.com/watch?v=xjMP0hspNLE

export const ClientContext = createContext(null);

export const ClientWrapper = ({children}) => {
    const navigate = useNavigate();


    const loginUser = (email, password) => {
        const body = {
            email: email,
            password: password,
        }
        FetchFunction('POST', 'auth/login', null, body)
            .then(response => {
                console.log(response)
                alert(response)
            })
            .catch(e => {
                console.log(e)
                alert(e)
            })
    }

    const logoutUser = () => {
        FetchFunction('POST', 'auth/logout', null, null)
            .then(res => res.json())
            .then(res => {
                alert(res)
                navigate('/login')
            })
            .catch(error => alert(error))
    }

    let contextData = {
       loginUser, logoutUser
    }

    useEffect( () => {
        // eslint-disable-next-line
    }, [])

    return (
        <ClientContext.Provider value={contextData}>
            {children}
        </ClientContext.Provider>
    )
}