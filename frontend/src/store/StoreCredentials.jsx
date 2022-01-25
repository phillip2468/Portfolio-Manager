import {createContext, useEffect, useMemo, useState} from "react";
import {FetchFunction} from "../components/FetchFunction";

export const ClientContext = createContext(null);

export const ClientWrapper = ({children}) => {
    const [token, setToken] = useState(()=> localStorage.getItem('token') ? localStorage.getItem('token') : null);
    const [loading, setLoading] = useState(true);

    const providerValue = useMemo(() => ({token, setToken}), [token, setToken])

    const refreshToken = () => {
        if (token) {
            FetchFunction('GET', '/auth/refresh', token, null)
                .then(response => {
                    console.log(response)
                    localStorage.setItem('token', response["access_token"])
                    setToken(localStorage.getItem('token'))
                })
                .catch(error => {
                    alert(error)
                    //localStorage.removeItem('token');
                })
        }

        if (loading) {
            setLoading(false);
        }
    }

    useEffect( () => {
        if (loading) {
            refreshToken()
        }

        refreshToken();
        // eslint-disable-next-line
        let interval = setInterval(()=> {
            if (token) {
                refreshToken();
            }
        }, 100000000)
        return () => clearInterval(interval)

    }, [token, loading])
    
    return (
        <ClientContext.Provider value={providerValue}>
            {loading ? null : children}
        </ClientContext.Provider>
    )
}