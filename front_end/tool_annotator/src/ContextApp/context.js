import React from "react";
import { useImmer } from "use-immer";



const defaultState = {
    isLogin: false,
};

const AppContext = React.createContext();

const AppProvider = ({ children }) => {
    const [state, dispatch] = useImmer({ ...defaultState });

    return (
        <AppContext.Provider value={[state, dispatch]}>
            {children}
        </AppContext.Provider>
    );
};

export { AppProvider, AppContext };