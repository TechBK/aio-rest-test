/**
 * Created by techbk on 19/03/2016.
 */

import {createStore, combineReducers} from 'redux'
import {reducer as formReducer} from 'redux-form'
import { routerReducer } from 'react-router-redux'

const reducer = combineReducers({
	form: formReducer,
	routing: routerReducer
})

export default reducer