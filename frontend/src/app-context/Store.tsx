import React, { createContext, ReactNode, useState } from "react"

interface CardState {
    cards: any[],
    waitingNum: number,
}

// interface AppState {
//     cardState: CardState,
//     updateCardState: (newState: Partial<AppState>) => void;
// }

interface AppState {
    cards: any[],
    waitingNum: number,
    updateCardState: (newState: Partial<AppState>) => void;
}

const defaultCardState: CardState = {
    cards: [],
    waitingNum: 0,
}

// const initialState : AppState = {
//     cardState: defaultCardState,
//     updateCardState: (_newState?: Partial<AppState>) => {},
// }

const initialState : AppState = {
    cards: [],
    waitingNum: 0,
    updateCardState: (_newState?: Partial<AppState>) => {},
}

interface Props {
    children: React.ReactNode
}

export const Context = createContext<AppState>(initialState);    


// Fix any with component
export const UserContextProvider: React.FunctionComponent<Props> = (props: Props): JSX.Element => {
    const [state, setState] = useState(initialState);
    const updateCardState = (newState: Partial<AppState>) => {
        setState({ ...state, ...newState })
    }

    return (
        <Context.Provider value={{ ...state, updateCardState }}>{props.children}</Context.Provider>
        // <Context.Provider value={[state, setState]}>{props.children}</Context.Provider>
    )
}

// ==========

