import {createContext, useMemo, useState} from "react";

export const ClientContext = createContext(null);

export const ClientWrapper = ({children}) => {
    const [jwt, setJWT] = useState(null);

    const providerValue = useMemo(() => ({jwt, setJWT}), [jwt, setJWT])

    console.log(jwt)

    return (
        <ClientContext.Provider value={providerValue}>
            {children}
        </ClientContext.Provider>
    )
}

