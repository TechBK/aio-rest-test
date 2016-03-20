/**
 * Created by quang_000 on 03/02/2016.
 */

import { createStore, applyMiddleware, compose } from 'redux'
import thunkMiddleware from 'redux-thunk'
import createLogger from 'redux-logger'
import rootReducer from '../reducers'

const loggerMiddleware = createLogger()

export default function configureStore(initialState){
  return createStore(
    rootReducer,
    initialState, compose(
      applyMiddleware(
        thunkMiddleware,
        loggerMiddleware
      ),
      window.devToolsExtension ? window.devToolsExtension() : undefined
    )
  )
}