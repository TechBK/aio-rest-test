/**
 * Created by techbk on 18/03/2016.
 */

import { createStore, applyMiddleware, compose } from 'redux'
import thunkMiddleware from 'redux-thunk'
import createLogger from 'redux-logger'
import promiseMiddleware from 'redux-promise-middleware'

//import { routerMiddleware } from 'react-router-redux'
import { browserHistory } from 'react-router'
import rootReducer from '../reducers'

//const reduxRouterMiddleware = syncHistory(browserHistory)
const loggerMiddleware = createLogger()

export default function configureStore(initialState){
	return createStore(
		rootReducer,
		initialState,
		compose(
			applyMiddleware(
				promiseMiddleware({
					promiseTypeSuffixes: ['LOADING', 'SUCCESS', 'ERROR']
				}),
				thunkMiddleware,
				loggerMiddleware
			),
			window.devToolsExtension ? window.devToolsExtension() : undefined
		)
	)
}
