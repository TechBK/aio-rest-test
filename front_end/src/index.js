/**
 * index
 * Created by techbk on 19/03/2016.
 */

import 'babel-polyfill'
import React from 'react'
import ReactDOM from 'react-dom'
import Root from './containers/Root'
import {browserHistory} from 'react-router'
import {syncHistoryWithStore} from 'react-router-redux'
import configureStore from './store'

const store = configureStore()
const history = syncHistoryWithStore(browserHistory, store)
//history.listen(location => analyticsService.track(location.pathname))

ReactDOM.render(
	<Root store={store} history={history} />,
	document.getElementById('root')
)