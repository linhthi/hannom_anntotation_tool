import { useContext} from "react";

import { AppContext } from "./context";


const useAppContext = () => {
    const [state, dispatch] = useContext(AppContext);


    function updateIsLogin(isLogin) {
        dispatch((draft) => {
            draft.isLogin = isLogin;
        })
    }


    return {
        ...state,
        updateIsLogin,
    };
};

export { useAppContext };