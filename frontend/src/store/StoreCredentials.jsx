import {createContext, useEffect, useState} from "react";
import {FetchFunction} from "../components/FetchFunction";
import {useNavigate} from "react-router-dom";

// https://www.youtube.com/watch?v=xjMP0hspNLE

export const ClientContext = createContext(null);

export const ClientWrapper = ({children}) => {
    const navigate = useNavigate();
    const [loggedIn, setLoggedIn] = useState(false)

    const loginUser = (email, password) => {
        const body = {
            email: email,
            password: password,
        }
        FetchFunction('POST', 'auth/login', null, body)
            .then(() => {
                setLoggedIn(true)
                navigate('/')
            })
            .catch(e => {
                console.log(e)
            })
    }


    const logoutUser = () => {
        FetchFunction('POST', 'auth/logout', null, null)
            .then(res => {
                console.log(res)
                setLoggedIn(false)
                navigate('/login')
            })
            .catch(res => console.log(res))
    }

    const findUser = () => {
        FetchFunction('GET', 'auth/which_user', null, null)
            .then(() => {
                setLoggedIn(true)
            })
            .catch(()=> {
                setLoggedIn(false)
            })
    }


    let contextData = {
       loginUser, logoutUser, findUser, loggedIn, setLoggedIn
    }

    useEffect( () => {
        // eslint-disable-next-line
        findUser()
    }, [loggedIn])

    return (
        <ClientContext.Provider value={contextData}>
            {children}
        </ClientContext.Provider>
    )
}