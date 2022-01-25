import {createContext, useEffect, useMemo, useState} from "react";
import {FetchFunction} from "../components/FetchFunction";

export const ClientContext = createContext(null);

export const ClientWrapper = ({children}) => {
    const [token, setToken] = useState(null);

    const providerValue = useMemo(() => ({token, setToken}), [token, setToken])

    const refreshToken = async () => {
        try {
            const response = await FetchFunction('GET', '/auth/refresh', token, null);
            localStorage.setItem('token', response["access_token"])
            setToken(localStorage.getItem('token'))
        } catch (e) {
            console.log(e)
        }

    }

    useEffect(async () => {
        if (token !== null) {
            setTimeout(async () => {
                await refreshToken();
            }, 10000)
        }

    }, [token])
    return (
        <ClientContext.Provider value={providerValue}>
            {children}
        </ClientContext.Provider>
    )
}