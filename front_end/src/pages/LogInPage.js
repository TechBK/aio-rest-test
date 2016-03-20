/**
 * LogInPage
 * Created by techbk on 19/03/2016.
 */

import React, { Component, ProTypes } from 'react'
import { connect } from 'react-redux'
import { push } from 'react-router-redux'


class LogInPage extends Component {
	render(){
		return (
			<div>
				<h1>LogIn Page!!!</h1>
				<div>
					<LogInForm/>
				</div>
			</div>
		)
	}
}

export default LogInPage